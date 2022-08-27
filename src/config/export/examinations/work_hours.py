import os
import pandas
from collections import defaultdict
from difflib import SequenceMatcher
from django.db.models import Sum, Count, F, Q, FloatField
from django.db.models.functions import Coalesce, Cast
from django.conf import settings


class WorkHourExaminationExporter:
    def __init__(self, survey_model, product_model):
        self.survey_model = survey_model
        self.product_model = product_model
        invalid_farmers = survey_model.objects.filter(note__icontains='無效戶').values_list('farmer_id', flat=True).distinct()
        self.survey_qs = survey_model.objects.filter(readonly=False).exclude(farmer_id__in=invalid_farmers)

    def farmer_id_generator(self):
        for obj in self.survey_qs.filter(page=1).order_by('farmer_id').iterator():
            yield obj.farmer_id

    def self_work_hour_generator(self):
        qs = self.survey_qs.prefetch_related(
            'populations', 'populations__farmer_work_day'
        ).values('farmer_id').annotate(
            hours=Coalesce(Sum(F('populations__farmer_work_day__min_day') * 8), 0),
        ).order_by('farmer_id')
        for obj in qs.iterator():
            yield obj['hours']

    def long_term_hire_work_hour_generator(self):
        # Annotate number workers
        qs1 = self.survey_qs.prefetch_related(
            'long_term_hires', 'long_term_hires__number_workers'
        ).values(
            'farmer_id', 'long_term_hires__id'
        ).annotate(
            number_workers=Cast(Coalesce(Sum('long_term_hires__number_workers__count'), 0), FloatField()),
        )
        df1 = pandas.DataFrame(qs1).set_index('farmer_id', 'long_term_hires__id')
        # Annotate number months
        qs2 = self.survey_qs.prefetch_related('long_term_hires').values(
            'farmer_id', 'long_term_hires__id'
        ).annotate(
            months=Cast(Count('long_term_hires__months'), FloatField()),
            avg_work_day=Cast(Coalesce('long_term_hires__avg_work_day', 0), FloatField()),
        )
        df2 = pandas.DataFrame(qs2).set_index('farmer_id', 'long_term_hires__id')
        # Merge tables
        df = pandas.merge(df1, df2, on=['farmer_id', 'long_term_hires__id'])
        df['work_hours'] = df['number_workers'] * df['months'] * df['avg_work_day'] * 8
        df = df.groupby(['farmer_id']).agg({'work_hours': "sum"}).sort_values('farmer_id')
        # Iterate rows
        for _, row in df.iterrows():
            yield round(row['work_hours'])

    def short_term_hire_work_hour_generator(self):
        # Annotate number workers
        qs = self.survey_qs.prefetch_related('short_term_hires', 'short_term_hires__number_workers').values(
            'farmer_id', 'short_term_hires__id'
        ).annotate(
            number_workers=Cast(Coalesce(Sum('short_term_hires__number_workers__count'), 0), FloatField()),
            avg_work_day=Cast(Coalesce('short_term_hires__avg_work_day', 0), FloatField()),
        )
        df = pandas.DataFrame(qs).set_index('farmer_id', 'short_term_hires__id')
        df['work_hours'] = df['number_workers'] * df['avg_work_day'] * 8
        df = df.groupby(['farmer_id']).agg({'work_hours': "sum"}).sort_values('farmer_id')
        # Iterate rows
        for _, row in df.iterrows():
            yield round(row['work_hours'])

    def crop_marketing_work_hour_generator(self):
        # 列舉有 child 的 product
        parent_products = defaultdict(dict)
        for obj in self.product_model.objects.filter(parent__isnull=False):
            parent_products[obj.parent.id][obj.name] = (obj.min_hour, obj.max_hour)
        # 處理預設值
        qs = self.survey_qs.prefetch_related(
            'crop_marketings', 'crop_marketings__product',
        ).values(
            'farmer_id',
            'crop_marketings__name',
            'crop_marketings__product__id',
            'crop_marketings__product__management_type'
        ).annotate(
            land_area=Cast(Coalesce('crop_marketings__land_area', 0), FloatField()),
            plant_times=Cast(Coalesce('crop_marketings__plant_times', 0), FloatField()),
            min_hour=Cast(Coalesce('crop_marketings__product__min_hour', 0), FloatField()),
            max_hour=Cast(Coalesce('crop_marketings__product__max_hour', 0), FloatField()),
        )
        df = pandas.DataFrame(qs)
        # 1. 經營類型為果樹，或是 parent product 的一起算
        df1 = df.loc[
            df['crop_marketings__product__id'].isin(parent_products.keys())
            | df['crop_marketings__product__management_type'] == 6
        ].copy(deep=True)
        # 1.1 果樹只取最大面積，做排序後只留第一筆
        df1['rank'] = df1.groupby(
            ['farmer_id', 'crop_marketings__product__management_type']
        )['land_area'].rank("dense", ascending=False)
        drops = df1.loc[(df1['rank'] > 1) & (df1['crop_marketings__product__management_type'] == 6)].index
        df1.drop(drops, inplace=True)
        # 1.2 將使用者輸入的產品名稱與 sub product 做匹配，相符的話將 product 工時取代為 sub product 工時
        for index, row in df1.iterrows():
            rate = 0.6
            for sub_name, (min_hour, max_hour) in parent_products[row['crop_marketings__product__id']].items():
                mr = SequenceMatcher(None, row['crop_marketings__name'], sub_name).ratio()
                if mr >= rate:
                    df1.at[index, 'min_hour'] = min_hour
                    df1.at[index, 'max_hour'] = max_hour
                    rate = mr
        df1['min_hour'] = df1['land_area'] / 100 * df1['plant_times'] * df1['min_hour']
        df1['max_hour'] = df1['land_area'] / 100 * df1['plant_times'] * df1['max_hour']
        df1 = df1.groupby(['farmer_id']).agg({'min_hour': 'sum', 'max_hour': 'sum'})
        # 2. 其他的一起算
        df2 = df.loc[
            ~df['crop_marketings__product__id'].isin(parent_products.keys())
            | df['crop_marketings__product__management_type'] != 6
        ].copy(deep=True)
        df2['min_hour'] = df2['land_area'] / 100 * df2['plant_times'] * df2['min_hour']
        df2['max_hour'] = df2['land_area'] / 100 * df2['plant_times'] * df2['max_hour']
        df2 = df2.groupby(['farmer_id']).agg({'min_hour': 'sum', 'max_hour': 'sum'})
        # 合併兩個 table 後再做一次 group sum
        df = pandas.concat([df1, df2])
        df = df.groupby(['farmer_id']).agg({'min_hour': 'sum', 'max_hour': 'sum'}).sort_values('farmer_id')
        # Iterate rows
        for _, row, in df.iterrows():
            yield row['min_hour'], row['max_hour']

    def livestock_marketing_work_hour_generator(self):
        qs = self.survey_qs.prefetch_related(
            'livestock_marketings', 'livestock_marketings__product',
        ).values(
            'farmer_id',
            'livestock_marketings__id',
        ).annotate(
            raising_number=Cast(Coalesce('livestock_marketings__raising_number', 0), FloatField()),
            min_hour=Cast(Coalesce('livestock_marketings__product__min_hour', 0), FloatField()),
            max_hour=Cast(Coalesce('livestock_marketings__product__max_hour', 0), FloatField()),
        ).annotate(
            min_hour=F('raising_number') * F('min_hour'),
            max_hour=F('raising_number') * F('max_hour')
        ).values(
            'farmer_id'
        ).annotate(
            min_hour=Sum('min_hour'),
            max_hour=Sum('max_hour')
        ).order_by('farmer_id')
        for obj in qs.iterator():
            yield obj['min_hour'], obj['max_hour']

    @staticmethod
    def get_examination_result_display(hour, min_hour, max_hour):
        if hour < min_hour:
            return '低於下限'
        elif hour > max_hour:
            return '高於下限'
        return '正常'

    @staticmethod
    def check_exhausted(*gens):
        return all(
            [
                len(list(gen)) == 0
                for gen in gens
            ]
        )

    def __call__(self):
        headers = [
            "農戶編號",
            "自家工時",
            "常僱工時",
            "臨僱工時",
            "自家 + 僱用小時",
            "最小工時",
            "最大工時",
            "工時撿誤範圍",
            "與最大工時差距",
        ]
        yield headers

        farmer_id_gen = self.farmer_id_generator()
        self_work_hour_gen = self.self_work_hour_generator()
        long_term_hire_work_hour_gen = self.long_term_hire_work_hour_generator()
        short_term_hire_work_hour_gen = self.short_term_hire_work_hour_generator()
        crop_work_hour_gen = self.crop_marketing_work_hour_generator()
        livestock_work_hour_gen = self.livestock_marketing_work_hour_generator()

        while True:
            try:
                self_hours = next(self_work_hour_gen)
                long_term_hours = next(long_term_hire_work_hour_gen)
                short_term_hours = next(short_term_hire_work_hour_gen)
                hire_hours = self_hours + long_term_hours + short_term_hours
                crop_min, crop_max = next(crop_work_hour_gen)
                livestock_min, livestock_max = next(livestock_work_hour_gen)
                min_hours = round(crop_min + livestock_min)
                max_hours = round(crop_max + livestock_max)
                yield [
                    next(farmer_id_gen),
                    self_hours,
                    long_term_hours,
                    short_term_hours,
                    hire_hours,
                    min_hours,
                    max_hours,
                    self.get_examination_result_display(hire_hours, min_hours, max_hours),
                    max_hours - hire_hours
                ]
            except StopIteration:
                if not self.check_exhausted(
                        farmer_id_gen,
                        self_work_hour_gen,
                        long_term_hire_work_hour_gen,
                        short_term_hire_work_hour_gen,
                        crop_work_hour_gen,
                        livestock_work_hour_gen,
                ):
                    yield ["匯出錯誤：", "匯出結果不完整"]
                break

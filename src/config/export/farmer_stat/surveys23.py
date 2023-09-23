import os
import pandas
from django.db.models import Sum, Max, F, OuterRef, Subquery
from django.db.models.functions import Coalesce
from apps.surveys23.models import Survey, ManagementType, Stratify, FarmerStat


class FarmerStatExporter111:
    def __init__(self):
        invalid_farmers = Survey.objects.filter(note__icontains='無效戶').values_list('farmer_id', flat=True).distinct()
        self.survey_qs = Survey.objects.filter(readonly=False).exclude(farmer_id__in=invalid_farmers)

    @staticmethod
    def get_stratify_df():
        df = pandas.DataFrame(columns=['id', 'stratify', 'magnification_factor'])
        for i, obj in enumerate(Stratify.objects.all()):
            df.loc[i] = [obj.pk, obj.code, obj.magnification_factor if obj.sample_count > 0 else '-']
        return df

    def get_farmer_df(self):
        management_types = ManagementType.objects.filter(surveys__page=1, surveys__readonly=False,
                                                         surveys=OuterRef('pk'))

        qs = self.survey_qs.filter(page=1).prefetch_related(
            'land_areas', 'farm_location__code', 'farmer_stat', 'crop_marketings', 'livestock_marketings'
        ).values('farmer_id').annotate(
            region_code=F('farm_location__code__region'),
            city_code=F('farm_location__code__code'),
            product_type=Subquery(management_types.values('type')[:1]),
            management_type=Subquery(management_types.values('code')[:1]),
            stratify=Coalesce(F('farmer_stat__stratify'), -1),
        )
        df = pandas.DataFrame(qs)
        df['city_code'] = df['city_code'].apply(lambda x: x.zfill(4)[:2])
        return df

    def get_year_sales_df(self):
        qs = self.survey_qs.prefetch_related(
            'crop_marketings', 'livestock_marketings'
        ).values('farmer_id').annotate(
            crop_year_sales=Coalesce(Sum('crop_marketings__year_sales'), 0),
            livestock_year_sales=Coalesce(Sum('livestock_marketings__year_sales'), 0)
        )
        df = pandas.DataFrame(qs)
        df['total_year_sales'] = df['crop_year_sales'] + df['livestock_year_sales']
        return df

    def get_land_area_df(self):
        qs = self.survey_qs.values('farmer_id', 'crop_marketings__land_number').order_by().annotate(
            land_area=Max('crop_marketings__land_area'))
        df = pandas.DataFrame(qs)
        df = df.groupby('farmer_id', as_index=False).agg({'land_area': 'sum'})
        return df

    def __call__(self, *args, **kwargs):
        assert FarmerStat.objects.count() > 0, "FarmerStats are not yet resolved."

        farmer_df = self.get_farmer_df()
        stratify_df = self.get_stratify_df()
        year_sales_df = self.get_year_sales_df()
        land_areas_df = self.get_land_area_df()

        # Join dataframes
        farmer_df = farmer_df.set_index('stratify').join(stratify_df.set_index('id'))
        farmer_df = farmer_df.set_index('farmer_id').join(year_sales_df.set_index('farmer_id'))
        farmer_df = farmer_df.join(land_areas_df.set_index('farmer_id'))

        # Formatting dataframe
        farmer_df = farmer_df.astype({"stratify": int, "land_area": int}).sort_index()
        farmer_df.index.name = '農戶編號'
        farmer_df.rename({
            'region_code': '四區代碼',
            'city_code': '縣市代碼',
            'product_type': '農1畜2',
            'management_type': '主要經營型態',
            'stratify': '層別',
            'magnification_factor': '擴大係數',
            'crop_year_sales': '農耕銷售額',
            'livestock_year_sales': '畜禽銷售額',
            'total_year_sales': '銷售額總計',
            'land_area': '耕地面積（公畝）'
        }, axis=1, inplace=True)

        # Export dataframe
        farmer_df.to_excel(*args, **kwargs)

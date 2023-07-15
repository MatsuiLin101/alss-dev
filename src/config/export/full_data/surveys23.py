import logging
import operator
from functools import reduce
from enum import Enum
from collections import OrderedDict
from django.db.models import Q

from apps.surveys23.models import (
    Survey,
    AgeScope
)

logging.getLogger(__file__).setLevel(logging.INFO)

FIELDS = [
    "農戶編號",
    "受訪人姓名",
    "與名冊戶長關係",
    "電話1",
    "電話2",
    "地址與名冊相不相同",
    "地址",
    "可耕地或畜牧用地所在地區",
    "可耕地或畜牧用地所在地區代號",
    "耕作地類型",
    "耕作地狀態",
    "耕作地面積",
    "兼營農業相關事業",
    "其他填寫",
    "主要經營型態",
    "作物代碼",
    "作物名稱",
    "耕作地編號",
    "種植面積",
    "種植次數",
    "計量單位",
    "全年銷售額",
    "是否使用農業設施",
    "作物備註",
    "畜禽代碼",
    "畜禽名稱",
    "計量單位",
    "年底在養數量",
    "全年銷售額",
    "契約飼養",
    "畜禽備註",
    "銷售類型",
    "銷售額區間",
    "全年主要淨收入來源",
    "年齡分類",
    "戶內人口性別",
    "戶內人口數",
    "與經濟戶長關係",
    "性別",
    "出生年",
    "教育程度別",
    "自家農牧業工作日數",
    "全年主要生活型態",
    "僱工情形",
    "常僱主要工作類型",
    "常僱平均工作日數",
    "常僱月份",
    "常僱合計",
    "常僱(44歲以下)",
    "常僱(45-64歲)",
    "常僱(65歲以上)",
    "臨僱主要工作類型",
    "臨僱平均工作日數",
    "臨僱月份",
    "臨僱合計",
    "臨僱(44歲以下)",
    "臨僱(45-64歲)",
    "臨僱(65歲以上)",
    "不支薪僱用月份",
    "不支薪人數",
    "不支薪平均工作日數",  # new 112
    "短缺情形",
    "常缺工作類型",
    "常缺各月人數",
    "常缺各月平均日數",
    "常缺月份",
    "臨缺工作類型",
    "臨缺產品代碼",
    "臨缺產品名稱",
    "臨缺各月人數",
    "臨缺各月平均日數",
    "臨缺月份",
    # apply_method=1
    "是否聽過人力團",
    "是否有申請人力團",
    "有申請人力團情形",
    "無申請人力團原因",
    # apply_method=2
    "是否聽過農業外籍移工",
    "是否有申請農業外籍移工",
    "有申請農業外籍移工情形",
    "無申請農業外籍移工原因",
    # apply_method=3
    "是否聽過外籍青農",
    "是否有申請外籍青農",
    "有申請外籍青農情形",
    "無申請外籍青農原因",
    "是否使用人力平台或好幫手APP",
    "調查員",
    "初審員",
]


class SurveyRelationGeneratorFactory111:
    """A highlevel class controls how to export all surveys."""

    def __init__(self, filters={}, excludes={}, limit=None):
        self.surveys = (
            Survey.objects.filter(readonly=False)
            .order_by("farmer_id", "page")
            .prefetch_related(
                "address_match",
                "farm_location",
                "farm_location__code",
                "land_areas",
                "land_areas__type",
                "land_areas__status",
                "businesses",
                "businesses__farm_related_business",
                "management_types",
                "crop_marketings",
                "crop_marketings__product",
                "crop_marketings__unit",
                "crop_marketings__loss",
                "livestock_marketings",
                "livestock_marketings__product",
                "livestock_marketings__unit",
                "livestock_marketings__contract",
                "livestock_marketings__loss",
                "annual_incomes",
                "annual_incomes__market_type",
                "annual_incomes__income_range",
                "population_ages",
                "population_ages__age_scope",
                "population_ages__gender",
                "populations",
                "populations__relationship",
                "populations__gender",
                "populations__education_level",
                "populations__life_style",
                "no_salary_hires",
                "no_salary_hires__month",
                "lacks",
                "long_term_hires",
                "long_term_hires__work_type",
                "long_term_hires__months",
                "long_term_hires__number_workers",
                "short_term_hires",
                "short_term_hires__work_types",
                "short_term_hires__number_workers",
                "short_term_hires__month",
                "long_term_lacks",
                "long_term_lacks__work_type",
                "short_term_lacks",
                "short_term_lacks__work_type",
                "short_term_lacks__product",
                "subsidy",
                "subsidy__applies",
                "subsidy__refuses",
                "subsidy__applies__result",
                "subsidy__refuses__reason",
            )
        )
        self.age_scopes = AgeScope.objects.filter(group=1).order_by("id").all()
        self.surveys = self.surveys.filter(
            reduce(operator.and_, [Q(**filters), ~Q(**excludes)])
        )
        # Limit the output for performance test purpose.
        if limit:
            self.surveys = self.surveys[:limit]

    def export_generator(self):
        errors = []
        yield tuple(FIELDS)
        for survey in self.surveys:
            try:
                yield from SurveyExportor(self.age_scopes, survey)()
            except Exception:
                errors.append((survey.farmer_id, survey.page))
        if errors:
            yield "未匯出成功的調查表："
            yield from errors


class Row(OrderedDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Pre-populate keys based on FIELDS
        for key in range(len(FIELDS)):
            self.setdefault(key, "")

        # Update the Row instance with the passed values
        self.update(OrderedDict(sorted(self.items())))


class ReportBlock:
    def __init__(self, generator, start_col, end_col, silence=False):
        self.generator = generator
        self.start_col = start_col
        self.end_col = end_col
        self.silence = silence
        self.is_exhausted = self.silence

    def write(self, row: Row):
        if not self.silence and not self.is_exhausted:
            try:
                # Get values and set to column
                fields = next(self.generator)
                for i in range(self.end_col, self.start_col - 1, -1):
                    # Parse the different values here
                    current = fields.pop()
                    if current is None:
                        current = ""
                    elif isinstance(current, bool):
                        current = "1" if current else "0"
                    elif isinstance(current, Enum):
                        current = current.value
                    row[i] = current
            except StopIteration:
                self.is_exhausted = True
                # Just do nothing.
                pass


class SurveyExportor:
    def __init__(self, age_scopes, survey):
        """Query one time and try to get all relationships to optimize."""
        self.survey = survey
        self.age_scopes = age_scopes

        self.blocks = [
            ReportBlock(
                generator=self.survey_info_generate(),
                start_col=0,
                end_col=8,
                silence=self.survey.page > 1,
            ),
            ReportBlock(
                generator=self.normal_relation_generate(
                    "land_areas", ["type__name", "status__name", "value"]
                ),
                start_col=9,
                end_col=11,
                silence=self.survey.page > 1,
            ),
            ReportBlock(
                generator=self.normal_relation_generate(
                    "businesses", ["farm_related_business__name", "extra"]
                ),
                start_col=12,
                end_col=13,
                silence=self.survey.page > 1,
            ),
            ReportBlock(
                generator=self.normal_relation_generate("management_types", ["name"]),
                start_col=14,
                end_col=14,
                silence=self.survey.page > 1,
            ),
            ReportBlock(
                generator=self.normal_relation_generate(
                    "crop_marketings",
                    [
                        "product__code",
                        "name",
                        "land_number",
                        "land_area",
                        "plant_times",
                        "unit__name",
                        "year_sales",
                        "has_facility",
                        "loss__name",
                    ],
                ),
                start_col=15,
                end_col=23,
                silence=False,
            ),
            ReportBlock(
                generator=self.normal_relation_generate(
                    "livestock_marketings",
                    [
                        "product__code",
                        "name",
                        "unit__name",
                        "raising_number",
                        "year_sales",
                        "contract__name",
                        "loss__name",
                    ],
                ),
                start_col=24,
                end_col=30,
                silence=False,
            ),
            ReportBlock(
                generator=self.normal_relation_generate(
                    "annual_incomes", ["market_type__name", "income_range__name"]
                ),
                start_col=31,
                end_col=32,
                silence=self.survey.page > 1,
            ),
            ReportBlock(
                generator=self.main_income_source_generate(),
                start_col=33,
                end_col=33,
                silence=self.survey.page > 1,
            ),
            ReportBlock(
                generator=self.normal_relation_generate(
                    "population_ages",
                    [
                        "age_scope__name",
                        "gender__name",
                        "count",
                    ],
                ),
                start_col=34,
                end_col=36,
                silence=self.survey.page > 1,
            ),
            ReportBlock(
                generator=self.normal_relation_generate(
                    "populations",
                    [
                        "relationship__name",
                        "gender__name",
                        "birth_year",
                        "education_level__name",
                        "farmer_work_day",
                        "life_style__name",
                    ],
                ),
                start_col=37,
                end_col=42,
                silence=False,
            ),
            ReportBlock(
                generator=self.hire_generate(),
                start_col=43,
                end_col=43,
                silence=self.survey.page > 1,
            ),
            ReportBlock(
                generator=self.long_term_hires_generate(),
                start_col=44,
                end_col=50,
                silence=False,
            ),
            ReportBlock(
                generator=self.short_term_hires_generate(),
                start_col=51,
                end_col=57,
                silence=False,
            ),
            ReportBlock(
                generator=self.normal_relation_generate(
                    "no_salary_hires", ["month__value", "count", "avg_work_day"]
                ),
                start_col=58,
                end_col=60,
                silence=False,
            ),
            ReportBlock(
                generator=self.normal_relation_generate("lacks", ["name"]),
                start_col=61,
                end_col=61,
                silence=self.survey.page > 1,
            ),
            ReportBlock(
                generator=self.long_term_lacks_generate(),
                start_col=62,
                end_col=65,
                silence=False,
            ),
            ReportBlock(
                generator=self.short_term_lacks_generate(),
                start_col=66,
                end_col=71,
                silence=False,
            ),
            ReportBlock(
                # Use built in filter to prevent query.
                generator=self.subsidy_info_generate(method_id=1),
                start_col=72,
                end_col=73,
                silence=self.survey.page > 1,
            ),
            ReportBlock(
                generator=self.applies_generate(method_id=1),
                start_col=74,
                end_col=74,
                silence=self.survey.page > 1,
            ),
            ReportBlock(
                generator=self.refuses_generate(method_id=1),
                start_col=75,
                end_col=75,
                silence=self.survey.page > 1,
            ),
            ReportBlock(
                # Use built in filter to prevent query.
                generator=self.subsidy_info_generate(method_id=2),
                start_col=76,
                end_col=77,
                silence=self.survey.page > 1,
            ),
            ReportBlock(
                generator=self.applies_generate(method_id=2),
                start_col=78,
                end_col=78,
                silence=self.survey.page > 1,
            ),
            ReportBlock(
                generator=self.refuses_generate(method_id=2),
                start_col=79,
                end_col=79,
                silence=self.survey.page > 1,
            ),
            ReportBlock(
                # Use built in filter to prevent query.
                generator=self.subsidy_info_generate(method_id=3),
                start_col=80,
                end_col=81,
                silence=self.survey.page > 1,
            ),
            ReportBlock(
                generator=self.applies_generate(method_id=3),
                start_col=82,
                end_col=82,
                silence=self.survey.page > 1,
            ),
            ReportBlock(
                generator=self.refuses_generate(method_id=3),
                start_col=83,
                end_col=83,
                silence=self.survey.page > 1,
            ),
            ReportBlock(
                generator=self.reviewer_generate(),
                start_col=84,
                end_col=86,
                silence=self.survey.page > 1,
            ),
        ]

    def __call__(self, to_tuple=True):
        while not self.is_exhausted:
            row = Row()
            row[0] = self.survey.farmer_id
            for block in self.blocks:
                block.write(row=row)
            # Last row must be empty, check one more time
            if not self.is_exhausted:
                yield tuple(row.values()) if to_tuple else row

    @property
    def is_exhausted(self):
        return all(block.is_exhausted for block in self.blocks)

    def survey_info_generate(self):
        yield [
            self.survey.farmer_id,
            self.survey.farmer_name,
            self.survey.interviewee_relationship,
            self.survey.phones.first().phone,
            self.survey.phones.last().phone,
            self.survey.address_match.match,
            self.survey.address_match.address,
            self.survey.farm_location.city + self.survey.farm_location.town,
            self.survey.farm_location.code.code if self.survey.farm_location.code else "",
        ]

    def main_income_source_generate(self):
        yield ["以自家農牧業淨收入為主" if self.survey.main_income_source else "以自家農牧業外淨收入為主"]

    def hire_generate(self):
        yield ["2" if self.survey.hire else "1"]

    def reviewer_generate(self):
        yield [
            "1" if self.survey.subsidy.heard_app else "0",
            self.survey.investigator,
            self.survey.reviewer,
        ]

    def normal_relation_generate(self, relate_name, values_list):
        """Generator function simply yielding one to many relation fields and that's it."""
        for item in getattr(self.survey, relate_name).values_list(*values_list).all():
            yield list(item)

    def long_term_hires_generate(self):
        """Generator function requires complex data processing."""
        for lth in self.survey.long_term_hires.all():
            values = [
                lth.work_type.name,
                lth.avg_work_day,
                ",".join(map(str, lth.months.values_list("value", flat=True))),
            ]
            worker_list = list()
            for age_scope in self.age_scopes:
                search = lth.number_workers.filter(age_scope=age_scope).first()
                worker_list.append(search.count if search else 0)
            values.append(sum(worker_list))
            values += worker_list
            yield values

    def short_term_hires_generate(self):
        """Generator function requires complex data processing."""
        for sth in self.survey.short_term_hires.all():
            values = [
                ",".join(map(str, sth.work_types.values_list("name", flat=True))),
                sth.avg_work_day,
                sth.month.value,
            ]
            worker_list = list()
            for age_scope in self.age_scopes:
                # search => sth.number_workers.filter(age_scope=age_scope).first()
                # In order to prevent a new query, use python instead
                search = 0
                for nw in sth.number_workers.all():
                    if nw.age_scope == age_scope:
                        search = nw.count
                        break
                worker_list.append(search)
            values.append(sum(worker_list))
            values += worker_list
            yield values

    def long_term_lacks_generate(self):
        """Generator function requires complex data processing."""
        for ltl in self.survey.long_term_lacks.all():
            yield [
                ltl.work_type.name,
                ltl.count,
                ltl.avg_lack_day,
                ",".join(map(str, ltl.months.values_list("value", flat=True))),
            ]

    def short_term_lacks_generate(self):
        """Generator function requires complex data processing."""
        for obj in self.survey.short_term_lacks.all():
            yield [
                obj.work_type.name,
                obj.product.code,
                obj.name,
                obj.count,
                obj.avg_lack_day,
                ",".join(map(str, obj.months.values_list("value", flat=True))),
            ]

    def subsidy_info_generate(self, method_id):
        """Yield first and second field, e.g. 是否聽過農業外籍移工, 是否有申請農業外籍移工."""
        yield [
            "1"
            if list(
                filter(
                    lambda refuse: refuse.method == method_id and refuse.reason.id == 0,
                    self.survey.subsidy.refuses.all(),
                )
            )
            else "0",
            "1"
            if list(
                filter(
                    lambda apply: apply.method == method_id,
                    self.survey.subsidy.applies.all(),
                )
            )
            else "0",
        ]

    def applies_generate(self, method_id):
        # qs => self.survey.subsidy.applies.filter(method=method_id)
        # In order to prevent a new query, use python instead
        for apply in self.survey.subsidy.applies.all():
            if apply.method == method_id:
                yield [apply.result]

    def refuses_generate(self, method_id):
        # qs => self.survey.subsidy.refuses.filter(method=method_id)
        # In order to prevent a new query, use python instead
        for refuse in self.survey.subsidy.refuses.all():
            # reason=0 represent "not heard", already display in other fields.
            if refuse.method == method_id and refuse.reason != 0:
                yield [refuse.reason]

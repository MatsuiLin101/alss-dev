from django.test import TestCase
from django.core.management import call_command
from surveys18.builder.tokenizer_labor import Builder
from surveys18.builder.exceptions import SignError, StringLengthError, CreateModelError
from surveys18.models import (
    MarketType,
    IncomeRange,
    AnnualIncome,
    Survey,
    AddressMatch,
    Lack,
    FarmRelatedBusiness,
    Business,
    Phone,
    LandArea,
    LandType,
    LandStatus,
    Loss,
    Unit,
    Product,
    Contract,
    CropMarketing,
    LivestockMarketing,
    Facility,
    PopulationAge,
    Population,
    EducationLevel,
    FarmerWorkDay,
    LifeStyle,
    OtherFarmWork,
    Subsidy,
    RefuseReason,
    AgeScope,
    LongTermHire,
    ShortTermHire,
    WorkType,
    NumberWorkers,
    NoSalaryHire,
    ShortTermLack,
    LongTermLack,
    Gender,
    ProductType,
    Relationship,
    Month,
    Refuse
)


class ModelTestCase(TestCase):
    def setUp(self):
        call_command('loaddata', 'unit.yaml', verbosity=0)
        call_command('loaddata', 'land-type.yaml', verbosity=0)
        call_command('loaddata', 'land-status.yaml', verbosity=0)
        call_command('loaddata', 'farm-related-business.yaml', verbosity=0)
        call_command('loaddata', 'management-type.yaml', verbosity=0)
        call_command('loaddata', 'product-type.yaml', verbosity=0)
        call_command('loaddata', 'product.yaml', verbosity=0)
        call_command('loaddata', 'loss.yaml', verbosity=0)
        call_command('loaddata', 'contract.yaml', verbosity=0)
        call_command('loaddata', 'income-range.yaml', verbosity=0)
        call_command('loaddata', 'market-type.yaml', verbosity=0)
        call_command('loaddata', 'age-scope.yaml', verbosity=0)
        call_command('loaddata', 'gender.yaml', verbosity=0)
        call_command('loaddata', 'relationship.yaml', verbosity=0)
        call_command('loaddata', 'education-level.yaml', verbosity=0)
        call_command('loaddata', 'farmer-work-day.yaml', verbosity=0)
        call_command('loaddata', 'life-style.yaml', verbosity=0)
        call_command('loaddata', 'other-farm-work.yaml', verbosity=0)
        call_command('loaddata', 'month.yaml', verbosity=0)
        call_command('loaddata', 'work-type.yaml', verbosity=0)
        call_command('loaddata', 'age-scope.yaml', verbosity=0)
        call_command('loaddata', 'lack.yaml', verbosity=0)
        call_command('loaddata', 'refuse-reason.yaml', verbosity=0)
        # self.string = "6700500100020101####林阿忠0912345678/###29911110501屏東縣屏東市屏東路2號#+00250000000003001000000000100000001農所實驗#00000000000100+A001104201100210000002321D011103001100072000007520+F00230000900000150500000F001300100000150009750031010000410020101030201+010110300200000010100000001000202203202000001001000000010001+120040020010011010000000000005220040020010011111111111111113+0100900000500412130000000000001004010001005004142100000000000285+01002070050011+2200110100000000014001111111111111+A60213002110000000000C50612001000110000000+1012120000101時間太忙#1勞工不穩定#+稻受雨害影響#005260035"
        self.string = "1000703051810101####林國仁#047353895/##########1010#+00050000000000000000000000100000000#00000100000000+C004100201100008500008323C017200201100001000007022C999300101100011000004522+0100000001020101040202+0101105708000001001000000001002022060080001000010000000100030320880510000000000000101000405102203100000000000000110010+++1000+++0000000000110#0#+１．其姊僅是同戶籍，實際上沒有共同居住。２．０１自營數學家教班，大多在晚上和假日時教學。３．所栽種之果樹種類很多，都是少株多品種，都是採自然農法方式，不噴農藥施用有機肥，略有病蟲害情形，故產量都不高。４柑橘類，如：橘子、柳丁、檸檬、桶柑、茂谷柑、帝王柑、砂糖橘等。５．芒果類，如：金煌、愛文、金蜜、四季等皆為新植（１．５至２年）且６月豪雨時落果嚴重。#000550017"
        self.builder = Builder(self.string)
        self.builder.build_survey()

    # def test_check_string(self):
    #     check_string = Builder.check_string(self.string)
    #     self.assertTrue(check_string)
    #     print(check_string)

    def test_build_survey(self):
        self.assertEquals(self.builder.survey.farmer_id, "100070305181")
        self.assertEquals(self.builder.survey.page, 1)
        self.assertEquals(self.builder.survey.total_pages, 1)
        self.assertEquals(self.builder.survey.farmer_name, "林國仁")
        self.assertEquals(self.builder.survey.origin_class, 10)
        # self.assertEquals(self.builder.survey.note, "")
        self.assertEquals(self.builder.survey.period, 55)
        self.assertEquals(self.builder.survey.distance, 17)

        # check survey query string


    def test_build_phone(self):
        self.builder.build_phone()
        self.assertEquals(self.builder.phones[0].phone, "047353895")
        # self.assertEquals(self.builder.phones[1].phone, "2991111")

    def test_build_address(self):
        self.builder.build_address()
        self.assertEquals(self.builder.address.match, True)
        self.assertEquals(self.builder.address.mismatch, False)
        self.assertEquals(self.builder.address.address, "")

    def test_build_land_area(self):
        self.builder.build_land_area()
        # self.assertEquals(len(self.builder.land_area),3)
        #
        # land_type_a = LandType.objects.get(id=1)
        # land_status_a = LandStatus.objects.get(id=1)
        # self.assertEquals(self.builder.land_area[0].value, 250 )
        # self.assertEquals(self.builder.land_area[0].type, land_type_a)
        # self.assertEquals(self.builder.land_area[0].status, land_status_a)
        #
        # land_type_b = LandType.objects.get(id=1)
        # land_status_b = LandStatus.objects.get(id=3)
        # self.assertEquals(self.builder.land_area[1].value, 30 )
        # self.assertEquals(self.builder.land_area[1].type, land_type_b)
        # self.assertEquals(self.builder.land_area[1].status, land_status_b)
        #
        # land_type_c = LandType.objects.get(id=2)
        # land_status_c = LandStatus.objects.get(id=1)
        # self.assertEquals(self.builder.land_area[2].value, 1000 )
        # self.assertEquals(self.builder.land_area[2].type, land_type_c)
        # self.assertEquals(self.builder.land_area[2].status, land_status_c)

    def test_build_business(self):
        self.builder.build_business()
        # self.assertEquals(len(self.builder.business), 2)
        # self.assertEquals(self.builder.business[0].farm_related_business.name, "無兼營農業相關事業")
        # self.assertEquals(self.builder.business[1].farm_related_business.name, "其他")
        # self.assertEquals(self.builder.business[1].extra, "農所實驗")

    def test_build_management(self):
        self.builder.build_management()
        # self.assertEquals(len(self.builder.survey.management_types.all()), 1)
        # self.assertEquals(self.builder.survey.management_types.all()[0].name, "豬")

    def test_build_crop_marketing(self):
        self.builder.build_crop_marketing()
        # self.assertEquals(len(self.builder.crop_marketing), 2)
        # self.assertEquals(self.builder.crop_marketing[0].product.code,"A001")
        # self.assertEquals(self.builder.crop_marketing[0].land_number, 1)
        # self.assertEquals(self.builder.crop_marketing[0].land_area, 420)
        # self.assertEquals(self.builder.crop_marketing[0].plant_times, 1)
        # self.assertEquals(self.builder.crop_marketing[0].unit.code, 1)
        # self.assertEquals(self.builder.crop_marketing[0].total_yield, 21000)
        # self.assertEquals(self.builder.crop_marketing[0].unit_price, 23)
        # self.assertEquals(self.builder.crop_marketing[0].has_facility, 0)
        # self.assertEquals(self.builder.crop_marketing[0].loss.code, 1)
        #
        # self.assertEquals(self.builder.crop_marketing[1].product.code,"D011")
        # self.assertEquals(self.builder.crop_marketing[1].land_number, 1)
        # self.assertEquals(self.builder.crop_marketing[1].land_area, 300)
        # self.assertEquals(self.builder.crop_marketing[1].plant_times, 1)
        # self.assertEquals(self.builder.crop_marketing[1].unit.code, 1)
        # self.assertEquals(self.builder.crop_marketing[1].total_yield, 7200)
        # self.assertEquals(self.builder.crop_marketing[1].unit_price, 75)
        # self.assertEquals(self.builder.crop_marketing[1].has_facility, 0)
        # self.assertEquals(self.builder.crop_marketing[1].loss.code, 0)

    def test_build_livestock_marketing(self):
        self.builder.build_livestock_marketing()
        # self.assertEquals(len(self.builder.livestock_marketing), 2)
        # self.assertEquals(self.builder.livestock_marketing[0].product.code,"F002")
        # self.assertEquals(self.builder.livestock_marketing[0].unit.code, 3)
        # self.assertEquals(self.builder.livestock_marketing[0].raising_number, 90)
        # self.assertEquals(self.builder.livestock_marketing[0].total_yield, 15)
        # self.assertEquals(self.builder.livestock_marketing[0].unit_price, 5000)
        # self.assertEquals(self.builder.livestock_marketing[0].contract.code, 0)
        # self.assertEquals(self.builder.livestock_marketing[0].loss.code, 0)
        #
        # self.assertEquals(self.builder.livestock_marketing[1].product.code,"F001")
        # self.assertEquals(self.builder.livestock_marketing[1].unit.code, 3)
        # self.assertEquals(self.builder.livestock_marketing[1].raising_number, 1000)
        # self.assertEquals(self.builder.livestock_marketing[1].total_yield, 1500)
        # self.assertEquals(self.builder.livestock_marketing[1].unit_price, 9750)
        # self.assertEquals(self.builder.livestock_marketing[1].contract.code, 0)
        # self.assertEquals(self.builder.livestock_marketing[1].loss.code, 3)
        #....種豬 頭 90 15 5000 無 無 /肉豬 頭 1000 1500 9750 無 疫病

    def test_build_annual_income(self):
        self.builder.build_annual_income()
        # self.assertEquals(len(self.builder.annual_income), 4)
        # self.assertEquals(self.builder.annual_income[0].market_type.name,"農作物及其製品(含生產及加工)")
        # self.assertEquals(self.builder.annual_income[0].income_range.name, "500以上")
        # self.assertEquals(self.builder.annual_income[1].market_type.name, "畜禽產品及其製品(含生產及加工)")
        # self.assertEquals(self.builder.annual_income[1].income_range.name, "500以上")
        # self.assertEquals(self.builder.annual_income[2].market_type.name, "休閒、餐飲及相關事業")
        # self.assertEquals(self.builder.annual_income[2].income_range.name, "75~未滿100")
        # self.assertEquals(self.builder.annual_income[3].market_type.name, "銷售額總計")
        # self.assertEquals(self.builder.annual_income[3].income_range.name, "500以上")

    def test_build_population_age(self):
        self.builder.build_population_age()
        # self.assertEquals(len(self.builder.population_age), 4)
        # self.assertEquals(self.builder.population_age[0].count,1)
        # self.assertEquals(self.builder.population_age[0].gender.name, "男")
        # self.assertEquals(self.builder.population_age[0].age_scope.name, "未滿15歲")
        # self.assertEquals(self.builder.population_age[1].count, 1)
        # self.assertEquals(self.builder.population_age[1].gender.name, "女")
        # self.assertEquals(self.builder.population_age[1].age_scope.name, "未滿15歲")
        # self.assertEquals(self.builder.population_age[2].count, 2)
        # self.assertEquals(self.builder.population_age[2].gender.name, "男")
        # self.assertEquals(self.builder.population_age[2].age_scope.name, "滿15歲以上")
        # self.assertEquals(self.builder.population_age[3].count, 1)
        # self.assertEquals(self.builder.population_age[3].gender.name, "女")
        # self.assertEquals(self.builder.population_age[3].age_scope.name, "滿15歲以上")

    def test_build_population(self):
        self.builder.build_population()
        # self.assertEquals(len(self.builder.population), 2)

    def test_build_hire(self):
        self.builder.build_hire()
        # self.assertEquals(self.builder.survey.non_hire,False)
        # self.assertEquals(self.builder.survey.hire, True)

    def test_build_long_term_hire(self):
        self.builder.build_long_term_hire()
        # self.assertEquals(len(self.builder.long_term_hire), 2)
        # self.assertEquals(len(self.builder.long_term_hire[0].number_workers.all()), 3)
        # self.assertEquals(len(self.builder.long_term_hire[0].months.all()), 2)
        # self.assertEquals(self.builder.long_term_hire[0].avg_work_day, 0.5)

    def test_build_short_term_hire(self):
        self.builder.build_short_term_hire()
        # self.assertEquals(len(self.builder.short_term_hire), 2)
        # self.assertEquals(len(self.builder.short_term_hire[0].number_workers.all()), 2)
        # self.assertEquals(self.builder.short_term_hire[0].month.value, 1)
        # self.assertEquals(self.builder.short_term_hire[0].avg_work_day,1)

    def test_build_no_salary_hire(self):
        self.builder.build_no_salary_hire()
        # self.assertEquals(len(self.builder.no_salary_hire), 2)
        # self.assertEquals(self.builder.no_salary_hire[0].month.value, 1)
        # self.assertEquals(self.builder.no_salary_hire[0].count, 2)
        # self.assertEquals(self.builder.no_salary_hire[1].month.value, 7)
        # self.assertEquals(self.builder.no_salary_hire[1].count, 5)

    def test_build_lack(self):
        self.builder.build_lack()
        # self.assertEquals(len(self.builder.survey.lacks.all()),2)

    def test_build_long_term_lack(self):
        self.builder.build_long_term_lack()

        # self.assertEquals(len(self.builder.long_term_lack),2)

    def test_build_short_term_lack(self):
        self.builder.build_short_term_lack()
        # self.assertEquals(len(self.builder.short_term_lack),2)

    def test_build_subsidy(self):
        self.builder.build_subsidy()
        # obj = Subsidy.objects.get(survey=self.builder.survey)
        # print(obj.survey)
        # print(obj.has_subsidy)
        #
        #
        # self.assertEquals(self.builder.subsidy.survey.farmer_id,"100101510450")
        # self.assertEquals(self.builder.subsidy.count, 12)
        # self.assertEquals(self.builder.subsidy.month_delta, 12)
        # self.assertEquals(self.builder.subsidy.day_delta, 0)
        # self.assertEquals(self.builder.subsidy.hour_delta, 0)
        # self.assertEquals(len(self.builder.refuse), 2)
        # print(self.builder.refuse[0].reason)
        # print(self.builder.refuse[0].extra)
        # print(self.builder.refuse[1].reason)
        # print(self.builder.refuse[1].extra)



























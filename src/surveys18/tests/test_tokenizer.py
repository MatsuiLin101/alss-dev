from django.test import TestCase
from django.core.management import call_command
from surveys18.builder.tokenizer import Builder
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
)


class ModelTestCase(TestCase):
    def setUp(self):
        call_command('loaddata', 'land-type.yaml', verbosity=0)
        call_command('loaddata', 'land-status.yaml', verbosity=0)
        call_command('loaddata', 'farm-related-business.yaml', verbosity=0)
        call_command('loaddata', 'management-type.yaml', verbosity=0)
        call_command('loaddata', 'product-type.yaml', verbosity=0)
        call_command('loaddata', 'product.yaml', verbosity=0)
        call_command('loaddata', 'loss.yaml', verbosity=0)
        call_command('loaddata', 'unit.yaml', verbosity=0)
        call_command('loaddata', 'contract.yaml', verbosity=0)
        self.string = "6700500100020101####林阿忠0912345678/###29911110501屏東縣屏東市屏東路2號#+00250000000003001000000000100000001農所實驗#00000000000100+A001104201100210000002321D011103001100072000007520+F00230000900000150500000F001300100000150009750031010000410020101030201+010110300200000010100000001000202203202000001001000000010001+1200400200100110100000000000522004002001001111111111111010+01009000005004121300000000000000401000100500414210000000000080+01002070050001+2200110100000000014001111111111111+A60213002110000000000C50612001000110000000+01212000000時間太忙#0#+稻受雨害影響#005260035"
        self.builder = Builder(self.string)
        self.builder.build_survey()

    # def test_check_string(self):
    #     check_string = Builder.check_string(self.string)
    #     self.assertTrue(check_string)
    #     print(check_string)

    def test_build_survey(self):
        self.assertEquals(self.builder.survey.farmer_id, "670050010002")
        self.assertEquals(self.builder.survey.page, 1)
        self.assertEquals(self.builder.survey.total_pages, 1)
        self.assertEquals(self.builder.survey.farmer_name, "林阿忠")
        self.assertEquals(self.builder.survey.origin_class, 5)
        self.assertEquals(self.builder.survey.note, "稻受雨害影響")
        self.assertEquals(self.builder.survey.period, 326)
        self.assertEquals(self.builder.survey.distance, 35)

        # check survey query string


    # def test_build_xxx(self):
    #     builder = Builder(self.string)
    #     self.assertRaisesMessage(NotImplementedError, self.builder.ERROR_MESSAGES['PlusSignError'])

    def test_build_phone(self):
        self.builder.build_phone()
        self.assertEquals(self.builder.phones[0].phone, "0912345678")
        self.assertEquals(self.builder.phones[1].phone, "2991111")

    def test_build_address(self):
        self.builder.build_address()
        self.assertEquals(self.builder.address.match, False)
        self.assertEquals(self.builder.address.mismatch, True)
        self.assertEquals(self.builder.address.address, "屏東縣屏東市屏東路2號")

    def test_build_land_area(self):
        self.builder.build_land_area()
        self.assertEquals(len(self.builder.land_area),3)

        land_type_a = LandType.objects.get(id=1)
        land_status_a = LandStatus.objects.get(id=1)
        self.assertEquals(self.builder.land_area[0].value, 250 )
        self.assertEquals(self.builder.land_area[0].type, land_type_a)
        self.assertEquals(self.builder.land_area[0].status, land_status_a)

        land_type_b = LandType.objects.get(id=1)
        land_status_b = LandStatus.objects.get(id=3)
        self.assertEquals(self.builder.land_area[1].value, 30 )
        self.assertEquals(self.builder.land_area[1].type, land_type_b)
        self.assertEquals(self.builder.land_area[1].status, land_status_b)

        land_type_c = LandType.objects.get(id=2)
        land_status_c = LandStatus.objects.get(id=1)
        self.assertEquals(self.builder.land_area[2].value, 1000 )
        self.assertEquals(self.builder.land_area[2].type, land_type_c)
        self.assertEquals(self.builder.land_area[2].status, land_status_c)

    def test_build_business(self):
        self.builder.build_business()
        self.assertEquals(len(self.builder.business), 2)
        self.assertEquals(self.builder.business[0].farm_related_business.name, "無兼營農業相關事業")
        self.assertEquals(self.builder.business[1].farm_related_business.name, "其他")
        self.assertEquals(self.builder.business[1].extra, "農所實驗")

    def test_build_management(self):
        self.builder.build_management()
        self.assertEquals(len(self.builder.survey.management_types.all()), 1)
        self.assertEquals(self.builder.survey.management_types.all()[0].name, "豬")

    def test_build_crop_marketing(self):
        self.builder.build_crop_marketing()
        self.assertEquals(len(self.builder.crop_marketing), 2)
        self.assertEquals(self.builder.crop_marketing[0].product.code,"A001")
        self.assertEquals(self.builder.crop_marketing[0].land_number, 1)
        self.assertEquals(self.builder.crop_marketing[0].land_area, 420)
        self.assertEquals(self.builder.crop_marketing[0].plant_times, 1)
        self.assertEquals(self.builder.crop_marketing[0].unit.code, 1)
        self.assertEquals(self.builder.crop_marketing[0].total_yield, 21000)
        self.assertEquals(self.builder.crop_marketing[0].unit_price, 23)
        self.assertEquals(self.builder.crop_marketing[0].has_facility, 0)
        self.assertEquals(self.builder.crop_marketing[0].loss.code, 1)

        self.assertEquals(self.builder.crop_marketing[1].product.code,"D011")
        self.assertEquals(self.builder.crop_marketing[1].land_number, 1)
        self.assertEquals(self.builder.crop_marketing[1].land_area, 300)
        self.assertEquals(self.builder.crop_marketing[1].plant_times, 1)
        self.assertEquals(self.builder.crop_marketing[1].unit.code, 1)
        self.assertEquals(self.builder.crop_marketing[1].total_yield, 7200)
        self.assertEquals(self.builder.crop_marketing[1].unit_price, 75)
        self.assertEquals(self.builder.crop_marketing[1].has_facility, 0)
        self.assertEquals(self.builder.crop_marketing[1].loss.code, 0)

    # def test_build_livestock_marketing(self):
    #     self.builder.build_livestock_marketing()
    #     self.assertEquals(len(self.builder.livestock_marketing), 2)



















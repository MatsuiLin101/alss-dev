from django.test import TestCase
from django.core.management import call_command
from surveys18.builder.tokenizer import Builder
from surveys18.models import (
    MarketType,
    IncomeRange,
    AnnualIncome,
    Survey,
    AddressMatch,
    Lack,
    Phone,
    LandArea,
    LandType,
    LandStatus,
    FarmRelatedBusiness,
    Business,
    Management,
    ManagementType,
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
        self.string = "6700500100020101####林阿忠0912345678/###29911110501屏東縣屏東市屏東路2號#+00250000000003001000000000100000001農所實驗#00000000000100+A001104201100210000002321D011103001100072000007520+F00230000900000150500000F001300100000150009750031010000410020101030201+010110300200000010100000001000202203202000001001000000010001+1200400200100110100000000000522004002001001111111111111010+01009000005004121300000000000000401000100500414210000000000080+01002070050001+2200110100000000014001111111111111+A60213002110000000000C50612001000110000000+01212000000時間太忙#0#+稻受雨害影響#005260035"
        self.builder = Builder(self.string)

    def test_check_string(self):
        check_string = Builder.check_string(self.string)
        self.assertTrue(check_string)

    def test_build_survey(self):
        self.builder.build_survey()
        self.assertEquals(self.builder.survey.farmer_id, "670050010002")
        self.assertEquals(self.builder.survey.page, 1)
        self.assertEquals(self.builder.survey.total_pages, 1)
        self.assertEquals(self.builder.survey.farmer_name, "林阿忠")
        self.assertEquals(self.builder.survey.origin_class, 5)
        self.assertEquals(self.builder.survey.note, "稻受雨害影響")
        self.assertEquals(self.builder.survey.period, 326)
        self.assertEquals(self.builder.survey.distance, 35)

        # check survey query string


    def test_build_xxx(self):
        builder = Builder(self.string)
        self.assertRaisesMessage(NotImplementedError, self.builder.ERROR_MESSAGES['PlusSignError'])



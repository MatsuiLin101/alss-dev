from django.test import TestCase
from django.core.management import call_command
from surveys18.builder.tokenizer_specialty import Builder
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
        call_command('loaddata', 'land-type.yaml', verbosity=0)
        call_command('loaddata', 'land-status.yaml', verbosity=0)
        call_command('loaddata', 'farm-related-business.yaml', verbosity=0)
        call_command('loaddata', 'management-type.yaml', verbosity=0)
        call_command('loaddata', 'product-type.yaml', verbosity=0)
        call_command('loaddata', 'product.yaml', verbosity=0)
        call_command('loaddata', 'loss.yaml', verbosity=0)
        call_command('loaddata', 'unit.yaml', verbosity=0)
        call_command('loaddata', 'contract.yaml', verbosity=0)
        call_command('loaddata', 'income-range.yaml', verbosity=0)
        call_command('loaddata', 'market-type.yaml', verbosity=0)
        call_command('loaddata', 'age-scope.yaml', verbosity=0)
        call_command('loaddata', 'gender.yaml', verbosity=0)
        call_command('loaddata', 'relationship.yaml', verbosity=0)
        call_command('loaddata', 'education-level.yaml', verbosity=0)
        call_command('loaddata', 'farmer-work-day.yaml', verbosity=0)
        call_command('loaddata', 'age-scope.yaml', verbosity=0)
        self.string = "2,106,660150001851,1,4,,5,趙信忠　　,0929963700 , ,臺中市后里區墩東里９鄰平安路１２之１號,,40,40,0,0,0,0,1,B021,甘藍(高麗菜),1   ,40,1,1,7500,10,2,,0,,,,,,,,,,,0,0,0,0,0,0,0,0,0,,1,1,1,04400 ,3,5,4. 蔬菜"
        self.builder = Builder(self.string)
        self.builder.build_survey()


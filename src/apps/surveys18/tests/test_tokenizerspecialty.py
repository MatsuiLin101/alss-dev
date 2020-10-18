from . import TestCase, setup_fixtures
from apps.surveys18.builder.tokenizer_specialty import Builder

from apps.surveys18.models import (
    Survey,
    AddressMatch,
    Business,
    Phone,
    LandArea,
    CropMarketing,
    LivestockMarketing,
    Population,
)


class ModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup_fixtures()

    def setUp(self):

        self.string = "279,106,100091101020,1,3,,2,廖見興　　,0912308329 ,55989438 ,否,雲林縣二崙鄉楊賢村８鄰楊賢路５４號,,0,360,0,0,0,0,1,A001,蓬萊米(梗稻)1期,1   ,300,1,1,28800,17,2,,1,,,,,,,,,,,0, , , , , , ,, ,,1,1,1,05500 ,4,6,1. 稻作"

        self.builder = Builder(self.string)
        self.builder.build_survey()

    def test_build_survey(self):
        obj = Survey.objects.get(farmer_id=self.builder.survey.farmer_id)
        self.assertEqual(obj.farmer_id, "100091101020")
        self.assertEqual(obj.page, 1)
        self.assertEqual(obj.total_pages, 1)
        self.assertEqual(obj.farmer_name, "廖見興")

    def test_build_phone(self):
        self.builder.build_phone()
        phones = Phone.objects.filter(survey=self.builder.survey).order_by('id').all()

        self.assertEqual(phones[0].phone, "0912308329")
        self.assertEqual(phones[1].phone, "55989438")

    def test_build_address(self):
        self.builder.build_address()
        obj = AddressMatch.objects.get(survey=self.builder.survey)
        self.assertEqual(obj.match, False)
        self.assertEqual(obj.mismatch, True)
        # self.assertEqual(obj.address, "雲林縣二崙鄉楊賢村８鄰楊賢路５４號")

    def test_build_land_area(self):
        self.builder.build_land_area()
        obj = LandArea.objects.filter(survey=self.builder.survey).all()
        self.assertEqual(len(obj), 1)
        # print(obj[0].type, obj[0].status, obj[0].value)

        # self.assertEqual(obj[0].type.id, 1)
        # self.assertEqual(obj[0].status.id, 1)
        # self.assertEqual(obj[0].value, 100)

        # self.assertEqual(obj[1].type.id, 1)
        # self.assertEqual(obj[1].status.id, 2)
        # self.assertEqual(obj[1].value, 40)

    def test_build_business(self):
        self.builder.build_business()
        obj = Business.objects.filter(survey=self.builder.survey).all()
        self.assertEqual(len(obj), 1)
        self.assertEqual(obj[0].farm_related_business.code, 1)
        # self.assertEqual(obj[0].extra, "123")

    def test_build_management(self):
        self.builder.build_management()
        obj = Survey.objects.filter(farmer_id=self.builder.survey.farmer_id).all()
        self.assertEqual(len(obj), 1)
        m_obj = obj[0].management_types.all()
        self.assertEqual(m_obj[0].code, 1)

    def test_build_crop_marketing(self):
        self.builder.build_crop_marketing()
        obj = CropMarketing.objects.filter(survey=self.builder.survey).all()
        self.assertEqual(len(obj), 1)
        self.assertEqual(obj[0].product.code, "A001")
        self.assertEqual(obj[0].land_number, 1)
        self.assertEqual(obj[0].land_area, 300)
        self.assertEqual(obj[0].plant_times, 1)
        self.assertEqual(obj[0].unit.name, "公斤")
        self.assertEqual(obj[0].total_yield, 28800)
        self.assertEqual(obj[0].unit_price, 17)
        self.assertEqual(obj[0].has_facility, 0)
        self.assertEqual(obj[0].loss.name, "災害")

    def test_build_livestock_marketing(self):
        self.builder.build_livestock_marketing()
        obj = LivestockMarketing.objects.filter(survey=self.builder.survey).all()
        self.assertEqual(len(obj), 0)

    def test_build_population(self):
        self.builder.build_population()
        obj = Population.objects.filter(survey=self.builder.survey).all()
        self.assertEqual(len(obj), 1)
        self.assertEqual(obj[0].relationship.code, 1)
        self.assertEqual(obj[0].gender.code, 1)
        self.assertEqual(obj[0].birth_year, 55)
        self.assertEqual(obj[0].education_level.code, 4)
        self.assertEqual(obj[0].farmer_work_day.code, 7)

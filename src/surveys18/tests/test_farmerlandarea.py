from django.test import TestCase
from django.core.management import call_command
from surveys18.models import Survey, FarmerLandArea, FarmerLandType


class ModelTestCase(TestCase):
    """
    models: FarmerLandArea, Survey
    reference models : farmer-land-type.yaml
    data: farmerlandarea.yaml, survey.yaml
    main: FarmerLandArea associate other models, the one farmer has many land types.
    """

    def setUp(self):
        # load fixtures
        call_command('loaddata', 'test/survey.yaml', verbosity=0)
        call_command('loaddata', 'farmer-land-type.yaml', verbosity=0)
        call_command('loaddata', 'test/farmerlandarea.yaml', verbosity=0)


    def test_loaddata(self):
        survey_list = Survey.objects.all()
        self.assertEquals(len(survey_list), 3)

        farmer_land_area_list = FarmerLandArea.objects.all()
        self.assertEquals(len(farmer_land_area_list), 2)

        farmer_land_type_list = FarmerLandType.objects.all()
        self.assertEquals(len(farmer_land_type_list), 6)

    def test_create_land_area(self):
        survey_id = Survey.objects.get(id=3)
        farmer_land_type_a = FarmerLandType.objects.get(id=2)

        farmer_land_area_list_before_size = len(FarmerLandArea.objects.all())

        #new value
        FarmerLandArea.objects.create(survey=survey_id, type=farmer_land_type_a, value=70)

        farmer_land_area_list_after_size = len(FarmerLandArea.objects.all())
        self.assertEquals(farmer_land_area_list_after_size, farmer_land_area_list_before_size+1)

    def test_survey_delete(self):
        Survey.objects.filter(id=1).delete()
        farmer_land_area_list = FarmerLandArea.objects.filter(survey__id=1)
        self.assertEquals(farmer_land_area_list.count(), 0)

    def test_survey_delete_all(self):
        farmer_land_types_list_before_size = len(FarmerLandType.objects.all())
        Survey.objects.all().delete()
        farmer_land_area_list = FarmerLandArea.objects.all()
        farmer_land_types_list_after_size = len(FarmerLandType.objects.all())

        self.assertEquals(len(farmer_land_area_list), 0)
        self.assertEquals(farmer_land_types_list_after_size, farmer_land_types_list_before_size)


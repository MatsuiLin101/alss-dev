from django.test import TestCase
from django.core.management import call_command
from basefarmers.models import BaseFarmer, FarmerLandArea, FarmerLandType

class ModelTestCase(TestCase):
    """
    models: FarmerLandArea, BaseFarmer
    reference models : FarmerLandType
    data: farmerlandarea.yaml, basefarmer.yaml
    main: FarmerLandArea associate other models, the one farmer has different FarmerLandType.
    """

    def setUp(self):
        # load fixtures
        call_command('loaddata', 'test/basefarmer.yaml', verbosity=0)
        call_command('loaddata', 'test/farmerlandarea.yaml', verbosity=0)

    def test_loaddata(self):
        basefarmer_list = BaseFarmer.objects.all()
        self.assertEquals(len(basefarmer_list), 3)

        farmer_landtype_list = FarmerLandType.objects.all()
        self.assertEquals(len(farmer_landtype_list), 6)

        landarea_list = FarmerLandArea.objects.all()
        self.assertEquals(len(landarea_list), 2)

    def test_create_landarea(self):
        basefarmer_id = BaseFarmer.objects.get(id=3)
        farmer_landtype = FarmerLandType.objects.get(id=26)

        landarea_list_before_size = len(FarmerLandArea.objects.all())

        #new value
        FarmerLandArea.objects.create(basefarmer=basefarmer_id, farmer_land_type=farmer_landtype)

        landarea_list_after_size = len(FarmerLandArea.objects.all())
        self.assertEquals(landarea_list_after_size, landarea_list_before_size+1)

    def test_basefarmer_delete(self):
        BaseFarmer.objects.filter(id=1).delete()
        landarea_list = FarmerLandArea.objects.filter(basefarmer__id=1)
        self.assertEquals(landarea_list.count(), 0)

    def test_basefarmer_delete_all(self):
        farmer_landtype_list_before_size = len(FarmerLandType.objects.all())
        BaseFarmer.objects.all().delete()
        landarea_list = FarmerLandArea.objects.all()
        farmer_landtype_list_after_size = len(FarmerLandType.objects.all())

        self.assertEquals(len(landarea_list), 0)
        self.assertEquals(farmer_landtype_list_before_size, farmer_landtype_list_after_size)

    def test_relatedbusiness_delete(self):
        FarmerLandType.objects.filter(id=24).delete()
        landtype_landarea_list = FarmerLandArea.objects.all().filter(farmer_land_type__id=24)
        self.assertEquals(landtype_landarea_list.count(), 0)




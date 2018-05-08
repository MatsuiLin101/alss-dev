from django.test import TestCase
from django.core.management import call_command
from basefarmers.models import BaseFarmer, Business, FarmRelatedBusiness


class ModelTestCase(TestCase):
    """
    models: Business, BaseFarmer
    reference models : FarmRelatedBusiness
    data: business.yaml, basefarmer.yaml
    main: Busniess associate other models, the one farmer has many businesses.
    """

    def setUp(self):
        # load fixtures
        call_command('loaddata', 'test/basefarmer.yaml', verbosity=0)
        call_command('loaddata', 'test/business.yaml', verbosity=0)

    def test_loaddata(self):
        basefarmer_list = BaseFarmer.objects.all()
        self.assertEquals(len(basefarmer_list), 3)

        business_list = Business.objects.all()
        self.assertEquals(len(business_list), 2)

    def test_create_business(self):
        basefarmer_id = BaseFarmer.objects.get(id=3)
        relatedbusiness_a = FarmRelatedBusiness.objects.get(id=11)
        relatedbusiness_b = FarmRelatedBusiness.objects.get(id=12)

        business_list_before_size = len(Business.objects.all())

        #new value
        Business.objects.create(basefarmer=basefarmer_id)
        new_business = Business.objects.get(basefarmer=basefarmer_id)
        new_business.farm_related_business.add(relatedbusiness_a, relatedbusiness_b)
        new_business.save()

        business_list_after_size = len(Business.objects.all())
        self.assertEquals(business_list_after_size, business_list_before_size+1)

    def test_basefarmer_delete(self):
        BaseFarmer.objects.filter(id=1).delete()
        business_list = Business.objects.filter(basefarmer__id=1)
        self.assertEquals(business_list.count(), 0)

    def test_basefarmer_delete_all(self):
        relatedbusiness_list_before = FarmRelatedBusiness.objects.all()
        BaseFarmer.objects.all().delete()
        business_list = Business.objects.all()
        relatedbusiness_list_after = FarmRelatedBusiness.objects.all()

        self.assertEquals(len(business_list), 0)
        self.assertEquals(len(relatedbusiness_list_before), len(relatedbusiness_list_after))

    def test_relatedbusiness_delete(self):
        FarmRelatedBusiness.objects.filter(id=11).delete()
        business_to_relatedbusiness_list = Business.objects.all().filter(farm_related_business__id=11)
        self.assertEquals(business_to_relatedbusiness_list.count(), 0)




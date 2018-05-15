from django.test import TestCase
from django.core.management import call_command
from basefarmers.models import BaseFarmer, Population, FarmerWorkDay, OtherFarmWorkCode, RelationshipCode, EducationLevelCode, LifeStyleCode

class ModelTestCase(TestCase):
    """
    models: Population, BaseFarmer
    reference models : FarmerWorkDay, OtherFarmWorkCode, RelationshipCode, EducationLevelCode, LifeStyleCode
    data: population.yaml, basefarmer.yaml
    main: Population associate other models, the one farmer has many population.
    """
def setUp(self):
    # load fixtures
    call_command('loaddata', 'test/basefarmer.yaml', verbosity=0)
    call_command('loaddata', 'test/population.yaml', verbosity=0)
    call_command('loaddata', 'test/education-level-code.yaml', verbosity=0)
    call_command('loaddata', 'test/farmer-work-day.yaml', verbosity=0)
    call_command('loaddata', 'test/life-style-code.yaml', verbosity=0)
    call_command('loaddata', 'test/other-farm-work-code.yaml', verbosity=0)
    call_command('loaddata', 'test/relationship-code.yaml', verbosity=0)

def test_loaddata(self):
    basefarmer_list = BaseFarmer.objects.all()
    self.assertEquals(len(basefarmer_list), 3)

    population_list = Population.objects.all()
    self.assertEquals(len(population_list), 4)

def test_create_population(self):
    basefarmer_id = BaseFarmer.objects.get(id=3)
    relationship_code = RelationshipCode.objects.get(id=201)
    education_level_code = EducationLevelCode.objects.get(id=163)
    farmer_work_day = FarmerWorkDay.objects.get(id=242)
    life_style_code = LifeStyleCode.objects.get(id=184)
    other_farm_work_code = OtherFarmWorkCode.objects.get(id=222)

    population_list_before_size = len(Population.objects.all())

    #new value
    Population.objects.create(basefarmer=basefarmer_id, relationship_code=relationship_code, sex='男', birth_year=52, education_level_code=education_level_code, farmer_work_day=farmer_work_day, life_style_code=life_style_code, other_farm_work_code=other_farm_work_code)

    population_list_after_size = len(Population.objects.all())
    self.assertEquals(population_list_before_size, population_list_after_size+1)

def test_basefarmer_delete(self):
    BaseFarmer.objects.filter(id=1).delete()
    population_list = Population.objects.filter(basefarmer__id=1)
    self.assertEquals(population_list.count(), 0)

def test_basefarmer_delete_all(self):
    farmer_work_day_list_before_size = len(FarmerWorkDay.objects.all())
    BaseFarmer.objects.all().delete()
    population_list = Population.objects.all()
    farmer_work_day_list_after_size = len(FarmerWorkDay.objects.all())

    self.assertEquals(len(population_list), 0)
    self.assertEquals(farmer_work_day_list_before_size, farmer_work_day_list_after_size)

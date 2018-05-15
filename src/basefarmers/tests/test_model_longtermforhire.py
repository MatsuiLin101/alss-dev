from django.test import TestCase
from django.core.management import call_command
from basefarmers.models import BaseFarmer, LongTermForHire, WorkTypeCode

class ModelTestCase(TestCase):
    """
    models: LongTermForHire, BaseFarmer
    reference models : WorkTypeCode
    data: longtermforhire.yaml, basefarmer.yaml, work-type-code.yaml
    main: LongTermForHire associate other models, the one farmer has many employee.
    """

def setUp(self):
    # load fixtures
    call_command('loaddata', 'test/basefarmer.yaml', verbosity=0)
    call_command('loaddata', 'test/population.yaml', verbosity=0)
    call_command('loaddata', 'test/work-type-code.yaml', verbosity=0)


def test_loaddata(self):
    basefarmer_list = BaseFarmer.objects.all()
    self.assertEquals(len(basefarmer_list), 3)

    longtermforhire_list = LongTermForHire.objects.all()
    self.assertEquals(len(longtermforhire_list), 3)

def test_create_longtermforhire(self):
    basefarmer_id = BaseFarmer.objects.get(id=3)
    work_type_code = WorkTypeCode.objects.get(id=785)

    longtermforhire_list_before_size = len(LongTermForHire.objects.all())

    #new value
    LongTermForHire.objects.create(basefarmer=basefarmer_id, work_type_code=work_type_code, work_unit_day=30)

    longtermforhire_list_after_size = len(LongTermForHire.objects.all())
    self.assertEquals(longtermforhire_list_before_size, longtermforhire_list_after_size+1)

def test_basefarmer_delete(self):
    BaseFarmer.objects.filter(id=1).delete()
    longtermforhire_list = LongTermForHire.objects.filter(basefarmer__id=1)
    self.assertEquals(population_list.count(), 0)

def test_basefarmer_delete_all(self):
    work_type_code_list_before_size = len(WorkTypeCode.objects.all())
    BaseFarmer.objects.all().delete()
    longtermforhire_list = LongTermForHire.objects.all()
    work_type_code_list_after_size = len(WorkTypeCode.objects.all())

    self.assertEquals(len(population_list), 0)
    self.assertEquals(work_type_code_list_before_size, work_type_code_list_after_size)

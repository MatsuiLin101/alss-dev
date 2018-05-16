from django.test import TestCase
from django.core.management import call_command
from basefarmers.models import BaseFarmer, ShortTermForHire

class ModelTestCase(TestCase):
    """
    models: ShortTermForHire, BaseFarmer
    reference models :
    data: shorttermforhire.yaml, basefarmer.yaml, work-type-code.yaml
    main: ShortTermForHire associate other models, the one farmer has many employee.
    """

def setUp(self):
    # load fixtures
    call_command('loaddata', 'test/basefarmer.yaml', verbosity=0)
    call_command('loaddata', 'test/shorttermforhire.yaml', verbosity=0)

def test_loaddata(self):
    basefarmer_list = BaseFarmer.objects.all()
    self.assertEquals(len(basefarmer_list), 3)

    shorttermforhire_list = ShortTermForHire.objects.all()
    self.assertEquals(len(shorttermforhire_list), 5)

def test_create_population(self):
    basefarmer_id = BaseFarmer.objects.get(id=3)

    shorttermforhire_list_before_size = len(ShortTermForHire.objects.all())

    #new value
    ShortTermForHire.objects.create(basefarmer=basefarmer_id, work_unit_day=20, month=7)

    shorttermforhire_list_after_size = len(ShortTermForHire.objects.all())
    self.assertEquals(shorttermforhire_list_before_size, shorttermforhire_list_after_size+1)

def test_basefarmer_delete(self):
    BaseFarmer.objects.filter(id=1).delete()
    shorttermforhire_list = ShortTermForHire.objects.filter(basefarmer__id=1)
    self.assertEquals(shorttermforhire_list.count(), 0)

def test_basefarmer_delete_all(self):
    BaseFarmer.objects.all().delete()
    shorttermforhire_list = ShortTermForHire.objects.all()

    self.assertEquals(len(shorttermforhire_list), 0)

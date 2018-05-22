from django.test import TestCase
from django.core.management import call_command
from surveys18.models import Survey, ShortTermHire, WorkType, Month

class ModelTestCase(TestCase):
    """
    models: Survey, ShortTermHire
    reference models :
    data: shorttermhire.yaml, survey.yaml, work-type.yaml, month.yaml
    main: ShortTermHire associate other models, the one farmer has many employee.
    """

    def setUp(self):
        # load fixtures
        call_command('loaddata', 'test/survey.yaml', verbosity=0)
        call_command('loaddata', 'work-type.yaml', verbosity=0)
        call_command('loaddata', 'month.yaml', verbosity=0)
        call_command('loaddata', 'test/shorttermhire.yaml', verbosity=0)

    def test_loaddata(self):
        survey_list = Survey.objects.all()
        self.assertEquals(len(survey_list), 3)

        shorttermhire_list = ShortTermHire.objects.all()
        print(len(shorttermhire_list))
        self.assertEquals(len(shorttermhire_list), 5)

    # def test_create_population(self):
    #     survey_id = Survey.objects.get(id=3)
    #
    #     shorttermhire_list_before_size = len(ShortTermHire.objects.all())
    #
    #     #new value
    #     ShortTermHire.objects.create(survey=survey_id, avg_work_day=20, month=7, work_types=4)
    #
    #     shorttermhire_list_after_size = len(ShortTermHire.objects.all())
    #     self.assertEquals(shorttermhire_list_after_size, shorttermhire_list_before_size+1)
    #
    # def test_survey_delete(self):
    #     Survey.objects.filter(id=1).delete()
    #     shorttermhire_list = ShortTermHire.objects.filter(survey=1)
    #     self.assertEquals(shorttermhire_list.count(), 0)
    #
    # def test_survey_delete_all(self):
    #     month_list_before_size = len(Month.objects.all())
    #     Survey.objects.all().delete()
    #     shorttermhire_list = ShortTermHire.objects.all()
    #     month_list_after_size = len(Month.objects.all())
    #
    #     self.assertEquals(len(shorttermhire_list), 0)
    #     self.assertEquals(month_list_before_size, month_list_after_size)

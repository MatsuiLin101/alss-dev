from django.test import TestCase
from django.core.management import call_command
from basefarmers.models import BaseFarmer, AnnualIncome, MarketType, IncomeRangeCode


class ModelTestCase(TestCase):
    """
    models: AnnualIncome, BaseFarmer
    reference models : IncomeRangeCode, MarketType
    data: annualincome.yaml, basefarmer.yaml
    main: AnnualIncome associate other models, the one farmer has many income.
    """

    def setUp(self):
        # load fixtures
        call_command('loaddata', 'test/basefarmer.yaml', verbosity=0)
        call_command('loaddata', 'test/annualincome.yaml', verbosity=0)

    def test_loaddata(self):
        basefarmer_list = BaseFarmer.objects.all()
        self.assertEquals(len(basefarmer_list), 3)

        annualincome_list = AnnualIncome.objects.all()
        self.assertEquals(len(annualincome_list), 2)

    def test_create_annualincome(self):
        basefarmer_id = BaseFarmer.objects.get(id=2)
        incomerangecode_a = IncomeRangeCode.objects.get(id=62)
        markettype_a = MarketType.objects.get(id=63)

        annualincome_list_before_size = len(AnnualIncome.objects.all())

        #new value
        AnnualIncome.objects.create(basefarmer=basefarmer_id, market_type=markettype_a, income_range_code=incomerangecode_a)

        annualincome_list_after_size = len(AnnualIncome.objects.all())
        self.assertEquals(annualincome_list_after_size, annualincome_list_before_size+1)

    def test_basefarmer_delete(self):
        BaseFarmer.objects.filter(id=1).delete()
        annualincome_list = AnnualIncome.objects.filter(basefarmer__id=1)
        self.assertEquals(annualincome_list.count(), 0)

    def test_basefarmer_delete_all(self):
        incomerangecode_list_before = IncomeRangeCode.objects.all()
        markettype_list_before = MarketType.objects.all()
        BaseFarmer.objects.all().delete()
        annualincome_list = AnnualIncome.objects.all()
        incomerangecode_list_after = IncomeRangeCode.objects.all()
        markettype_list_after = MarketType.objects.all()

        self.assertEquals(len(annualincome_list), 0)
        self.assertEquals(len(incomerangecode_list_before), len(incomerangecode_list_after))
        self.assertEquals(len(markettype_list_before), len(markettype_list_after))

    def test_markettype_delete(self):
        MarketType.objects.filter(id=64).delete()
        annualincome_to_markettype_list = AnnualIncome.objects.all().filter(market_type=64)
        self.assertEquals(annualincome_to_markettype_list.count(), 0)

    def test_incomerangecode_delete(self):
        IncomeRangeCode.objects.filter(id=62).delete()
        annualincome_to_incomerangecode_list = AnnualIncome.objects.all().filter(income_range_code=62)
        self.assertEquals(annualincome_to_incomerangecode_list.count(), 0)

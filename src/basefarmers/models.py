from django.db import models

# Create your models here.
from django.utils.translation import ugettext_lazy as _
#from model_utils.managers import InheritanceManager
from django.db.models import (
    Model,
    QuerySet,
    SET_NULL,
    CharField,
    DateTimeField,
    ForeignKey,
    ManyToManyField,
    IntegerField,
    BooleanField,
    TextField,
    DateField,
    Q
)
'''
class AbstractProduct(Model):
    name = CharField(max_length=50, verbose_name=_('Name'))
    code = CharField(max_length=50, verbose_name=_('Code'))
    config = ForeignKey('configs.Config', null=True, on_delete=SET_NULL, verbose_name=_('Config'))
    type = ForeignKey('configs.Type', null=True, on_delete=SET_NULL, verbose_name=_('Type'))
    parent = ForeignKey('self', null=True, blank=True, on_delete=SET_NULL, verbose_name=_('Parent'))
    track_item = BooleanField(default=True, verbose_name=_('Track Item'))
    update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))

    objects = InheritanceManager()

    class Meta:
        verbose_name = _('Abstract Product')
        verbose_name_plural = _('Abstract Products')

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)

    def children(self):
        return AbstractProduct.objects.filter(parent=self).select_subclasses()

    def children_all(self):
        return AbstractProduct.objects.filter(
            Q(parent=self) | Q(parent__parent=self) | Q(parent__parent__parent=self)
        ).select_subclasses()

    @property
    def has_child(self):
        if self.children().count() > 0:
            return True
        else:
            return False

    def types(self):
        if self.children():
            type_dics = self.children_all().values('type').distinct()
            type_ids = [d['type'] for d in type_dics]
            return Type.objects.filter(id__in=type_ids)
        elif self.type:
            return Type.objects.filter(id=self.type.id)
        else:
            return []

    def sources(self):
        return Source.objects.filter(configs__id__exact=self.config.id).filter(type=self.type)

    def unit(self):
        return self.config.unit


class Config(Model):
    name = CharField(max_length=50, unique=True, verbose_name=_('Name'))
    code = CharField(max_length=50, unique=True, null=True, verbose_name=_('Code'))
    charts = ManyToManyField('configs.Chart', blank=True, verbose_name=_('Chart'))
    unit = ForeignKey('configs.Unit', null=True, blank=True, verbose_name=_('Unit'))
    type_level = IntegerField(choices=[(1, 1), (2, 2)], default=1, verbose_name=_('Type Level'))
    update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('Config')
        verbose_name_plural = _('Configs')

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)

    def products(self):
        # Use select_subclasses() to return subclass instance
        return AbstractProduct.objects.filter(config=self).select_subclasses()

    def first_level_products(self):
        # Use select_subclasses() to return subclass instance
        return AbstractProduct.objects.filter(config=self).filter(parent=None).select_subclasses()

    def types(self):
        products_qs = self.products().values('type').distinct()
        types_ids = [p['type'] for p in products_qs]
        types_qs = Type.objects.filter(id__in=types_ids)
        return types_qs


class SourceQuerySet(QuerySet):
    """ for case like Source.objects.filter(config=config).filter_by_name(name) """
    def filter_by_name(self, name):
        if not isinstance(name, str):
            raise TypeError
        name = name.replace('台', '臺')
        return self.filter(name=name)


class Source(Model):
    name = CharField(max_length=50, verbose_name=_('Name'))
    code = CharField(max_length=50, null=True, verbose_name=_('Code'))
    configs = ManyToManyField('configs.Config', verbose_name=_('Config'))
    type = ForeignKey('configs.Type', null=True, on_delete=SET_NULL, verbose_name=_('Type'))
    update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))

    objects = SourceQuerySet.as_manager()

    class Meta:
        verbose_name = _('Source')
        verbose_name_plural = _('Sources')

    def __str__(self):
        flat = self.configs_flat
        return str(self.name) + '(%s-%s)' % (flat, self.type.name)

    def __unicode__(self):
        flat = self.configs_flat
        return str(self.name) + '(%s-%s)' % (flat, self.type.name)

    @property
    def simple_name(self):
        return self.name.replace('臺', '台')

    @property
    def configs_flat(self):
        return ','.join(config.name for config in self.configs.all())


class Type(Model):
    name = CharField(max_length=50, unique=True, verbose_name=_('Name'))
    update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('Type')
        verbose_name_plural = _('Types')

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)

    def sources(self):
        return Source.objects.filter(type=self)


class Unit(Model):
    name = CharField(max_length=50, unique=True, verbose_name=_('Unit'))
    update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)


class Chart(Model):
    name = CharField(max_length=120, unique=True, verbose_name=_('Name'))
    code = CharField(max_length=50, unique=True, null=True, verbose_name=_('Code'))
    ajax = CharField(max_length=120, null=True, blank=True, verbose_name=_('Ajax'))
    static = CharField(max_length=240, default='mychart.js', verbose_name=_('Static'))
    update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('Chart')
        verbose_name_plural = _('Charts')

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)
'''


class IncomeRangeCode(Model):
    name = CharField(max_length=50, unique=True, verbose_name=_('Name'))
    minimum = IntegerField(verbose_name=_('Minimum Income'))
    maximum = IntegerField(verbose_name=_('Maximum Income'))
    update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('IncomeRangeCode')
        verbose_name_plural = _('IncomeRangeCodes')

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)


class MarketType(Model):
    name = CharField(max_length=50, unique=True, verbose_name=_('Name'))
    update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('MarketType')
        verbose_name_plural = _('MarketTypes')

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)


class AnnualIncome(Model):
    market_type = ForeignKey('basefarmers.MarketType', verbose_name=_('Market Type'))
    income_range_code = ForeignKey('basefarmers.IncomeRangeCode', verbose_name=_('Income Range Code'))
    update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('AnnualIncome')
        verbose_name_plural = _('AnnualIncomes')

    def __str__(self):
        return '%s(%s)' % (self.market_type, self.income_range_code)

    def __unicode__(self):
        return '%s(%s)' % (self.market_type, self.income_range_code)


class BaseFarmer(Model):
    farmer_id = CharField(max_length=12, verbose_name=_('Farmer Id'))
    farmer_name = CharField(max_length=10, verbose_name=_('Farmer Name'))
    total_pages = IntegerField(verbose_name=_('Total Pages'))
    page = IntegerField(verbose_name=_('Page'))
    #is_address_match = CharField(max_length=1, null=True, blank=True, verbose_name=_('Is Address Match'))
    #address = CharField(max_length=100, null=True, blank=True, verbose_name=_('Address'))
    ori_class = IntegerField(null=True, blank=True, verbose_name=_('Original Class'))
    #is_lack = CharField(max_length=1, null=True, blank=True, verbose_name=_('Is Lack'))
    investigator_name = CharField(max_length=10, null=True, blank=True, verbose_name=_('Investigator Name'))
    investigation_time = IntegerField(null=True, blank=True, verbose_name=_('Investigation Time'))
    investigation_date = DateField(null=True, blank=True, verbose_name=_('Investigation Date'))
    investigation_distance_km = IntegerField(null=True, blank=True, verbose_name=_('Investigation Distance KM'))
    note = TextField(null=True, blank=True, verbose_name=_('Note'))

    update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))

    annual_income = ManyToManyField('basefarmers.AnnualIncome', verbose_name=_('Annual Income'))

    class Meta:
        verbose_name = _('AnnualIncome')
        verbose_name_plural = _('AnnualIncomes')

    def __str__(self):
        return '%s(%s)' % (self.market_type, self.income_range_code)

    def __unicode__(self):
        return '%s(%s)' % (self.market_type, self.income_range_code)
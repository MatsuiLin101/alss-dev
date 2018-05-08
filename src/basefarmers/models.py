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
    OneToOneField,
    ManyToManyField,
    IntegerField,
    BooleanField,
    TextField,
    DateField,
    Q
)


class BaseFarmer(Model):
    """
    read_only: Keep original data(read_only=True). Modify data(read_only=False).
    """
    farmer_id = CharField(max_length=12, verbose_name=_('Farmer Id'))
    farmer_name = CharField(null=True, blank=True, max_length=10, verbose_name=_('Farmer Name'))
    total_pages = IntegerField( verbose_name=_('Total Pages'))
    page = IntegerField( verbose_name=_('Page'))
    ori_class = IntegerField(null=True, blank=True, verbose_name=_('Original Class'))
    address = CharField(max_length=100, null=True, blank=True, verbose_name=_('Address'))
    investigator_name = CharField(max_length=10, null=True, blank=True, verbose_name=_('Investigator Name'))
    investigationp_period = IntegerField(null=True, blank=True, verbose_name=_('Investigation Period'))
    investigation_date = DateField(null=True, blank=True, verbose_name=_('Investigation Date'))
    investigation_distance_km = IntegerField(null=True, blank=True, verbose_name=_('Investigation Distance KM'))
    note = TextField(null=True, blank=True, verbose_name=_('Note'))
    read_only = BooleanField(default=True, verbose_name=_('Read Only'))
    update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))

    #annual_income = ManyToManyField('basefarmers.AnnualIncome', blank=True, verbose_name=_('Annual Income'))
    #address_match = ForeignKey('basefarmers.AddressMatch', related_name='basefarmer', null=True, blank=True, verbose_name=_('Is Address Match'))
    lack = ManyToManyField('basefarmers.Lack', blank=True, verbose_name=_('Lack'))

    class Meta:
        verbose_name = _('BaseFarmer')
        verbose_name_plural = _('BaseFarmer')

    def __str__(self):
        return self.farmer_id

    def __unicode__(self):
        return self.farmer_id


# class Loss(Model):
#     code = IntegerField(verbose_name=_('Loss Code'))
#     name = CharField(max_length=10, null=True, blank=True, verbose_name=_('Loss Name'))
#     type = CharField(max_length=20, null=True, blank=True, verbose_name=_('Loss Type'))
#     update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))
#
#     class Meta:
#         verbose_name = _('Loss')
#         verbose_name_plural = _('Loss')
#
#     def __str__(self):
#         return str(self.name)
#
#     def __unicode__(self):
#         return str(self.name)
#
#
# class Unit(Model):
#     code = IntegerField(verbose_name=_('Unit Code'))
#     name = CharField(max_length=10, null=True, blank=True, verbose_name=_('Unit Name'))
#     type = CharField(max_length=20, null=True, blank=True, verbose_name=_('Unit Type'))
#     update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))
#
#     class Meta:
#         verbose_name = _('Unit')
#         verbose_name_plural = _('Unit')
#
#     def __str__(self):
#         return str(self.name)
#
#     def __unicode__(self):
#         return str(self.name)
#
#
# class ProductCode(Model):
#     code = IntegerField(verbose_name=_('Product Code'))
#     name = CharField(max_length=50, null=True, blank=True, verbose_name=_('Product Code Name'))
#     type = CharField(max_length=20, null=True, blank=True, verbose_name=_('Product Type'))
#     update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))
#
#     class Meta:
#         verbose_name = _('ProductCode')
#         verbose_name_plural = _('ProductCode')
#
#     def __str__(self):
#         return str(self.name)
#
#     def __unicode__(self):
#         return str(self.name)
#
#
# class Contract(Model):
#     code = IntegerField(verbose_name=_('Contract Code'))
#     name = CharField(max_length=10, null=True, blank=True, verbose_name=_('Contract Name'))
#     update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))
#
#     class Meta:
#         verbose_name = _('AnimalUnit')
#         verbose_name_plural = _('AnimalUnit')
#
#     def __str__(self):
#         return str(self.name)
#
#     def __unicode__(self):
#         return str(self.name)


class ManagementType(Model):
    name = CharField(max_length=50, null=True, blank=True, verbose_name=_('Management Type Name'))
    update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('ManagementType')
        verbose_name_plural = _('ManagementType')

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)


class Management(Model):
    basefarmer = OneToOneField('basefarmers.BaseFarmer', related_name='management', verbose_name=_('BaseFarmer'))
    management_type = ManyToManyField('basefarmers.FarmRelatedBusiness', related_name='management_type',
                                            verbose_name=_('Management Type'))
    update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('Management')
        verbose_name_plural = _('Management')

    def __str__(self):
        return str(self.basefarmer)

    def __unicode__(self):
        return str(self.basefarmer)


class FarmRelatedBusiness(Model):
    name = CharField(max_length=50, null=True, blank=True, verbose_name=_('Related Business Name'))
    has_business = CharField(max_length=1, null=True, blank=True, verbose_name=_('Has Business'))
    update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('FarmRelatedBusiness')
        verbose_name_plural = _('FarmRelatedBusiness')

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)
    

class Business(Model):
    basefarmer = OneToOneField('basefarmers.BaseFarmer', related_name='business', verbose_name=_('BaseFarmer'))
    farm_related_business = ManyToManyField('basefarmers.FarmRelatedBusiness', related_name='farm_related_business', verbose_name=_('Farm Related Business'))
    update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('Business')
        verbose_name_plural = _('Business')

    def __str__(self):
        return str(self.basefarmer)

    def __unicode__(self):
        return str(self.basefarmer)


class FarmerProductionType(Model):
    name = CharField(max_length=20, null=True, blank=True, verbose_name=_('Production Type Name'))
    update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('FarmerProductionType')
        verbose_name_plural = _('FarmerProductionType')

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)


class FarmerLandType(Model):
    name = CharField(max_length=20, null=True, blank=True, verbose_name=_('Land Type Name'))
    update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('FarmerLandType')
        verbose_name_plural = _('FarmerLandType')

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)


class FarmerLandArea(Model):
    basefarmer = ForeignKey('basefarmers.BaseFarmer', related_name='farmer_land_areas', blank=True, verbose_name=_('BaseFarmer'))
    farmer_production_type = ForeignKey('basefarmers.FarmerProductionType', related_name='farmer_production_type', verbose_name=_('Farmer Production Type'))
    farmer_land_type = ForeignKey('basefarmers.FarmerLandType', related_name='farmer_land_type', verbose_name=_('Farmer Land Type'))
    value = IntegerField(null=True, blank=True, verbose_name=_('Area Value'))
    update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('FarmerLandArea')
        verbose_name_plural = _('FarmerLandArea')

    def __str__(self):
        return str(self.basefarmer)

    def __unicode__(self):
        return str(self.basefarmer)


class Phone(Model):
    basefarmer = ForeignKey('basefarmers.BaseFarmer', related_name='phones', verbose_name=_('BaseFarmer'))
    phone = CharField(max_length=100, null=True, blank=True, verbose_name=_('Phone'))
    update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('Phone')
        verbose_name_plural = _('Phone')

    def __str__(self):
        return str(self.basefarmer)

    def __unicode__(self):
        return str(self.basefarmer)

class Lack(Model):
    #enough_worker = BooleanField(default=False, verbose_name=_('Enough Worker'))
    #uncertain_worker = BooleanField(default=False, verbose_name=_('Uncertain Worker'))
    #add_value_others = BooleanField(default=False, verbose_name=_('Add Value Others'))
    #is_lack = BooleanField(default=False, verbose_name=_('Is Lack'))
    name = CharField(max_length=50, unique=True, verbose_name=_('Name'))
    #is_lack = BooleanField(default=False, verbose_name=_('Is Lack'))
    update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('Lack')
        verbose_name_plural = _('Lack')

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)


class AddressMatch(Model):
    basefarmer = OneToOneField('basefarmers.BaseFarmer', related_name='address_match', verbose_name=_('BaseFarmer'))
    match = BooleanField(default=False, verbose_name=_('Address Match'))
    different = BooleanField(default=False, verbose_name=_('Address Different'))
    address = CharField(max_length=100, null=True, blank=True, verbose_name=_('Address'))
    update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('AddressMatch')
        verbose_name_plural = _('AddressMatch')

    def __str__(self):
        return str(self.basefarmer)

    def __unicode__(self):
        return str(self.basefarmer)


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
    basefarmer = ForeignKey('basefarmers.BaseFarmer', related_name='annual_incomes', blank=True, verbose_name=_('BaseFarmer'))
    market_type = ForeignKey('basefarmers.MarketType', verbose_name=_('Market Type'))
    income_range_code = ForeignKey('basefarmers.IncomeRangeCode', verbose_name=_('Income Range Code'))
    update_time = DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('AnnualIncome')
        verbose_name_plural = _('AnnualIncomes')

    def __str__(self):
        return str(self.basefarmer)
        #return '%s(%s)' % (self.market_type, self.income_range_code)

    def __unicode__(self):
        return str(self.basefarmer)
        #return '%s(%s)' % (self.market_type, self.income_range_code)



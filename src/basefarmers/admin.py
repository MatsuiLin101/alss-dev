from django.contrib import admin
from .models import (
    MarketType,
    IncomeRangeCode,
    AnnualIncome,
    BaseFarmer,
    AddressMatch,
    Lack,
    Phone,
    FarmerLandArea,
    FarmerLandType,
    FarmerProductionType,
    FarmRelatedBusiness,
    Business,
    Management,
    ManagementType,
)

admin.site.register(MarketType)
admin.site.register(IncomeRangeCode)
admin.site.register(AnnualIncome)
admin.site.register(BaseFarmer)
admin.site.register(AddressMatch)
admin.site.register(Lack)
admin.site.register(Phone)
admin.site.register(FarmerLandArea)
admin.site.register(FarmerLandType)
admin.site.register(FarmerProductionType)
admin.site.register(FarmRelatedBusiness)
admin.site.register(Business)
admin.site.register(ManagementType)
admin.site.register(Management)
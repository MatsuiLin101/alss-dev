from django.contrib import admin
from .models import MarketType, IncomeRangeCode, AnnualIncome, BaseFarmer, AddressMatch, Lack

admin.site.register(MarketType)
admin.site.register(IncomeRangeCode)
admin.site.register(AnnualIncome)
admin.site.register(BaseFarmer)
admin.site.register(AddressMatch)
admin.site.register(Lack)
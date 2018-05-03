from django.contrib import admin
from .models import MarketType, IncomeRangeCode, AnnualIncome, BaseFarmer

admin.site.register(MarketType)
admin.site.register(IncomeRangeCode)
admin.site.register(AnnualIncome)
admin.site.register(BaseFarmer)
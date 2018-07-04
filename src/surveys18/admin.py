from django.contrib import admin
from rangefilter.filter import DateRangeFilter
from .models import (
    BuilderFile,
    BuilderFileType,
    MarketType,
    IncomeRange,
    AnnualIncome,
    Survey,
    AddressMatch,
    Lack,
    Phone,
    LandArea,
    LandType,
    LandStatus,
    FarmRelatedBusiness,
    ManagementType,
    Loss,
    Unit,
    Product,
    Contract,
    CropMarketing,
    LivestockMarketing,
    Facility,
    PopulationAge,
    Population,
    EducationLevel,
    FarmerWorkDay,
    LifeStyle,
    OtherFarmWork,
    Subsidy,
    RefuseReason,
    AgeScope,
    LongTermHire,
    ShortTermHire,
    WorkType,
    NumberWorkers,
    NoSalaryHire,
    ShortTermLack,
    LongTermLack,
    Gender,
    ProductType,
    Business,
)


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'farmer_id',
                    'farmer_name',
                    'total_pages',
                    'page',
                    'readonly',
                    'is_updated',
                    'update_time')
    list_filter = ('is_updated', 'readonly', 'page', ('update_time', DateRangeFilter))


admin.site.register(Survey, SurveyAdmin)
admin.site.register(BuilderFile)
admin.site.register(BuilderFileType)
admin.site.register(MarketType)
admin.site.register(IncomeRange)
admin.site.register(AnnualIncome)
admin.site.register(AddressMatch)
admin.site.register(Lack)
admin.site.register(Phone)
admin.site.register(LandArea)
admin.site.register(LandType)
admin.site.register(LandStatus)
admin.site.register(Business)
admin.site.register(FarmRelatedBusiness)
admin.site.register(ManagementType)
admin.site.register(Loss)
admin.site.register(Unit)
admin.site.register(Product)
admin.site.register(Contract)
admin.site.register(CropMarketing)
admin.site.register(LivestockMarketing)
admin.site.register(Facility)
admin.site.register(PopulationAge)
admin.site.register(Population)
admin.site.register(EducationLevel)
admin.site.register(FarmerWorkDay)
admin.site.register(LifeStyle)
admin.site.register(OtherFarmWork)
admin.site.register(Subsidy)
admin.site.register(RefuseReason)
admin.site.register(AgeScope)
admin.site.register(WorkType)
admin.site.register(LongTermHire)
admin.site.register(ShortTermHire)
admin.site.register(NumberWorkers)
admin.site.register(NoSalaryHire)
admin.site.register(ShortTermLack)
admin.site.register(LongTermLack)
admin.site.register(Gender)
admin.site.register(ProductType)







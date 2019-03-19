from rest_framework.serializers import ModelSerializer

from apps.surveys19.models import (
    Survey19,
    Phone,
    AddressMatch,
    CityTownCode,
    FarmLocation,
    LandStatus,
    LandType,
    LandArea,
    Business,
    FarmRelatedBusiness,
    ManagementType,
    CropMarketing,
    LivestockMarketing,
    ProductType,
    Product,
    Unit,
    Loss,
    Contract,
    AnnualIncome,
    MarketType,
    IncomeRange,
    AgeScope,
    PopulationAge,
    Population,
    Relationship,
    Gender,
    EducationLevel,
    FarmerWorkDay,
    LifeStyle,
    LongTermHire,
    ShortTermHire,
    NoSalaryHire,
    NumberWorkers,
    Lack,
    LongTermLack,
    ShortTermLack,
    WorkType,
    Subsidy,
    Refuse,
    RefuseReason,
    Month,
)


class Survey19Serializer(ModelSerializer):

    class Meta:
        model = Survey19
        fields = '__all__'


class PhoneSerializer(ModelSerializer):

    class Meta:
        model = Phone
        fields = '__all__'


class AddressMatchSerializer(ModelSerializer):

    class Meta:
        model = AddressMatch
        fields = '__all__'


class CityTownCodeSerializer(ModelSerializer):

    class Meta:
        model = CityTownCode
        fields = '__all__'


class FarmLocationSerializer(ModelSerializer):

    class Meta:
        model = FarmLocation
        fields = '__all__'


class LandStatusSerializer(ModelSerializer):

    class Meta:
        model = LandStatus
        fields = '__all__'


class LandTypeSerializer(ModelSerializer):

    class Meta:
        model = LandType
        fields = '__all__'


class LandAreaSerializer(ModelSerializer):

    class Meta:
        model = LandArea
        fields = '__all__'


class BusinessSerializer(ModelSerializer):

    class Meta:
        model = Business
        fields = '__all__'


class FarmRelatedBusinessSerializer(ModelSerializer):

    class Meta:
        model = FarmRelatedBusiness
        fields = '__all__'


class ManagementTypeSerializer(ModelSerializer):

    class Meta:
        model = ManagementType
        fields = '__all__'


class CropMarketingSerializer(ModelSerializer):

    class Meta:
        model = CropMarketing
        fields = '__all__'


class LivestockMarketingSerializer(ModelSerializer):

    class Meta:
        model = LivestockMarketing
        fields = '__all__'


class ProductTypeSerializer(ModelSerializer):

    class Meta:
        model = ProductType
        fields = '__all__'


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class UnitSerializer(ModelSerializer):

    class Meta:
        model = Unit
        fields = '__all__'


class LossSerializer(ModelSerializer):

    class Meta:
        model = Loss
        fields = '__all__'


class ContractSerializer(ModelSerializer):

    class Meta:
        model = Contract
        fields = '__all__'


class AnnualIncomeSerializer(ModelSerializer):

    class Meta:
        model = AnnualIncome
        fields = '__all__'


class MarketTypeSerializer(ModelSerializer):

    class Meta:
        model = MarketType
        fields = '__all__'


class IncomeRangeSerializer(ModelSerializer):

    class Meta:
        model = IncomeRange
        fields = '__all__'


class AgeScopeSerializer(ModelSerializer):

    class Meta:
        model = AgeScope
        fields = '__all__'


class PopulationAgeSerializer(ModelSerializer):

    class Meta:
        model = PopulationAge
        fields = '__all__'


class PopulationSerializer(ModelSerializer):

    class Meta:
        model = Population
        fields = '__all__'


class RelationshipSerializer(ModelSerializer):

    class Meta:
        model = Relationship
        fields = '__all__'


class GenderSerializer(ModelSerializer):

    class Meta:
        model = Gender
        fields = '__all__'


class EducationLevelSerializer(ModelSerializer):

    class Meta:
        model = EducationLevel
        fields = '__all__'


class FarmerWorkDaySerializer(ModelSerializer):

    class Meta:
        model = FarmerWorkDay
        fields = '__all__'


class LifeStyleSerializer(ModelSerializer):

    class Meta:
        model = LifeStyle
        fields = '__all__'


class LongTermHireSerializer(ModelSerializer):

    class Meta:
        model = LongTermHire
        fields = '__all__'


class ShortTermHireSerializer(ModelSerializer):

    class Meta:
        model = ShortTermHire
        fields = '__all__'


class NoSalaryHireSerializer(ModelSerializer):

    class Meta:
        model = NoSalaryHire
        fields = '__all__'


class NumberWorkersSerializer(ModelSerializer):

    class Meta:
        model = NumberWorkers
        fields = '__all__'


class LackSerializer(ModelSerializer):

    class Meta:
        model = Lack
        fields = '__all__'


class LongTermLackSerializer(ModelSerializer):

    class Meta:
        model = LongTermLack
        fields = '__all__'


class ShortTermLackSerializer(ModelSerializer):

    class Meta:
        model = ShortTermLack
        fields = '__all__'


class WorkTypeSerializer(ModelSerializer):

    class Meta:
        model = WorkType
        fields = '__all__'


class SubsidySerializer(ModelSerializer):

    class Meta:
        model = Subsidy
        fields = '__all__'


class RefuseSerializer(ModelSerializer):

    class Meta:
        model = Refuse
        fields = '__all__'


class RefuseReasonSerializer(ModelSerializer):

    class Meta:
        model = RefuseReason
        fields = '__all__'


class MonthSerializer(ModelSerializer):

    class Meta:
        model = Month
        fields = '__all__'

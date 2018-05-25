from rest_framework.serializers import ModelSerializer
from surveys18.models import (
    AnnualIncome,
    Survey,
    AddressMatch,
    Lack,
    Phone,
    LandArea,
    Business,
    Management,
    CropMarketing,
    LivestockMarketing,
    PopulationAge,
    Population,
    Subsidy,
    LongTermHire,
    ShortTermHire,
    NoSalaryHire,
    ShortTermLack,
    LongTermLack,
)


class AnnualIncomeSerializer(ModelSerializer):
    class Meta:
        model = AnnualIncome
        fields = '__all__'


class AddressMatchSerializer(ModelSerializer):
    class Meta:
        model = AddressMatch
        fields = '__all__'


class LackSerializer(ModelSerializer):
    class Meta:
        model = Lack
        fields = '__all__'


class PhoneSerializer(ModelSerializer):
    class Meta:
        model = Phone
        fields = '__all__'


class LandAreaSerializer(ModelSerializer):
    class Meta:
        model = LandArea
        fields = '__all__'


class BusinessSerializer(ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'


class ManagementSerializer(ModelSerializer):
    class Meta:
        model = Management
        fields = '__all__'


class CropMarketingSerializer(ModelSerializer):
    class Meta:
        model = CropMarketing
        fields = '__all__'


class LivestockMarketingSerializer(ModelSerializer):
    class Meta:
        model = LivestockMarketing
        fields = '__all__'


class PopulationAgeSerializer(ModelSerializer):
    class Meta:
        model = PopulationAge
        fields = '__all__'


class PopulationSerializer(ModelSerializer):
    class Meta:
        model = Population
        fields = '__all__'


class SubsidySerializer(ModelSerializer):
    class Meta:
        model = Subsidy
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


class ShortTermLackSerializer(ModelSerializer):
    class Meta:
        model = ShortTermLack
        fields = '__all__'


class LongTermLackSerializer(ModelSerializer):
    class Meta:
        model = LongTermLack
        fields = '__all__'


class SurveySerializer(ModelSerializer):
    annual_incomes = AnnualIncomeSerializer(many=True)
    address_match = AddressMatchSerializer()
    lacks = LackSerializer(many=True)
    phones = PhoneSerializer(many=True)
    land_areas = LandAreaSerializer(many=True)
    businesses = BusinessSerializer()
    managements = ManagementSerializer()
    crop_marketings = CropMarketingSerializer(many=True)
    livestock_marketings = LivestockMarketingSerializer(many=True)
    population_ages = PopulationAgeSerializer(many=True)
    populations = PopulationSerializer(many=True)
    subsidy = SubsidySerializer()
    long_term_hires = LongTermHireSerializer(many=True)
    short_term_hires = ShortTermHireSerializer(many=True)
    no_salary_hires = NoSalaryHireSerializer(many=True)
    long_term_lacks = LongTermLackSerializer(many=True)
    short_term_lacks = ShortTermLackSerializer(many=True)

    class Meta:
        model = Survey
        fields = '__all__'





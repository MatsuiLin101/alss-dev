from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import ModelSerializer, IntegerField
from surveys18.models import (
    AnnualIncome,
    Survey,
    AddressMatch,
    Lack,
    Phone,
    LandArea,
    ManagementType,
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
    LandStatus,
    LandType,
    FarmRelatedBusiness,
    NumberWorkers,
    Business,
    Refuse,
    Product,
    Month,
)


class AnnualIncomeSerializer(ModelSerializer):
    id = IntegerField(read_only=False)
    
    class Meta:
        model = AnnualIncome
        fields = '__all__'


class AddressMatchSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = AddressMatch
        fields = '__all__'
        extra_kwargs = {
            'survey': {'validators': []},
        }


class LackSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = Lack
        fields = '__all__'


class PhoneSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = Phone
        fields = '__all__'


class LandStatusSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = LandStatus
        fields = '__all__'


class LandTypeSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = LandType
        fields = '__all__'


class LandAreaSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = LandArea
        fields = '__all__'


class ManagementTypeSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = ManagementType
        fields = '__all__'


class CropMarketingSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = CropMarketing
        fields = '__all__'


class LivestockMarketingSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = LivestockMarketing
        fields = '__all__'


class PopulationAgeSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = PopulationAge
        fields = '__all__'


class PopulationSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = Population
        fields = '__all__'


class RefuseSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = Refuse
        fields = '__all__'
        extra_kwargs = {
            'reason': {'validators': []},
        }


class SubsidySerializer(ModelSerializer):
    id = IntegerField(read_only=False)
    refuses = RefuseSerializer(many=True)

    class Meta:
        model = Subsidy
        fields = '__all__'
        extra_kwargs = {
            'survey': {'validators': []},
        }


class NumberWorkers(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = NumberWorkers
        fields = '__all__'


class MonthSerializer(ModelSerializer):
    class Meta:
        model = Month
        fields = '__all__'


class LongTermHireSerializer(ModelSerializer):
    id = IntegerField(read_only=False)
    number_workers = NumberWorkers(many=True)

    class Meta:
        model = LongTermHire
        fields = '__all__'


class ShortTermHireSerializer(ModelSerializer):
    id = IntegerField(read_only=False)
    number_workers = NumberWorkers(many=True)

    class Meta:
        model = ShortTermHire
        fields = '__all__'


class NoSalaryHireSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = NoSalaryHire
        fields = '__all__'


class ShortTermLackSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = ShortTermLack
        fields = '__all__'


class LongTermLackSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = LongTermLack
        fields = '__all__'


class FarmRelatedBusinessSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = FarmRelatedBusiness
        fields = '__all__'


class BusinessSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = Business
        fields = '__all__'
        extra_kwargs = {
            'farm_related_business': {'validators': []},
        }


class SurveySerializer(ModelSerializer):
    annual_incomes = AnnualIncomeSerializer(many=True)
    address_match = AddressMatchSerializer()
    businesses = BusinessSerializer(many=True)
    lacks = LackSerializer(many=True)
    phones = PhoneSerializer(many=True)
    land_areas = LandAreaSerializer(many=True)
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

    def update(self, instance, validated_data):
        # Update the instance
        instance.farmer_name = validated_data['farmer_name']
        instance.note = validated_data['note']
        instance.hire = validated_data['hire']
        instance.non_hire = validated_data['non_hire']

        instance.save()

        '''Phone'''
        for item in validated_data['phones']:
            phone_qs = instance.phones.filter(id=item['id'])
            phone_qs.update(
                phone=item['phone']
            )

        '''AddressMatch'''
        instance.address_match.match = validated_data['address_match']['match']
        instance.address_match.mismatch = validated_data['address_match']['mismatch']
        instance.address_match.address = validated_data['address_match']['address']
        instance.address_match.save()

        '''CropMarketing'''
        crop_marketing_ids = [item['id'] for item in validated_data['crop_marketings'] if 'id' in item]
        # Delete not included in the request
        for obj in instance.crop_marketings.all():
            if obj.id not in crop_marketing_ids:
                obj.delete()
        for item in validated_data['crop_marketings']:
            if 'id' in item.keys():
                # Update included in the request
                crop_marketing_qs = instance.crop_marketings.filter(id=item['id'])
                if crop_marketing_qs:
                    crop_marketing_ids.append(item['id'])
                    crop_marketing_qs.update(
                        product=item['product'] if 'product' in item else None,
                        loss=item['loss'] if 'loss' in item else None,
                        unit=item['unit'] if 'unit' in item else None,
                        land_number=item['land_number'] if 'land_number' in item else None,
                        land_area=item['land_area'] if 'land_area' in item else None,
                        plant_times=item['plant_times'] if 'plant_times' in item else None,
                        total_yield=item['total_yield'] if 'total_yield' in item else None,
                        unit_price=item['unit_price'] if 'unit_price' in item else None,
                        has_facility=item['has_facility'] if 'has_facility' in item else None
                    )
            else:
                # Create
                CropMarketing.objects.create(
                    survey=instance,
                    product=item['product'] if 'product' in item else None,
                    loss=item['loss'] if 'loss' in item else None,
                    unit=item['unit'] if 'unit' in item else None,
                    land_number=item['land_number'] if 'land_number' in item else None,
                    land_area=item['land_area'] if 'land_area' in item else None,
                    plant_times=item['plant_times'] if 'plant_times' in item else None,
                    total_yield=item['total_yield']if 'total_yield' in item else None,
                    unit_price=item['unit_price'] if 'unit_price' in item else None,
                    has_facility=item['has_facility'] if 'has_facility' in item else None
                )
                
        '''LivestockMarketing'''
        livestock_marketing_ids = [item['id'] for item in validated_data['livestock_marketings'] if 'id' in item]
        # Delete not included in the request
        for obj in instance.livestock_marketings.all():
            if obj.id not in livestock_marketing_ids:
                obj.delete()
        for item in validated_data['livestock_marketings']:
            if 'id' in item.keys():
                # Update included in the request
                livestock_marketing_qs = instance.livestock_marketings.filter(id=item['id'])
                if livestock_marketing_qs:
                    livestock_marketing_qs.update(
                        product=item['product'] if 'product' in item else None,
                        loss=item['loss'] if 'loss' in item else None,
                        unit=item['unit'] if 'unit' in item else None,
                        raising_number=item['raising_number'] if 'raising_number' in item else None,
                        total_yield=item['total_yield'] if 'total_yield' in item else None,
                        unit_price=item['unit_price'] if 'unit_price' in item else None,
                        contract=item['contract'] if 'contract' in item else None
                    )
            else:
                # Create
                LivestockMarketing.objects.create(
                    survey=instance,
                    product=item['product'] if 'product' in item else None,
                    loss=item['loss'] if 'loss' in item else None,
                    unit=item['unit'] if 'unit' in item else None,
                    raising_number=item['raising_number'] if 'raising_number' in item else None,
                    total_yield=item['total_yield'] if 'total_yield' in item else None,
                    unit_price=item['unit_price'] if 'unit_price' in item else None,
                    contract=item['contract'] if 'contract' in item else None
                )
                
        '''AnnualIncome'''
        annual_income_ids = [item['id'] for item in validated_data['annual_incomes'] if 'id' in item]
        # Delete not included in the request
        for obj in instance.annual_incomes.all():
            if obj.id not in annual_income_ids:
                obj.delete()
        for item in validated_data['annual_incomes']:
            if 'id' in item.keys():
                # Update included in the request
                annual_income_qs = instance.annual_incomes.filter(id=item['id'])
                if annual_income_qs:
                    annual_income_qs.update(
                        market_type=item['market_type'] if 'market_type' in item else None,
                        income_range=item['income_range'] if 'income_range' in item else None
                    )
            else:
                # Create
                AnnualIncome.objects.create(
                    survey=instance,
                    market_type=item['market_type'] if 'market_type' in item else None,
                    income_range=item['income_range'] if 'income_range' in item else None
                )

        '''PopulationAge'''
        for item in validated_data['population_ages']:
            # Update included in the request
            population_age_qs = instance.population_ages.filter(id=item['id'])
            if population_age_qs:
                population_age_qs.update(
                    count=item['count'] if 'count' in item else None,
                )

        '''Population'''
        population_ids = [item['id'] for item in validated_data['populations'] if 'id' in item]
        # Delete not included in the request
        for obj in instance.populations.all():
            if obj.id not in population_ids:
                obj.delete()
        for item in validated_data['populations']:
            if 'id' in item.keys():
                # Update included in the request
                population_qs = instance.populations.filter(id=item['id'])
                if population_qs:
                    population_qs.update(
                        relationship=item['relationship'] if 'relationship' in item else None,
                        gender=item['gender'] if 'gender' in item else None,
                        birth_year=item['birth_year'] if 'birth_year' in item else None,
                        education_level=item['education_level'] if 'education_level' in item else None,
                        farmer_work_day=item['farmer_work_day'] if 'farmer_work_day' in item else None,
                        life_style=item['life_style'] if 'life_style' in item else None,
                        other_farm_work=item['other_farm_work'] if 'other_farm_work' in item else None
                    )
            else:
                # Create
                Population.objects.create(
                    survey=instance,
                    relationship=item['relationship'] if 'relationship' in item else None,
                    gender=item['gender'] if 'gender' in item else None,
                    birth_year=item['birth_year'] if 'birth_year' in item else None,
                    education_level=item['education_level'] if 'education_level' in item else None,
                    farmer_work_day=item['farmer_work_day'] if 'farmer_work_day' in item else None,
                    life_style=item['life_style'] if 'life_style' in item else None,
                    other_farm_work=item['other_farm_work'] if 'other_farm_work' in item else None
                )

        '''LongTermHire'''
        long_term_hire_ids = [item['id'] for item in validated_data['long_term_hires'] if 'id' in item]
        # Delete not included in the request
        for obj in instance.long_term_hires.all():
            if obj.id not in long_term_hire_ids:
                obj.delete()
        for item in validated_data['long_term_hires']:
            if 'id' in item.keys():
                pass
                # Update included in the request
                long_term_hire_qs = instance.long_term_hires.filter(id=item['id'])
                if long_term_hire_qs:
                    long_term_hire_qs.update(
                        work_type=item['work_type'] if 'work_type' in item else None,
                        avg_work_day=item['avg_work_day'] if 'avg_work_day' in item else None,
                    )
                    long_term_hire_qs.first().months.clear()
                    for month in item['months']:
                        long_term_hire_qs.first().months.add(month)

                    '''NumberWorker'''
                    number_worker_ids = [item['id'] for item in item['number_workers'] if 'id' in item]
                    # Delete not included in the request
                    for obj in long_term_hire_qs.first().number_workers.all():
                        if obj.id not in number_worker_ids:
                            obj.delete()
                    for obj in item['number_workers']:
                        if 'id' in obj.keys():
                            # Update included in the request
                            number_worker_qs = long_term_hire_qs.first().number_workers.filter(id=obj['id'])
                            if number_worker_qs:
                                number_worker_qs.update(
                                    count=obj['count'] if 'count' in obj else None,
                                )
                        else:
                            # Create
                            NumberWorkers.objects.create(
                                count=obj['count'] if 'count' in obj else None,
                                content_type=ContentType.objects.get(app_label='surveys18', model="longtermhire"),
                                object_id=item['id']
                            )
            else:
                # Create
                content_object = LongTermHire.objects.create(
                    survey=instance,
                    work_type=item['work_type'] if 'work_type' in item else None,
                    avg_work_day=item['avg_work_day'] if 'avg_work_day' in item else None,
                )
                for month in item['months']:
                    content_object.months.add(month)
                for obj in item['number_workers']:
                    NumberWorkers.objects.create(
                        count=obj['count'] if 'count' in obj else None,
                        content_type=ContentType.objects.get(app_label='surveys18', model="longtermhire"),
                        object_id=content_object.id,
                    )

        return instance







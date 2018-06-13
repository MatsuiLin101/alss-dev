from .exceptions import SignError, StringLengthError, CreateModelError
from django.contrib.contenttypes.models import ContentType

from surveys18.models import (
    MarketType,
    IncomeRange,
    AnnualIncome,
    Survey,
    AddressMatch,
    FarmRelatedBusiness,
    Business,
    ManagementType,
    Lack,
    Phone,
    LandArea,
    LandType,
    LandStatus,
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
    Relationship,
    Month,
    Refuse
)

class Builder(object):

    def __init__(self, string):
        string = string.replace(" ","")
        self.string = string.split(",")

    def build(self, readonly=True):
        self.build_survey(readonly=readonly)
        try:
            self.build_phone()
            self.build_address()
            self.build_land_area()
            self.build_business()
            self.build_management()
            self.build_crop_marketing()
            self.build_livestock_marketing()
            self.build_population()
        except Exception as e:
            Survey.objects.filter(farmer_id=self.survey.farmer_id, page=self.survey.page,
                                  readonly=self.survey.readonly).delete()
            raise e

    def build_survey(self, readonly=True):
        farmer_id = self.string[2]
        total_pages = 1
        page = 1
        name = self.string[7]
        is_updated = True
        obj = Survey.objects.filter(page=page, farmer_id=farmer_id).all()
        if obj is None:
            try:

                survey = Survey.objects.create(
                    farmer_id=farmer_id,
                    farmer_name=name,
                    page=page,
                    total_pages=total_pages,
                    is_updated=is_updated,
                    readonly=readonly
                )

                self.survey = survey
            except ValueError as e:
                raise CreateModelError(target='Survey', msg=e)
            else:
                self.survey = survey

    def build_phone(self):
        phones = self.string[8:10]
        if len(phones[0]) > 0 or len(phones[1]) > 0:
            try:
                self.phones = []
                for number in phones:
                    if len(number) > 0:
                        phone = Phone.objects.create(
                            survey=self.survey,
                            phone=number
                        )
                        self.phones.append(phone)
            except ValueError as e:
                raise CreateModelError(target='Phone', msg=e)

    def build_address(self):
        address = self.string[10]
        if len(address) > 0:
            try:
                address = AddressMatch.objects.create(
                    survey=self.survey,
                    mismatch=True,
                    address=address
                )
            except ValueError as e:
                raise CreateModelError(target='Address Match', msg=e)
            else:
                self.address = address
        else:
            try:
                address = AddressMatch.objects.create(
                    survey=self.survey,
                    match=True,
                )
            except ValueError as e:
                raise CreateModelError(target='Address Match', msg=e)
            else:
                self.address = address


    def build_land_area(self):
        land_area_str = self.string[12:18]
        if len(land_area_str[0]) > 0 :
            try:
                self.land_area = []
                cnt = 0
                for i in range(0, len(land_area_str),3):
                    if int(land_area_str[i]) > 0:
                        type = 1 if cnt < 3 else 2
                        status = (i % 3) + 1

                        land_type = LandType.objects.get(id=type)
                        land_status = LandStatus.objects.get(id=status)

                        land_area = LandArea.objects.create(
                            survey=self.survey,
                            type=land_type,
                            status=land_status,
                            value=int(land_area_str[i])
                        )
                        self.land_area.append(land_area)
                    cnt = cnt + 1

                if int(land_area_str[-1]) > 0:
                    land_type = LandType.objects.get(id=3)
                    land_area = LandArea.objects.create(
                        survey=self.survey,
                        type=land_type,
                    )
                    self.land_area.append(land_area)

            except ValueError as e:
                raise CreateModelError(target='Land Area', msg=e)

    def build_business(self):
        business_str = self.string[40:50]
        if len(business_str) > 0:
            try:
                self.business = []
                for i in range(0, 8):
                    if business_str[i] == "1":
                        num = i + 1
                        business = Business.objects.create(
                            survey=self.survey,
                            farm_related_business=FarmRelatedBusiness.objects.get(code=num)

                        )
                        self.business.append(business)
                if business_str[8] == "1" :
                    business = Business.objects.create(
                        survey=self.survey,
                        farm_related_business=FarmRelatedBusiness.objects.get(code=9),
                        extra=business_str[9]
                    )
                    self.business.append(business)
                elif len(business_str[9]) > 0 :
                    business = Business.objects.create(
                        survey=self.survey,
                        farm_related_business=FarmRelatedBusiness.objects.get(code=9),
                        extra=business_str[9]
                    )
                    self.business.append(business)

            except ValueError as e:
                raise CreateModelError(target='Business', msg=e)

    def build_management(self):
        management_str = self.string[55]
        if len(management_str) > 0 :
            try:
                char = list(management_str)
                num = int(char[0])
                if num > 3:
                    num = num
                elif num > 3 and num < 8 :
                    num = num+1
                elif num == 10:
                    num = 12
                elif num == 12:
                    num = 13
                elif num == 11 or num == 13 or num == 14 or num == 15 :
                    num = 14
                else:
                    num = 0

                if num> 0:
                    management_type = ManagementType.objects.get(id=num)
                    self.survey.management_types.add(management_type)

            except ValueError as e:
                raise CreateModelError(target='management', msg=e)

    def build_crop_marketing(self):
        crop_marketing_str = self.string[19:30]
        if len(crop_marketing_str[0]) > 0:
            try:
                product_str = crop_marketing_str[0]
                product = Product.objects.filter(code=product_str).first()
                land_number = crop_marketing_str[2]
                land_area = crop_marketing_str[3]
                plant_times = crop_marketing_str[4]
                unit_str = int(crop_marketing_str[5])
                unit = Unit.objects.filter(code=unit_str, type=1).first()
                total_yield  = crop_marketing_str[6]
                unit_price = crop_marketing_str[7]
                has_facility_str = int(crop_marketing_str[8])
                if has_facility_str == 0:
                    has_facility = None
                elif has_facility_str == 1:
                    has_facility = 1

                loss_str = int(crop_marketing_str[10])
                loss = Loss.objects.filter(code=loss_str, type=1).first()

                crop_marketing = CropMarketing.objects.create(
                    survey=self.survey,
                    product=product,
                    land_number=land_number,
                    land_area=land_area,
                    plant_times=plant_times,
                    unit=unit,
                    total_yield=total_yield,
                    unit_price=unit_price,
                    has_facility=has_facility,
                    loss=loss
                )
                self.crop_marketing.append(crop_marketing)

            except ValueError as e:
                raise CreateModelError(target='CropMarketing', msg=e)

    def build_livestock_marketing(self):
        livestock_str = self.string[31:40]
        if len(livestock_str[0]) > 0 :
            try:
                product_str = livestock_str[0]
                product = Product.objects.filter(code=product_str).first()
                unit_str = livestock_str[2]
                unit = Unit.objects.filter(code=unit_str, type=2).first()
                raising_number = int(livestock_str[3])
                total_yield = int(livestock_str[4])
                unit_price = int(livestock_str[5])
                contract_str = int(livestock_str[6])
                contract = Contract.objects.filter(code=contract_str).first()
                loss_str = int(livestock_str[7])
                loss = Loss.objects.filter(code=loss_str, type=2).first()

                livestock_marketing = LivestockMarketing.objects.create(
                    survey=self.survey,
                    product=product,
                    unit=unit,
                    raising_number=raising_number,
                    total_yield=total_yield,
                    unit_price=unit_price,
                    contract=contract,
                    loss=loss

                )
                self.livestock_marketing.append(livestock_marketing)
            except ValueError as e:
                raise CreateModelError(target='LivestockMarketing', msg=e)

    def build_population(self):
        population_str = self.string[51:56]
        if len(population_str[0]) > 0:
            try:
                self.population=[]
                relationship_str = int(population_str[0])
                relationship = Relationship.objects.filter(code=relationship_str).first()
                gender_str = int(population_str[1])
                gender = Gender.objects.filter(code=gender_str).first()

                birth_year = int(int(population_str[2])/100)
                education_level_str = int(population_str[3])
                education_level = EducationLevel.objects.filter(code=education_level_str).first()
                farmer_work_day_str = population_str[4]
                farmer_work_day_cnt, farmer_work_day_id = self.id_and_value(farmer_work_day_str)
                if farmer_work_day_cnt != 1:
                    farmer_work_day = None
                else:
                    farmer_work_day = FarmerWorkDay.objects.filter(code=farmer_work_day_id).first()

                population = Population.objects.create(
                    survey=self.survey,
                    relationship=relationship,
                    gender=gender,
                    birth_year=birth_year,
                    education_level=education_level,
                    farmer_work_day=farmer_work_day
                )
                self.population.append(population)

            except ValueError as e:
                raise CreateModelError(target='Population', msg=e)
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
        obj = Survey.objects.filter(page=page, farmer_id=id).all()
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
                    address=address
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
        business_str = self.string[40:49]
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
                if business_str[8] == "1":
                    business = Business.objects.create(
                        survey=self.survey,
                        farm_related_business=FarmRelatedBusiness.objects.get(code=9),
                        extra=business_str[9:]
                    )
                print(business.farm_related_business)
                self.business.append(business)
            except ValueError as e:
                raise CreateModelError(target='Business', msg=e)

    def build_management(self):
        management_str = self.string[55]
        if len(management_str) > 0 :
            try:
                if management_str
                for i in range(0, 14):
                    if management_str[i] == "1":
                        num = i + 1
                        management_type = ManagementType.objects.get(id=num)
                        self.survey.management_types.add(management_type)

            except ValueError as e:
                raise CreateModelError(target='management', msg=e)















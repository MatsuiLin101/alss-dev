from .exceptions import SignError, StringLengthError, CreateModelError
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
)


class Builder(object):

    def __init__(self, string):
        self.check_string(string)

        delimiter_plus = '+'
        delimiter_pound = '#+'
        cut_token = []
        tokens = string.split(delimiter_pound)
        for token in tokens:
            for t in token.split(delimiter_plus):
                cut_token.append(t)

        self.string = cut_token

    def build(self):
        self.build_survey()
        self.build_phone()
        self.build_address()
        self.build_land_area()

    @staticmethod
    def check_string(string):
        delimiter_plus = '+'
        delimiter_pound = '#+'
        slices = string.split(delimiter_plus)
        slices_pound = string.split(delimiter_pound)

        if len(slices) != 12 or len(slices_pound) != 3:
            if len(slices) != 12:
                raise SignError('+')
            if len(slices_pound) != 3:
                raise SignError('#+')
        else:
            if (slices_pound[1].find("#") is -1) or (slices_pound[-1].find("#") is -1) \
                    or (slices_pound[-2].find("#") is -1):
                raise SignError('#')
        return True



    # def build_crop_marketings(self):
    #     print(CROP_MARKETING_TOKEN)
    #     crop_marketings = []
    #     crop_marketings.appned(CropMarketing())
    #     self.crop_marketings = crop_marketings

    def build_survey(self):
        try:
            string = self.string[0]
            id = string[0:12]
            page = int(string[12:14])
            total_pages = int(string[14:16])
            name = string[16:23].replace("#", "")
            ori_class = int(string[44:46])

            string = self.string[-1]
            note = string.split("#")[0]
            period_h = int(string.split("#")[1][-9:-6])
            period_m = int(string.split("#")[1][-6:-4])
            distance_km = int(string.split("#")[1][-4:])

        except ValueError:
            raise StringLengthError('Survey')

        else:
            try:
                survey = Survey.objects.create(
                    farmer_id=id,
                    page=page,
                    total_pages=total_pages,
                    farmer_name=name,
                    origin_class=ori_class,
                    note=note,
                    period=period_h*60+period_m,
                    distance=distance_km
                )
            except ValueError:
                raise CreateModelError('Survey')
            else:
                 self.survey = survey

    def build_phone(self):
        try:
            string = self.string[0]
            phones = string[23:44].replace("#", "").split("/")
        except ValueError:
            raise StringLengthError('Phone')
        else:
            try:
                self.phones = []
                for number in phones:
                    if len(number) > 0:
                        phone =Phone.objects.create(
                            survey=self.survey,
                            phone=number
                        )
                        self.phones.append(phone)
            except ValueError:
                raise CreateModelError('Phone')

    def build_address(self):
        match = False
        mismatch = False
        try:
            string = self.string[0]
            match_str = string[46:47]
            mismatch_str = string[47:48]
            address = string[48:]
            if match_str == "1":
                match = True
            if mismatch_str == "1":
                mismatch = True
        except ValueError:
            raise StringLengthError('Address Match')
        else:
            try:
                address = AddressMatch.objects.create(
                    survey=self.survey,
                    match=match,
                    mismatch=mismatch,
                    address=address
                )
            except ValueError:
                raise CreateModelError('Address Match')
            else:
                self.address = address

    def build_land_area(self):
        try:
            string = self.string[1]
            area_str = string[0:26]
        except ValueError:
            raise StringLengthError('Land Area')
        else:
            try:
                self.land_area = []
                cnt = 0
                for i in range(5,len(area_str),5):
                    if int(area_str[cnt*5:i])>0:

                        type=1 if cnt<3 else 2
                        status=int((i/5))-3 if i/5>3 else int((i/5))

                        land_type = LandType.objects.get(id=type)
                        land_status = LandStatus.objects.get(id=status)

                        land_area = LandArea.objects.create(
                            survey=self.survey,
                            type=land_type,
                            status=land_status,
                            value=int(area_str[cnt*5:i])
                        )
                        self.land_area.append(land_area)
                    cnt = cnt+1

                if area_str[-1] == "1":
                    land_type = LandType.objects.get(id=3)
                    land_area = LandArea.objects.create(
                        survey=self.survey,
                        type=land_type,
                    )
                    self.land_area.append(land_area)

            except ValueError:
                raise CreateModelError('Land Area')

    def build_business(self):
        try:
            string = self.string[1]
            business_str = string[26:].split("#")[0]

        except ValueError:
            raise StringLengthError('Business')
        else:
            try:
                self.business = []
                for i in range(0,8):
                    if business_str[i] == "1":
                        num = i+1
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
                self.business.append(business)
            except ValueError:
                raise CreateModelError('Business')

    def build_management(self):
        try:
            string = self.string[1]
            management_str = string[26:].split("#")[1]

        except ValueError:
            raise StringLengthError('management')
        else:
            try:
                self.management=[]
                survey = Survey.objects.get(farmer_id=self.survey)
                for i in range(0,14):
                    if management_str[i] == "1":
                        num = i + 1
                        management_type = ManagementType.objects.get(id=num)
                        print(dir(management_type))
                        management_type.survey_set.add(survey)
                        #self.management.append(ManagementType.objects.get(id=num))

                # survey.save()
                # print(self.management)
                print(survey.farmer_id)
                print(survey.management_types)



            except ValueError:
                raise CreateModelError('management')

















# builder.survey

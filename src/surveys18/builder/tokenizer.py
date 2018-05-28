from .exceptions import SignError, StringLengthError, CreateModelError
from surveys18.models import (
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
    Business,
    Management,
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
        different = False
        try:
            string = self.string[0]
            match_str = string[46:47]
            different_str = string[47:48]
            address = string[48:]
            if match_str == "1":
                match = True
            if different_str == "1":
                different = True
        except ValueError:
            raise StringLengthError('Address Match')
        else:
            try:
                address = AddressMatch.objects.create(
                    survey=self.survey,
                    match=match,
                    different=different,
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
                        if cnt < 3 :
                            type = 1
                        else:
                            type = 2

                        if i/5 > 3 :
                            status = int((i / 5))-3
                        else:
                            status = int((i / 5))

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







# builder.survey

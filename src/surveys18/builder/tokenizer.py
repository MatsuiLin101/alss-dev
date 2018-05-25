from .exceptions import SignError
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
    # slice var
    BASE_SLICE = 48
    TABLE_1_SLICE = [26, 9, 14, 24, 24, 10]
    TABLE_2_SLICE = [12, 29]
    TABLE_3_1_SLICE = [2, 29, 31, 5]
    TABLE_3_2_SLICE = [4, 17, 21]
    TABLE_3_3_SLICE = [11]
    LAST_SLICE = [9]
    PAGE_NUMBER = 0

    # table
    SURVEY_ID = [0, 11]
    SURVEY_PAGE = [12, 13]
    SURVEY_TOTAL_PAGES = [13, 14]

    CROP_MARKETING_TOKEN = [55, 72]

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
            raise NotImplementedError('Survey data size error')
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
                raise NotImplementedError('Survey create error')
        self.survey = survey

    def build_phone(self):
        try:
            string = self.string[0]
            phones = string[23:44].replace("#", "").split("/")
        except ValueError:
            raise NotImplementedError('Phone data size error')
        else:
            try:
                for number in phones:
                    if len(number) > 0:
                        Phone.objects.create(
                            survey=self.survey,
                            phone=number
                        )
            except ValueError:
                raise NotImplementedError('Phone create error')

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
            raise NotImplementedError('Address Match data size error')
        else:
            try:
                AddressMatch.objects.create(
                    survey=self.survey,
                    match=match,
                    different=different,
                    address=address
                )
            except ValueError:
                raise NotImplementedError('AddressMatch create error')







# builder.survey

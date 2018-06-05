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
            if len(management_str) != 14:
                raise StringLengthError('management')
        except ValueError:
            raise StringLengthError('management')
        else:
            try:
                for i in range(0,14):
                    if management_str[i] == "1":
                        num = i + 1
                        management_type = ManagementType.objects.get(id=num)
                        self.survey.management_types.add(management_type)

            except ValueError:
                raise CreateModelError('management')

    def build_crop_marketing(self):

        string = self.string[2]
        if len(string)% 25 != 0 :
            raise StringLengthError('CropMarketing')
        else:
            try:
                self.crop_marketing = []
                num = int(len(string)/ 25)
                for i in range(0,num):
                    crop_marketing = string[i*25:i*25+25]
                    product_str = crop_marketing[0:4]

                    try:
                        product = Product.objects.get(code=product_str)
                    except Product.DoesNotExist:
                        product = None

                    land_number = int(crop_marketing[4:5])
                    land_area = int(crop_marketing[5:9])
                    plant_times =  int(crop_marketing[9:10])
                    unit_str = int(crop_marketing[10:11])
                    try:
                        unit = Unit.objects.get(code=unit_str , type = 1)
                    except Unit.DoesNotExist:
                        unit = None
                    total_yield = int(crop_marketing[11:18])
                    unit_price = int(crop_marketing[18:23])
                    has_facility_str = int(crop_marketing[23:24])
                    if has_facility_str == 0 :
                        has_facility = None
                    elif has_facility_str == 1 :
                        has_facility = 1
                    else:
                        has_facility = 0

                    loss_str = int(crop_marketing[24:25])
                    try:
                        loss = Loss.objects.get(code=loss_str, type = 1)
                    except Unit.DoesNotExist:
                        loss = None

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
            except ValueError:
                raise CreateModelError('CropMarketing')

    def build_livestock_marketing(self):

        string = self.string[3]
        livestock_str=string[:-22]
        if len(string)% 24 != 0 :
            raise StringLengthError('LivestockMarketing')
        else:
            try:
                self.livestock_marketing = []
                num = int(len(livestock_str)/ 24)
                for i in range(0,num):
                    livestock_marketing = livestock_str[i*24:i*24+24]
                    product_str = livestock_marketing[0:4]

                    try:
                        product = Product.objects.get(code=product_str)
                    except Product.DoesNotExist:
                        product = None

                    unit_str = int(livestock_marketing[4:5])
                    try:
                        unit = Unit.objects.get(code=unit_str , type = 2)
                    except Unit.DoesNotExist:
                        unit = None
                    raising_number = int(livestock_marketing[5:11])
                    total_yield = int(livestock_marketing[11:17])
                    unit_price = int(livestock_marketing[17:22])

                    contract_str = int(livestock_marketing[22:23])
                    try:
                        contract = Contract.objects.get(code=contract_str)
                    except Contract.DoesNotExist:
                        contract = None

                    loss_str = int(livestock_marketing[23:24])
                    try:
                        loss = Loss.objects.get(code=loss_str, type = 2)
                    except Unit.DoesNotExist:
                        loss = None

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
            except ValueError:
                raise CreateModelError('LivestockMarketing')

















# builder.survey

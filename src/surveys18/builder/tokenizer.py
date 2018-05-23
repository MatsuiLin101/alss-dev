from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.dates import MONTHS
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


BASE_SLICE = 48
TABLE_1_SLICE = [26, 9, 14, 24, 24, 10]
TABLE_2_SLICE = [12, 29]
TABLE_3_1_SLICE = [2, 29, 31, 5]
TABLE_3_2_SLICE = [4, 17, 21]
TABLE_3_3_SLICE = [11]
LAST_SLICE = [9]
PAGE_NUMBER = 0

def TokenSize(InputString):
    InputString="1122333332"
    log=""
    delimiter_plus = '+'
    delimiter_pound = '#'

    Slices = InputString.split(delimiter_plus)
    Slices_Pound = InputString.split(delimiter_pound)
    if len(Slices) != 12 or len(Slices_Pound) != 6:
        log += str("Total slice size error,")
        return log
    else:
        for StringLen in range(0,len(Slices)):
            if StringLen == 0:
                print(list(Slices[StringLen])[0:5])








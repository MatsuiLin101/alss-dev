import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Survey
from surveys18.api.serializers import(
    SurveySerializer,
)



@csrf_exempt
def get_surveys(request):
    farmer_id = request.POST.get('fid')
    readonly = json.loads(request.POST.get('readonly', 'false'))
    surveys = Survey.objects.filter(farmer_id=farmer_id, readonly=readonly)
    data = SurveySerializer(surveys, many=True).data
    return JsonResponse(data, safe=False)


@csrf_exempt
def set_surveys(request):
    data = json.loads(request.POST.get('data'))
    stream = BytesIO(JSONRenderer().render(data))
    native_data = JSONParser().parse(stream)
    print(native_data)

    surveys = SurveySerializer(data=native_data, many=True)

    if surveys.is_valid():
        print(surveys)
    else:
        print(surveys.errors)

    return JsonResponse(data, safe=False)

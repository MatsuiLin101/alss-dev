from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Survey
from surveys18.api.serializers import(
    SurveySerializer,
)


@csrf_exempt
def get_surveys(request, fid):
    surveys = Survey.objects.filter(farmer_id=fid)
    data = SurveySerializer(surveys, many=True).data
    return JsonResponse(data, safe=False)

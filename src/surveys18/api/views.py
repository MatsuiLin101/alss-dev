import json
import logging
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import Q

from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
)
from rest_framework.exceptions import (
    ValidationError,
)

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
from rest_framework.permissions import (
    IsAuthenticated,
)

from rest_framework import pagination

from .serializers import SurveySerializer
from surveys18.models import(
    Survey,
    ShortTermHire,
    LongTermHire,
    NumberWorkers,
    WorkType,
    AgeScope,
)

from . import serializers_singleton

review_logger = logging.getLogger('review')
system_logger = logging.getLogger('system')


class SurveyPagination(pagination.PageNumberPagination):
    page_size = 30


class SurveyListAPIView(ListAPIView):
    serializer_class = SurveySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    permission_classes = [IsAuthenticated]
    pagination_class = SurveyPagination
    search_fields = ['farmer_id']

    def get_queryset(self, *args, **kwargs):
        queryset_list = Survey.objects.all()
        fid = self.request.GET.get('fid')
        readonly = json.loads(self.request.GET.get('readonly', 'false'))
        if fid:
            queryset_list = queryset_list.filter(
                    Q(farmer_id=fid) & Q(readonly=readonly)
                    ).distinct()
        return queryset_list


class SurveyUpdateAPIView(UpdateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return Survey.objects.get(id=pk)

    def patch(self, request):
        try:
            data = json.loads(request.data.get('data'))
            pk = data.get('id')
            survey = self.get_object(pk)
            serializer = SurveySerializer(survey,
                                          data=data,
                                          partial=True)  # set partial=True to update a data partially
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(data=serializer.data)
            else:
                review_logger.error(serializer.errors, extra={
                    'object_id': pk,
                    'content_type': ContentType.objects.filter(app_label='surveys18', model='survey').first(),
                    'user': request.user,
                })
                raise ValidationError(serializer.errors)

        except Exception as e:
            system_logger.exception(e)
            return JsonResponse(data=e, safe=False)


# serializer singleterm

class SurveySingleListAPIView(ListAPIView):
    serializer_class = serializers_singleton.SurveySerializer
    queryset = Survey.objects.all()
    permission_classes = [IsAuthenticated]


class ShortTermHireSingleListAPIView(ListAPIView):
    serializer_class = serializers_singleton.ShortTermHireSerializer
    queryset = ShortTermHire.objects.all()
    permission_classes = [IsAuthenticated]


class LongTermHireSingleListAPIView(ListAPIView):
    serializer_class = serializers_singleton.LongTermHireSerializer
    queryset = LongTermHire.objects.all()
    permission_classes = [IsAuthenticated]


class NumberWorkersSingleListAPIView(ListAPIView):
    serializer_class = serializers_singleton.NumberWorkersSerializer
    queryset = NumberWorkers.objects.all()
    permission_classes = [IsAuthenticated]


class WorkTypeSingleListAPIView(ListAPIView):
    serializer_class = serializers_singleton.WorkTypeSerializer
    queryset = WorkType.objects.all()
    permission_classes = [IsAuthenticated]


class AgeScopeSingleListAPIView(ListAPIView):
    serializer_class = serializers_singleton.AgeScopeSerializer
    queryset = AgeScope.objects.all()
    permission_classes = [IsAuthenticated]

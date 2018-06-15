import json
import logging
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import Q

from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
)

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
from rest_framework.permissions import (
    IsAuthenticated,
)

from .serializers import SurveySerializer
from surveys18.models import Survey

logger = logging.getLogger('review')


class SurveyListAPIView(ListAPIView):
    serializer_class = SurveySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    permission_classes = [IsAuthenticated]
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
            logger.exception(serializer.errors, extra={
                'object_id': pk,
                'content_type': ContentType.objects.filter(app_label='surveys18', model='survey').first(),
                'user': request.user,
            })

        return JsonResponse(data=serializer.errors, safe=False)


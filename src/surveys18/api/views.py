import json
from django.db.models import Q
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
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


class SurveyDetailAPIView(RetrieveAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    lookup_field = 'farmer_id'
    permission_classes = [IsAuthenticated]


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

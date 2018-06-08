import csv
from rest_framework.generics import (
    CreateAPIView,
)

from rest_framework.permissions import IsAuthenticated
from .serializers import BuilderFieldSerializer
from surveys18.models import BuilderFile


class BuilderFileCreateAPIView(CreateAPIView):
    queryset = BuilderFile.objects.all()
    serializer_class = BuilderFieldSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.is_valid():
            datafile = self.request.data.get('datafile')
            serializer.save(user=self.request.user,
                            datafile=datafile)
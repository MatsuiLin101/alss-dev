from rest_framework.generics import (
    CreateAPIView,
)

from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from .serializers import BuilderFileSerializer
from surveys18.models import BuilderFile


class BuilderFileCreateAPIView(CreateAPIView):
    queryset = BuilderFile.objects.all()
    serializer_class = BuilderFileSerializer
    # permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        if serializer.is_valid():
            datafile = self.request.data.get('datafile')
            token = self.request.data.get('token')
            user = self.request.user
            if not isinstance(user, User):
                user = None

            serializer.save(user=user,
                            datafile=datafile, token=token)
        else:
            print(serializer.errors)
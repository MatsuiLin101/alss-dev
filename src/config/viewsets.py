from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from config.permissions import IsSuperUser


class StandardViewSet(ModelViewSet):

    def get_permissions(self):
        if self.request.method in ['GET']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsSuperUser]
        return [permission() for permission in permission_classes]

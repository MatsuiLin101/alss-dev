from django.conf.urls import url

from .views import (
    ReviewLogViewSet,
    ReviewLogUpdateAPIView,
)

urlpatterns = [
    url(r'^$', ReviewLogViewSet.as_view({'get': 'list'}), name='list'),
    url(r'^update/$', ReviewLogUpdateAPIView.as_view(), name='update'),
]
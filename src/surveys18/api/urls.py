from django.conf.urls import url

from .views import (
    SurveyListAPIView,
)

urlpatterns = [
    url(r'^$', SurveyListAPIView.as_view(), name='list'),
]
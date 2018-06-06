from django.conf.urls import url

from .views import (
    SurveyListAPIView,
    SurveyUpdateAPIView,
)

urlpatterns = [
    url(r'^$', SurveyListAPIView.as_view(), name='list'),
    url(r'^update/$', SurveyUpdateAPIView.as_view(), name='update'),
]
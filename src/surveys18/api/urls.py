from django.conf.urls import url

from .views import (
    SurveyListAPIView,
    SurveyUpdateAPIView,
    SurveySingleListAPIView,
    ShortTermHireSingleListAPIView,
    LongTermHireSingleListAPIView,
    NumberWorkersSingleListAPIView,
    AgeScopeSingleListAPIView,
    WorkTypeSingleListAPIView,
)

urlpatterns = [
    url(r'^$', SurveyListAPIView.as_view(), name='list'),
    url(r'^update/$', SurveyUpdateAPIView.as_view(), name='update'),

    # serializer singleterm
    url(r'^survey/$', SurveySingleListAPIView.as_view(), name='list-survey'),
    url(r'^shorttermhire/$', ShortTermHireSingleListAPIView.as_view(), name='list-single-shorttermhire'),
    url(r'^longtermhire/$', LongTermHireSingleListAPIView.as_view(), name='list-single-longtermhire'),
    url(r'^numberworkers/$', NumberWorkersSingleListAPIView.as_view(), name='list-single-numberworkers'),
    url(r'^worktype/$', WorkTypeSingleListAPIView.as_view(), name='list-single-worktype'),
    url(r'^agescope/$', AgeScopeSingleListAPIView.as_view(), name='list-single-agescope'),
]

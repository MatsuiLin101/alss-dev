from django.conf.urls import url

from .views import (
    SurveyListAPIView,
    SurveyUpdateAPIView,

    ContentTypeSingletonListAPIView,
    SurveySingletonListAPIView,
    ShortTermHireSingletonListAPIView,
    LongTermHireSingletonListAPIView,
    NumberWorkersSingletonListAPIView,
    AgeScopeSingletonListAPIView,
    WorkTypeSingletonListAPIView,
)

urlpatterns = [
    url(r'^$', SurveyListAPIView.as_view(), name='list'),
    url(r'^update/$', SurveyUpdateAPIView.as_view(), name='update'),
    # serializer singleton
    url(r'^survey/$', SurveySingletonListAPIView.as_view(), name='list_singleton_survey'),
    url(r'^contenttype/$', ContentTypeSingletonListAPIView.as_view(), name='list_singleton_contenttype'),
    url(r'^shorttermhire/$', ShortTermHireSingletonListAPIView.as_view(), name='list_singleton_shorttermhire'),
    url(r'^longtermhire/$', LongTermHireSingletonListAPIView.as_view(), name='list_singleton_longtermhire'),
    url(r'^numberworkers/$', NumberWorkersSingletonListAPIView.as_view(), name='list_singleton_numberworkers'),
    url(r'^worktype/$', WorkTypeSingletonListAPIView.as_view(), name='list_singleton_worktype'),
    url(r'^agescope/$', AgeScopeSingletonListAPIView.as_view(), name='list_singleton_agescope'),
]

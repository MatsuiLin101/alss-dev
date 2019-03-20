from django.conf.urls import url, include

from .views import Surveys2019Index

urlpatterns = [
    url(r'^$', Surveys2019Index.as_view(), name='surveys19_index'),
    url(r'^api/', include('apps.surveys19.api.urls', namespace='api')),
]

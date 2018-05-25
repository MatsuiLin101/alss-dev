from django.conf.urls import url
from .views import (
    get_surveys,
)

urlpatterns = [
    url(r'^get-surveys/(?P<fid>\d+)/$', get_surveys, name='get_surveys'),
]
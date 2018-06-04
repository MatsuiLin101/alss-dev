from django.conf.urls import url
from .views import (
    get_surveys,
    set_surveys,
)

urlpatterns = [
    url(r'^get-surveys/$', get_surveys, name='get_surveys'),
    url(r'^set-surveys/$', set_surveys, name='set_surveys'),
]
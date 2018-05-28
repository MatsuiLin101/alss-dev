from django.conf.urls import url
from .views import (
    get_surveys,
)

urlpatterns = [
    url(r'^get-surveys/$', get_surveys, name='get_surveys'),
]
from django.conf.urls import url, include

from .api import api

urlpatterns = [
    url(r'^', include(api.urls)),
]

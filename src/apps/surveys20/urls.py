from django.urls import path
from django.conf.urls import include
from .api import api

from .views import Surveys2020Index

app_name = "surveys20"

urlpatterns = [
    path("", Surveys2020Index.as_view(), name="surveys20_index"),
    path("api/", include(api.urls)),
]

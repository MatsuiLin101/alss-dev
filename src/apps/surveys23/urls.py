from django.urls import path
from django.conf.urls import include
from .api import api

from .views import Surveys2022Index

app_name = "surveys23"

urlpatterns = [
    path("", Surveys2022Index.as_view(), name="surveys23_index"),
    path("api/", include(api.urls)),
]

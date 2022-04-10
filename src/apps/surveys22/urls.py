from django.urls import path
from django.conf.urls import include
from .api import api

from .views import Surveys2022Index

app_name = "surveys22"

urlpatterns = [
    path("", Surveys2022Index.as_view(), name="surveys22_index"),
    path("api/", include(api.urls)),
]

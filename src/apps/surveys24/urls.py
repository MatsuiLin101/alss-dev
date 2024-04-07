from django.urls import path
from django.conf.urls import include
from .api import api

from .views import Surveys2024Index

app_name = "surveys24"

urlpatterns = [
    path("", Surveys2024Index.as_view(), name="surveys24_index"),
    path("api/", include(api.urls)),
]

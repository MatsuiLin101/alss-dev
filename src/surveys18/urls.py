from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include('surveys18.api.urls', namespace='api')),
]
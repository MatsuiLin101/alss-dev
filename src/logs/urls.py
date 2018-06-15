from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include('logs.api.urls', namespace='api')),
]
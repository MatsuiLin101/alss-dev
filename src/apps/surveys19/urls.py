from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include('apps.surveys19.api.urls', namespace='api')),
]

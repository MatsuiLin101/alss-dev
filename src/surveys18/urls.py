from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include('surveys18.api.urls', namespace='api')),
    url(r'^builder/', include('surveys18.builder.urls', namespace='builder')),
]
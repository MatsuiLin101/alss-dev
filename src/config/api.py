from rest_framework.routers import DefaultRouter
from .views import ExportViewSet, SessionViewSet

api = DefaultRouter()
api.trailing_slash = "/?"

api.register(r"session", SessionViewSet, basename='session')
api.register(r"export", ExportViewSet, basename='export')

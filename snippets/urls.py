from django.urls import path, include
from rest_framework.routers import DefaultRouter

from snippets import views

app_name = 'snippets'

router = DefaultRouter()
router.register('snippets', views.SnippetsViewSet)

urlpatterns = [
    path('', include(router.urls))
]

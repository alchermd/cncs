from django.urls import path, include
from rest_framework.routers import DefaultRouter

from snippets import views

app_name = 'snippets'

router = DefaultRouter()
router.register('snippets', views.SnippetsViewSet)

urlpatterns = [
    path('snippets/<pk>/set-password/', views.set_password, name='snippet-set-password'),
    path('snippets/languages/', views.language_list, name='language-list'),
    path('', include(router.urls)),
]

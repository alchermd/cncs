from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('accounts/', views.account_list, name='account-list'),
    path('accounts/<pk>/', views.account_detail, name='account-detail'),
]

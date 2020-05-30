from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('accounts/', views.account_list, name='account-list'),
    path('accounts/<pk>/', views.account_detail, name='account-detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]

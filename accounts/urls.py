from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
]
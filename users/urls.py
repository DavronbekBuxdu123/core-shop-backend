from django.urls import path
from .views import UserRegisterApiView,ForgotPasswordView,ResetPasswordView

urlpatterns = [
    path('register/', UserRegisterApiView.as_view(), name='user_register'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]
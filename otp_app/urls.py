from django.urls import path

from otp_app import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
app_name = "otp_app"



urlpatterns = [
    path('api/register/', views.UserRegisterView.as_view(), name="register"),
    path('api/profile/', views.UserView.as_view(), name="userView"),
    path('api/generate/', views.GenerateOtpSeretView.as_view(), name="generate"),
    path('api/verify/', views.VerifyOtpView.as_view(), name="verify"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
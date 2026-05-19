from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    UserProfileDetailView,
    GenerateCodeView,
    WorkoutViewSet,  # შემოგვაქვს ახალი ვიუები
    ExerciseViewSet,
    SetViewSet,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)

# ვქმნით როუტერს და ვარეგისტრირებთ ჩვენს ViewSet-ებს
router = DefaultRouter()
router.register(r'workouts', WorkoutViewSet, basename='workout')
router.register(r'exercises', ExerciseViewSet, basename='exercise')
router.register(r'sets', SetViewSet, basename='set')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/me/', UserProfileDetailView.as_view(), name='user_profile'),
    path('generate-code/', GenerateCodeView.as_view(), name='generate_code'),
    path('', include(router.urls)),
    path("password-reset/request/", PasswordResetRequestView.as_view(), name="password_reset_request"),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
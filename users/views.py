import random

from django.core.cache import cache
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status, generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Workout, Exercise, Set
from .permissions import IsOwnerOnly
from .serializers import (
    RegisterSerializer,
    UserProfileSerializer,
    WorkoutSerializer,
    ExerciseSerializer,
    SetSerializer,
)

User = get_user_model()


@extend_schema(tags=["Auth"])
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=RegisterSerializer, responses={201: RegisterSerializer})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "მომხმარებელი წარმატებით დარეგისტრირდა!"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Profile"])
class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOnly]

    def get_object(self):
        return self.request.user


@extend_schema(tags=["Redis"])
class GenerateCodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        generated_code = str(random.randint(1000, 9999))

        cache_key = f"user_{user_id}_code"
        cache.set(cache_key, generated_code, timeout=3600)

        return Response(
            {
                "message": "კოდი გენერირებულია და ვალიდურია 1 საათის განმავლობაში.",
                "code": generated_code,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Workout"])
class WorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user).order_by("-date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=["Exercise"])
class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@extend_schema(tags=["Set"])
class SetViewSet(viewsets.ModelViewSet):
    serializer_class = SetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Set.objects.filter(workout__user=self.request.user)
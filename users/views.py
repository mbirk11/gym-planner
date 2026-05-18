import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions, viewsets
from django.core.cache import cache
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema

from .serializers import RegisterSerializer, UserProfileSerializer, WorkoutSerializer, ExerciseSerializer, SetSerializer
from .models import Workout, Exercise, Set
from .permissions import IsOwnerOnly

User = get_user_model()


# 1. რეგისტრაცია (APIView)
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=RegisterSerializer, responses={201: RegisterSerializer})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "მომხმარებელი წარმატებით დარეგისტრირდა!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. პროფილის CRUD (Generic View - RetrieveUpdateDestroy)
class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOnly]

    def get_object(self):
        return self.request.user


# 3. Redis 4-ნიშნა კოდის გენერაცია (APIView)
class GenerateCodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # მხოლოდ ავტორიზებულებისთვის

    def get(self, request):
        user_id = request.user.id
        # 4-ნიშნა შემთხვევითი კოდის გენერაცია
        generated_code = str(random.randint(1000, 9999))

        # კოდის შენახვა რეიდისში უნიკალური ქიით 1 საათით (3600 წამი)
        cache_key = f"user_{user_id}_code"
        cache.set(cache_key, generated_code, timeout=3600)

        return Response({
            "message": "კოდი გენერირებულია და ვალიდურია 1 საათის განმავლობაში.",
            "code": generated_code
        }, status=status.HTTP_200_OK)


class WorkoutViewSet(viewsets.ModelViewSet):

    #აქედან მომხმარებლები ნახავენ სხვების ვარჯიშებს და ჩაწერენ თავისას.
    #IsAuthenticatedOrReadOnly ნიშნავს: ნახვა შეუძლია ყველას, ჩაწერა მხოლოდ სისტემაში შესულს.


    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        # ვარჯიშის შექმნისას, ბაზაში იუზერის ველში ავტომატურად ჩაიწერება ის, ვინც სისტემაშია შესული
        serializer.save(user=self.request.user)


class ExerciseViewSet(viewsets.ModelViewSet):

    #სავარჯიშოების ბაზა (მაგალითად: აზიდვები, ჩაჯდომები და ა.შ.)

    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SetViewSet(viewsets.ModelViewSet):
    serializer_class = SetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Set.objects.filter(workout__user=self.request.user)
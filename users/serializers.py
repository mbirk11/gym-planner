from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Workout, Exercise, Set

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'height', 'weight', 'birth_date']

    def create(self, validated_data):
        # ვქმნით მომხმარებელს ჰეშირებული პასვორდით
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'height', 'weight', 'birth_date']
        read_only_fields = ['username', 'email'] # იუზერნეიმის და იმეილის შეცვლა აიკრძალოს

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'

class SetSerializer(serializers.ModelSerializer):
    exercise_name = serializers.ReadOnlyField(source='exercise.name')

    class Meta:
        model = Set
        fields = ['id', 'exercise', 'exercise_name', 'weight', 'reps']

class WorkoutSerializer(serializers.ModelSerializer):
    sets = SetSerializer(many=True, read_only=True)
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Workout
        fields = ['id', 'user', 'username', 'date', 'notes', 'sets']
        read_only_fields = ['user']
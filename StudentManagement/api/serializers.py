from rest_framework import serializers
from superadmin.models import *
from django.contrib.auth.models import User

class UserSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class CourseSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name')
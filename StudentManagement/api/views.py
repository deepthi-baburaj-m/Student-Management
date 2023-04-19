from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth import login, logout, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.db.models import Q
from django.contrib.auth.models import User

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user_type = request.POST.get("user_type")
    if user_type == "student":
        staff=False
        superuser=False
        student=True
    elif user_type == "teacher":
        staff=True
        superuser = False
        student = False
    elif user_type == "superuser":
        staff=False
        superuser = True
        student = False
    try:
        user=User.objects.get(username=username,password=password,is_staff=staff,is_superuser=superuser)
    except:
        user=User.objects.create(username=username,password=password,is_staff=staff,is_superuser=superuser)

    if superuser == True:
        course = Course.objects.all()
        student = User.objects.filter(is_staff=False, is_superuser=False)
        staff = User.objects.filter(is_staff=True, is_superuser=False)
        c = CourseSerilaizer(course, many=True)
        teach = UserSerilaizer(staff, many=True)
        stu = UserSerilaizer(student, many=True)
        data = {'status': True, 'staff': teach.data, 'student': stu.data, 'course': c.data}
    if staff == True:
        student = User.objects.filter(is_staff=False, is_superuser=False)
        stu = UserSerilaizer(student, many=True)
        data = {'status': True, 'student': stu.data}
    if student == True:
        course = Course.objects.all()
        c = CourseSerilaizer(course, many=True)
        data = {'status': True, 'course': c.data}
    return Response(data)



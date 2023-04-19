from .helper import renderhelper
from django.contrib.auth import login, logout, authenticate  # add this
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from .models import *
from django.db.models import Q
from django.db import transaction
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User

PAGINATION_COUNT=10

def login_view(request):
    context = {}
    username = request.session.get("username")
    if username:
        return redirect('dashboard')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password,is_superuser=True)
            if user is not None:
                request.session['username'] = user.username
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, "Username or password is incorrect")
        return renderhelper(request, 'main', 'login', context)


@login_required(login_url="login")
def course_update(request, course_id=None):
    context = {}
    section = 'course'
    if course_id:
        try:
            course = Course.objects.get(id=course_id)
            section = 'update'
            context['course'] = course
        except Course.DoesNotExist:
            course = None
    else:
        course = Course()
        section = 'create'
    if request.method == "POST":
        name = request.POST['name']
        try:
            with transaction.atomic():
                if name:
                    course.name = name
                course.save()
        except Exception as error:
            section = "error"
        if section == "create":
            messages.info(request, "Course created successfully")
        elif section == "update":
            messages.info(request, "Course updated successfully")
        elif section == "error":
            messages.info(request, 'Something went wrong')
        return redirect("course_view")
    else:
        return renderhelper(request, 'course', 'course_create', context)

@login_required(login_url="login")
def course_view(request):
    context = {}
    page = request.GET.get("page", 1)
    search = request.GET.get("search")
    delete = request.GET.get("delete")
    course = Course.objects.all().order_by("-id")
    if search:
        course = course.filter(name__icontains=search)
    if delete:
        course_id = request.GET.get("course_id")
        if course_id:

            try:
                courses = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                courses = None
            if courses:
                courses.delete()
    paginator = Paginator(course, PAGINATION_COUNT)
    try:
        course = paginator.get_page(page)
    except PageNotAnInteger:
        course = paginator.get_page(1)
    except EmptyPage:
        course = paginator.get_page(paginator.num_pages)
    context['course_list'] = course
    context['page'] = page
    return renderhelper(request, 'course', 'course_view', context)


@login_required(login_url="login")
def staff_update(request, staff_id=None):
    context = {}
    section = 'staff'
    if staff_id:
        try:
            staff = User.objects.get(id=staff_id)
            section = 'update'
            context['staff'] = staff
        except User.DoesNotExist:
            staff = None
    else:
        staff = User(is_staff=True)
        section = 'create'
    if request.method == "POST":
        name = request.POST['name']
        try:
            with transaction.atomic():
                if name:
                    staff.name = name
                staff.save()
        except Exception as error:
            section = "error"
        if section == "create":
            messages.info(request, "Staff created successfully")
        elif section == "update":
            messages.info(request, "Staff updated successfully")
        elif section == "error":
            messages.info(request, 'Something went wrong')
        return redirect("staff_view")
    else:
        return renderhelper(request, 'staff', 'staff_create', context)

@login_required(login_url="login")
def staff_view(request):
    context = {}
    page = request.GET.get("page", 1)
    search = request.GET.get("search")
    delete = request.GET.get("delete")
    staff = User.objects.all().order_by("-id")
    if search:
        staff = staff.filter(name__icontains=search)
    if delete:
        staff_id = request.GET.get("staff_id")
        if staff_id:

            try:
                staffs = User.objects.get(id=staff_id)
            except User.DoesNotExist:
                staffs = None
            if staffs:
                staffs.delete()
    paginator = Paginator(staff, PAGINATION_COUNT)
    try:
        staff = paginator.get_page(page)
    except PageNotAnInteger:
        staff = paginator.get_page(1)
    except EmptyPage:
        staff = paginator.get_page(paginator.num_pages)
    context['staff_list'] = staff
    context['page'] = page
    return renderhelper(request, 'staff', 'staff_view', context)
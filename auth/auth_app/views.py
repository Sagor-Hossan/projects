from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from .models import *
# Create your views here.

def signup(r):
    if r.method=='POST':
        first_name = r.POST.get('first_name')
        last_name = r.POST.get('last_name')
        username = r.POST.get('username')
        email = r.POST.get('email')
        password = r.POST.get('password')
        confirm_password = r.POST.get('confirm_password')
        is_staff = r.POST.get('is_staff', False) == 'on'
        is_active = r.POST.get('is_active', False) == 'on'
        # print(first_name,last_name,username,email,password,is_staff,is_active)
        if password==confirm_password:
            user = customUser.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                is_active=is_active,
                is_staff=is_staff,
            )          
            user.save()
            return redirect('signin')

    return render(r,"signup.html")

def signin(r):
    if r.method=='POST':
        username = r.POST.get('username')
        password = r.POST.get('password')

        user = authenticate(username=username,password=password)
        if user:
            login(r,user)
            return redirect('home')
    return render(r,'signin.html')

def home(r):
    return render(r,'home.html')

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        is_staff = request.POST.get('is_staff', False) == 'on'
        is_active = request.POST.get('is_active', False) == 'on'
        
        if password == confirm_password:
            user = customUser.objects.create_user(
                username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.is_staff = is_staff
            user.is_active = is_active
            user.save()
            
            login(request, user)
            
            return redirect('home')
    
    return render(request, 'signup.html')
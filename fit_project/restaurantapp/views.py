from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .models import *
from fit_app.models import *
from django.db.models import Q
# from fit_app.models import customUser


def restaurant_signup(r):
    if r.method=='POST':
        name = r.POST['name']
        email = r.POST['email']
        password = r.POST['password']
        profile_pic = r.FILES['profile_pic']

        user = customUser.objects.create_user(
            username=email,
            email=email,
            password=password,
            name=name,
            user_type='restaurant',
            profile_pic=profile_pic)
        user.save()
        
        if user:
            login(r,user)
            return redirect('dashboard')
    return render(r,'resturant/signup.html')

def restaurant_login(r):
    if r.method=='POST':
        email = r.POST['email']
        password = r.POST['password']

        user = authenticate(username=email,password=password)
        if user:
            login(r,user)
            return redirect('dashboard')
    return render(r,'resturant/signin.html')

def restaurant_signout(r):
    logout(r)
    return redirect('restaurant_login')

@login_required
def dashboard(r):
    
    dashboardVar = addRestaurantFood.objects.filter(user=r.user)
    dashboardDict = {
        'dashboardKey':dashboardVar,
    }
    return render(r,'resturant/dashboard.html', dashboardDict)

def homePage(request):
    return render(request, 'resturant/base.html')

@login_required
def aboutPage(request):
    return render(request, 'resturant/about.html')

@login_required
def servicePage(request):
    return render(request, 'resturant/service.html')

@login_required
def contactPage(request):
    return render(request, 'resturant/contact.html')

@login_required
def afterLoginDashboard(request):
    return render(request, 'resturant/afterLoginDashboard.html')

@login_required
def restaurantForm(request):
    if request.method == "POST":
        food_name = request.POST.get('food_name')
        calories = request.POST.get('calories')
        category = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        image = request.FILES.get('image')

        restaurantFormObj = addRestaurantFood(
            food_name = food_name,
            calories = calories,
            category = category,
            description = description,
            price = price,
            quantity = quantity,
            image = image,
        )
        restaurantFormObj.save()
        return redirect('dashboard')
    return render(request, 'resturant/restaurantForm.html')

@login_required
def viewRestaurantFood(request, id):  
    viewFoodVar = addRestaurantFood.objects.get(id=id)
    viewFoodDict = {
        'viewFoodVar': viewFoodVar,
    }
    return render(request, 'resturant/viewRestaurantFood.html', viewFoodDict)

@login_required
def editRestaurantFood(request, id):
    editFoodVar = addRestaurantFood.objects.filter(id=id)
    editFoodDict = {
        'editFoodKey': editFoodVar
    }
    return render(request, 'resturant/editRestaurantFood.html', editFoodDict)

@login_required
def updateRestaurantFood(request):
    if request.method == "POST":
        id = request.POST.get('id')
        food_name = request.POST.get('food_name')
        calories = request.POST.get('calories')
        category = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        image = request.FILES.get('image')
        image1 = request.POST.get('image1')

        updateFoodObj = addRestaurantFood(
            id = id,
            food_name = food_name,
            calories = calories,
            category = category,
            description = description,
            price = price,
            quantity = quantity,
        )
        if image:
            updateFoodObj.image = image
        else:
            updateFoodObj.image = image1
        updateFoodObj.save()
    return redirect('dashboard')

@login_required
def deleteRestaurantFood(request, id):
    deleteFoodVar = addRestaurantFood.objects.get(id=id)
    deleteFoodVar.delete()
    return redirect('dashboard')
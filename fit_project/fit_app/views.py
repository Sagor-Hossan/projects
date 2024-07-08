from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import date, timedelta, datetime
# from django.core.serializers import serialize
from django.db.models import Q
from django.urls import reverse
import json
from django.db.models import Sum
# from django.http import HttpRequest, HttpResponse

# Create your views here.

def signin(r):
    if r.method=='POST':
        username = r.POST['username']
        password = r.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            login(r,user)
            return redirect('home')

    return render(r,'register/signin.html')

def signup(r):
    if r.method=='POST':
        name = r.POST['name']
        username = r.POST['username']
        password = r.POST['password']
        gender = r.POST['gender']
        dob = r.POST['dob']
        height = r.POST['height']
        weight = r.POST['weight']
        goal = r.POST['goal']
        profile_pic = r.FILES['profile_pic']
        location = r.POST['location']
        phone = r.POST['phone']
        about = r.POST['about']
        email = r.POST['email']

        user = customUser.objects.create_user(
            username=username,
            password=password,
            name=name,
            gender=gender,
            dob=dob,
            height=height,
            weight=weight,
            goal=goal,
            user_type='user',
            profile_pic=profile_pic,
            location=location,
            phone=phone,
            about=about,
            email=email,
        )
        user.save()
        
        if user:
            login(r,user)
            return redirect('home')

    return render(r,'register/signup.html')

def signout(r):
    logout(r)
    return redirect('signin')

def get_weekly_calories(user):
    start_date = date.today() - timedelta(days=7)
    daily_calories = []
    for i in range(8): 
        day = start_date + timedelta(days=i)
        calories = ConsumedCalories.objects.filter(user=user, date=day).aggregate(total_calories=Sum('calorie_consumed'))['total_calories']
        if calories is None:
            calories = 0
        daily_calories.append((day.strftime('%Y-%m-%d'), calories))
    return daily_calories

def get_weekly_bmr(user):
    bmr = userBMR(user)
    start_date = date.today() - timedelta(days=7)
    weekly_bmr = [[(start_date + timedelta(days=i)).strftime('%Y-%m-%d'), bmr] for i in range(8)]
    return weekly_bmr

@login_required
def home(r):
    user = r.user
    weekly_calories = json.dumps(get_weekly_calories(user))
    weekly_bmr = json.dumps(get_weekly_bmr(user))
    bmr = userBMR(user)
    calSum = today_calories(r)
    user = customUser.objects.get(id=r.user.id)
    total_followers = userFollow.objects.filter(follow=user).count()
    return render(r, 'common/home.html', {'weekly_calories': weekly_calories, 'weekly_bmr': weekly_bmr, 'bmr': bmr, 'calSum': calSum, 'total_followers': total_followers})


@login_required
def profilepage(r):
    user = customUser.objects.get(id=r.user.id)
    total_followers = userFollow.objects.filter(follow=user).count()
    total_following = userFollow.objects.filter(user=user).count()

    postdata = userPost.objects.filter(user=user).order_by('-date','-time')
    postLength = postdata.count()
    
    context = {
        'user': user,
        'total_followers': total_followers,
        'total_following': total_following,
        'postdata': postdata,
        'postLength': postLength,
    }
     
    return render(r,'profile/profilepage.html', context)


@login_required
def createPost(r, next=None):
    if r.method=='POST':
        post = r.POST.get('post')  
        post = userPost(user=r.user,post=post)
        post.save()

        for image in r.FILES.getlist('images'):
            postImage(userpost=post,image=image).save()
        if next:
            return redirect(next)

    return redirect(r.META.get('HTTP_REFERER', '/'))
        
    
def comments(r, next=None):
    if r.method == 'POST':
        comment = r.POST.get('comment')
        comment_id = r.POST.get('id') 
        try:
            post = userPost.objects.get(id=comment_id)
        except userPost.DoesNotExist:
            if next:
                return redirect(next)
        comment_data = commentsModel(user=r.user, post=post, comment=comment)
        comment_data.save()

        if next:
            return redirect(next)

    return redirect(r.META.get('HTTP_REFERER', '/'))

@login_required
def postSection(r):
    postdata = userPost.objects.all().order_by('-date', '-time')
    postLength = postdata.count()

    context = {
        'postdata': postdata,
        'postLength': postLength,
    }

    return render(r, 'profile/postSection.html', context)

def unFollow(r, id, next=None):
    follow = userFollow.objects.filter(user=r.user, follow=customUser.objects.get(id=id))
    follow.delete()
    if next:
        return redirect(next)
    else:
        return redirect(r.META.get('HTTP_REFERER', '/'))


@login_required
def editprofile(r):
    user = customUser.objects.get(id=r.user.id)
    if r.method=='POST':
        user.name = r.POST['name']
        user.username = r.POST['username']
        user.dob = r.POST['dob']
        user.height = r.POST['height']
        user.weight = r.POST['weight']
        user.goal = r.POST['goal']
        user.location = r.POST['location']
        user.about = r.POST['about']
        user.phone = r.POST['phone']

        profile_pic = r.FILES.get('profile_pic')
        if profile_pic:
            user.profile_pic = profile_pic
        else:
            profile_pic1 = r.POST.get('profile_pic1')
            if profile_pic1:
                user.profile_pic = profile_pic1

        user.save()
        return redirect('profilepage')

    return render(r,'profile/editprofile.html')

@login_required
def addFood(r):
    if r.method=='POST':
        food_name = r.POST['food_name']
        calories = r.POST['calories']
        image = r.FILES['image']

        food = foodModel(user=r.user,food_name=food_name,calories=calories,image=image)
        food.save()
        return redirect('viewFood')

    return render(r,'foods_by_user/addFood.html')



@login_required
def viewFood(r):
    if 'search1' in r.GET:
        search = r.GET.get('search1')
        if search:
            foods = foodModel.objects.filter(Q(food_name__icontains=search))
            return render(r,'foods_by_user/viewFood.html',{'foods':foods})
        
    foods = foodModel.objects.filter(user=r.user)
    print(r.path)
    return render(r,'foods_by_user/viewFood.html',{'foods':foods})

@login_required
def editFood(r,id):
    food = foodModel.objects.get(id=id)
    if r.method=='POST':
        food.food_name = r.POST['food_name']
        food.calories = r.POST['calories']

        image = r.FILES.get('image')
        if image:
            food.image = image
        else:
            image1 = r.POST.get('image1')
            if image1:
                food.image = image1

        food.save()
        return redirect('viewFood')

    return render(r,'foods_by_user/editFood.html',{'food':food})

@login_required
def deleteFood(r,id):
    food = foodModel.objects.get(id=id)
    food.delete()
    return redirect('viewFood')

def userAge(user):
    if user.user_type ==  'user':
        today = date.today()
        birthdate = user.dob 
        years = today.year - birthdate.year 
        if today.month < birthdate.month or (today.month == birthdate.month and today.day < birthdate.day):
            years -= 1
        
        next_birthday_month = birthdate.month
        next_birthday_year = today.year if today.month > birthdate.month or (today.month == birthdate.month and today.day >= birthdate.day) else today.year - 1
        next_birthday = date(next_birthday_year, next_birthday_month, birthdate.day)
        
        days_since_last_birthday = (today - next_birthday).days
        days_in_year = 366 if next_birthday_year % 4 == 0 else 365
        
        fractional_year = days_since_last_birthday / days_in_year
        total_age = years + fractional_year
        return f"{total_age:.2f}"

def userBMR(user):
    if user.user_type ==  'user':
        age = float(userAge(user))
        # print('age',age)
        if user.gender == 'male':
            bmr = 66.47 + (13.75 * user.weight) + (5.003 * user.height) - (6.755 * age)
        else:
            bmr = 655.1 + (9.563 * user.weight) + (1.850 * user.height) - (4.676 * age)
        return f"{bmr:.2f}"

def today_consumed(r):
    consumed = ConsumedCalories.objects.filter(user=r.user, date=date.today())
    return consumed

def today_calories(r):
    consumed = ConsumedCalories.objects.filter(user=r.user, date=date.today())
    calSum = sum(c.calorie_consumed for c in consumed)
    return calSum

@login_required
def addConsumedCalories(r):
    if r.method=='POST':
        item_name = r.POST['item_name']
        calorie_consumed = float(r.POST['calorie_consumed'])

        consumed = ConsumedCalories(user=r.user,item_name=item_name,calorie_consumed=calorie_consumed)
        consumed.save()
        return redirect('viewConsumedCalories')
    return render(r,'calories/addConsumedCalories.html')


@login_required
def addFoodsCalories(r, id):
    food = foodModel.objects.get(id=id)
    consumed = ConsumedCalories(user=r.user,item_name=food.food_name,calorie_consumed=food.calories)
    consumed.save()
    return redirect('viewConsumedCalories')

@login_required
def addRestFoodsCalories(r, id):
    food = addRestaurantFood.objects.get(id=id)
    consumed = ConsumedCalories(user=r.user,item_name=food.food_name,calorie_consumed=food.calories)
    consumed.save()
    return redirect('viewConsumedCalories')


@login_required
def deleteConsumedCalories(r, id):
    consumed = ConsumedCalories.objects.get(id=id)
    consumed.delete()
    return redirect('viewConsumedCalories')


@login_required
def viewConsumedCalories(r):
    bmr = userBMR(r.user)
    calSum = today_calories(r)
    consumed = today_consumed(r)

    return render(r, 'calories/viewConsumedCalories.html', {'consumed': consumed, 'bmr': bmr, 'calSum': calSum})

@login_required
def friendlist(r):
    if 'search3' in r.GET:
        search = r.GET.get('search3')
        if search:
            data = customUser.objects.filter(user_type='user').exclude(id=r.user.id).filter(Q(name__icontains=search))
            
    else:
        data = customUser.objects.filter(user_type='user').exclude(id=r.user.id)
    
    follow_list = []
    for i in data:
        is_following = userFollow.objects.filter(user=r.user, follow = i).exists()
        follow_list.append((i, is_following))
        
    return render(r, 'friends/friendlist.html',{'follow_list': follow_list})

@login_required
def veiwFriendsProfile(r, id):
    user = customUser.objects.get(id=id)
    total_followers = userFollow.objects.filter(follow=user).count()
    total_following = userFollow.objects.filter(user=user).count()

    postdata = userPost.objects.filter(user=user).order_by('-date','-time')
    postLength = postdata.count()
    weekly_calories = json.dumps(get_weekly_calories(user))
    weekly_bmr = json.dumps(get_weekly_bmr(user))
    context = {
        'user': user,
        'total_followers': total_followers,
        'total_following': total_following,
        'postdata': postdata,
        'postLength': postLength,
        'weekly_calories': weekly_calories,
        'weekly_bmr': weekly_bmr,
    }
    print(user)
    return render(r, 'friends/veiwFriendsProfile.html', context)


@login_required
def userPage(r, id):
    user = customUser.objects.get(id=id)
    return render(r, 'profile/userPage.html', {'user': user})

@login_required
def Follow(r, id):
    follow = userFollow(user=r.user, follow=customUser.objects.get(id=id))
    follow.save()
    
    return redirect('friendlist')

@login_required
def unFollow(r, id, next=None):
    follow = userFollow.objects.filter(user=r.user, follow=customUser.objects.get(id=id))
    follow.delete()
    if next:
        return redirect(next)
    else:
        return redirect(r.META.get('HTTP_REFERER', '/'))
    

@login_required
def followerlist(r):
    user = customUser.objects.get(id=r.user.id)
    followers = userFollow.objects.filter(follow=user)
         
    return render(r, 'friends/followerlist.html',{'followers': followers})

@login_required
def friendFollower(r, id):
    user=customUser.objects.get(username=id)
    followers = userFollow.objects.filter(follow=user)

    # alsoFollowMe = userFollow.objects.filter(user=r.user, follow=follow).exists()

    return render(r, 'friends/friendFollowerList.html',{'followers': followers})
    

@login_required
def friendFollowing(r, id):
    user=customUser.objects.get(username=id)
    followers = userFollow.objects.filter(user = user)
    
    return render(r, 'friends/friendFollowingList.html', {'followers': followers})

@login_required
def deleteFollower(r, userid):  
    follow=customUser.objects.get(username=userid)
    followers = userFollow.objects.get(user = follow,follow=r.user)
    print(followers)
    followers.delete()
    return redirect('followerlist')

@login_required
def followinglist(r):
    user = customUser.objects.get(id=r.user.id)
    following = userFollow.objects.filter(user=user)
    print(following)
         
    return render(r, 'friends/followinglist.html',{'following': following})


@login_required
def restaurantListPage(r):
    if 'search2' in r.GET:
        search = r.GET.get('search2')
        if search:
            restaurant = addRestaurantFood.objects.filter(Q(food_name__icontains=search))
            return render(r, 'foods_by_user/restaurantList.html', {'restaurant': restaurant})

    restaurant = addRestaurantFood.objects.all()

    return render(r, 'foods_by_user/restaurantList.html', {'restaurant': restaurant})


@login_required
def viewrestaurantfood(request, id):
    viewFoodVar = addRestaurantFood.objects.get(id=id)
    viewFoodDict = {
        'viewFoodVar': viewFoodVar,
    }
    return render(request, 'foods_by_user/viewrestaurantfood.html', viewFoodDict)

@login_required
def gymPage(request):
    return render(request, 'fitness/gym.html')

@login_required
def exercisePage(request):
    return render(request, 'fitness/exercise.html')

@login_required
def restOrSleepPage(request):
    return render(request, 'fitness/restOrSleep.html')









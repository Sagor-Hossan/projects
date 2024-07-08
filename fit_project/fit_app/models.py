from django.db import models
from django.contrib.auth.models import AbstractUser

class customUser(AbstractUser):
    GENDER = [('male','Male'),('female','Female')]
    GOAL = [('lose_weight','Lose Weight'),('gain_weight','Gain Weight'),('maintain_weight','Maintain Weight')]

    name = models.CharField(max_length=50,null=True,blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic/',null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    height = models.FloatField(null=True,blank=True)
    weight = models.FloatField(null=True,blank=True)
    gender = models.CharField(max_length=10,choices=GENDER,null=True,blank=True)
    goal = models.CharField(max_length=20,choices=GOAL,null=True,blank=True)
    user_type = models.CharField(max_length=20,null=True,blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.username
    

class userFollow(models.Model):
    user = models.ForeignKey(customUser, on_delete=models.CASCADE, related_name='follower')
    follow = models.ForeignKey(customUser, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return self.user.username + ' follows ' + self.follow.username
    
    
# class userDiet(models.Model):
#     user = models.ForeignKey(customUser, on_delete=models.CASCADE)
#     diet = models.TextField()
#     date = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.user.username
    
class userPost(models.Model):
    user = models.ForeignKey(customUser, on_delete=models.CASCADE)
    post = models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username + ' posted on ' + str(self.date)

class postImage(models.Model):
    userpost = models.ForeignKey(userPost, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_pics/')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.userpost.user.username
    
class commentsModel(models.Model):
    user = models.ForeignKey(customUser, on_delete=models.CASCADE)
    post = models.ForeignKey(userPost, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username


# class userWeight(models.Model):
#     user = models.ForeignKey(customUser,on_delete=models.CASCADE)
#     weight = models.FloatField()
#     date = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.user.username

class ConsumedCalories(models.Model):
    user = models.ForeignKey(customUser, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    calorie_consumed = models.FloatField(default=0)
    date = models.DateField(auto_now_add=True, null=True)
    time = models.TimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.item_name


class foodModel(models.Model):
    user = models.ForeignKey(customUser,on_delete=models.CASCADE)
    food_name = models.CharField(max_length=50)
    calories = models.FloatField(null=True)
    image = models.ImageField(upload_to='food_pics/')

    def __str__(self):
        return self.food_name


class addRestaurantFood(models.Model):
    user = models.ForeignKey(customUser, on_delete=models.CASCADE, null=True)
    food_name = models.CharField(max_length=100)
    calories = models.CharField(max_length=100)
    CATEGORY = [
        ('fruit', 'Fruit'),
        ('vegetable', 'Vegetable'),
        ('grain', 'Grain'),
        ('protein', 'Protein'),
        ('dairy', 'Dairy'),
        ('dessert', 'Dessert'),
        ('beverage', 'Beverage'),
        ('fast_food', 'Fast Food'),
    ]
    category = models.CharField(choices=CATEGORY, max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField()
    quantity = models.CharField(max_length=100)
    image = models.ImageField(upload_to='restaurantFoods')

    def __str__(self):
        return self.food_name
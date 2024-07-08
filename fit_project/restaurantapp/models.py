from django.db import models
from fit_app.models import customUser

# class addRestaurantFood(models.Model):
#     food_name = models.CharField(max_length=100)
#     calories = models.CharField(max_length=100)
#     CATEGORY = [
#         ('fruit', 'Fruit'),
#         ('vegetable', 'Vegetable'),
#         ('grain', 'Grain'),
#         ('protein', 'Protein'),
#         ('dairy', 'Dairy'),
#         ('dessert', 'Dessert'),
#         ('beverage', 'Beverage'),
#     ]
#     category = models.CharField(choices=CATEGORY, max_length=100)
#     description = models.TextField()
#     price = models.PositiveIntegerField()
#     quantity = models.CharField(max_length=100)
#     expiry_date = models.DateField(auto_now=True)
#     image = models.ImageField(upload_to='restaurantFoods')

#     def __str__(self):
#         return self.food_name
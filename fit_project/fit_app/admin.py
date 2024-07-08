from django.contrib import admin
from .models import *

admin.site.register(customUser)
admin.site.register(foodModel)
admin.site.register(userFollow)
admin.site.register(userPost)
admin.site.register(postImage)
admin.site.register(addRestaurantFood)
admin.site.register(commentsModel)

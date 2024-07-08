from django.contrib import admin
from myApp.models import *

class displaycustomuser(admin.ModelAdmin):
    list_display=[
        'username',
    ]
    search_fields=["username",'gender']
    fieldsets=[
        (
            "Customuser Backend",
            {
                "fields":[('username','email','role','gender','city','profile_picture')],
            }
        ),
        (
            "Basic Information",
            {
                'classes':["collapse"],
                'fields':["father_name","mother_name","address"],
            }
        ),
        (
            "Contact Information",
            {
                'classes':["collapse"],
                'fields':["phone","emergency_contact"],
            }
        )
    ]
    
admin.site.register(customuser,displaycustomuser)


# class jobmodeldisplay(admin.ModelAdmin):
#     list_display=[
#         "username"
#     ]
admin.site.register(jobmodel)
admin.site.register(seekerprofilemodel)

# class applyjobmodeldisplay(admin.ModelAdmin):
#     list_display=['applied_by','apply_to','skills']
#     search_fields=["skills","education"]
#     fieldsets=[
#         (
#             "This is my title",
#             {
#                 "fields": [('skills','education','applied_by')]
#             }
#         ),
#         (
#             "Advance Options",
#             {
#                 "classes":["collapse"],
#                 "fields":["apply_to","applied_by"],
#             }
#         )
#     ]
admin.site.register(jobapplymodel)
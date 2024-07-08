from django.conf import settings
from django.conf.urls.static import static


from django.contrib import admin
from django.urls import path
from myProject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    
    
    # authenticate
    path('',signin,name="signin"),
    path('signup/',signup,name="signup"),
    path('signout/',signout,name="signout"),
    
    path('index/',index,name='index'),
    path('dashboard/',dashboard,name='dashboard'),
    
    
    # Job CRUD
    path('addjob/',addjob,name="addjob"),
    path('joblistforall/',joblistforall,name="joblistforall"),
    path('viewjob/<str:myid>',viewjob,name="viewjob"),
    path('deletejob/<str:myid>',deletejob,name="deletejob"),
    path('editjob/<str:myid>',editjob,name="editjob"),
    
    
    path('applyjob/<str:myid>',applyjob,name="applyjob"),
    path('viewapplicant/<str:myid>',viewapplicant,name="viewapplicant"),
    path('appliedjob/',appliedjob,name="appliedjob"),
    
    
    # profile
    path('profile/',profile,name="profile"),
    path('resumeprofile/',resumeprofile,name="resumeprofile"),
    path('postedjob/',postedjob,name="postedjob"),
    path('changepassword/',changepassword,name="changepassword"),
    path('editprofile/',editprofile,name="editprofile"),
    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app.views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),

    
    path('recruiter_dashboard/', recruiter_dashboard, name='recruiter_dashboard'),
    
    path('',dashboard, name='dashboard'),
    path('dashboard/',dashboard, name='dashboard'),
    path('searchJob/',searchJob, name='searchJob'),
    path('profilepage/', profilepage, name='profilepage'),
    path('addjobpage/', addjobpage, name='addjobpage'),
    path('job_list/', job_list, name='job_list'),
    path('apply_job/<int:id>/', apply_job, name='apply_job'),
    path('job_detail/<int:id>/', job_detail, name='job_detail'),
    path('job_delate/<int:id>/', job_delate, name='job_delate'),
    path('editjobspage/<int:id>/', editjobspage, name='editjobspage'),
    path('changepassword/', changepassword, name='changepassword'),
    path('applyedjobpage/', applyedjobpage, name='applyedjobpage'),
    path('applicantspage/<int:id>/',applicantspage, name='applicantspage'),
    path('applicant_reject/<int:id>/',applicant_reject, name='applicant_reject'),
    path('applicant_approved/<int:id>/',applicant_approved, name='applicant_approved'),


    path('jobList/', jobList.as_view()),
    path('jobDetail/<int:pk>/', jobList.as_view()),
    path('customUserList/', customUserList.as_view()),
    path('customUserDetail/<int:pk>/', customUserDetail.as_view()),
    path('jobListApi/',jobListApi),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

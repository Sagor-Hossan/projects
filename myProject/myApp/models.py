from django.db import models
from django.contrib.auth.models import AbstractUser

class customuser(AbstractUser):
    role=[
        ('recruiter','Recruiter'),
        ('job_seeker','JOb_Seeker'),
    ]
    gender=[
        ('male','Male'),
        ('female','Female'),
        ('other','Other'),
    ]
    role=models.CharField(choices=role,max_length=100,null=True)
    city=models.CharField(max_length=100,null=True)
    gender=models.CharField(choices=gender,max_length=100,null=True)
    profile_picture=models.ImageField(upload_to='static/picture/user',null=True)
    
    # Basic Information
    father_name=models.CharField(max_length=100,null=True)
    mother_name=models.CharField(max_length=100,null=True)
    address=models.CharField(max_length=100,null=True)
    
    # Contact
    phone=models.CharField(max_length=20,null=True)
    emergency_contact=models.CharField(max_length=20,null=True)


class jobmodel(models.Model):
    job_title=models.CharField(max_length=100,null=True)
    company_description=models.CharField(max_length=100,null=True)
    company_logo=models.ImageField(upload_to='static/picture/company',null=True)
    company_name=models.CharField(max_length=100,null=True)
    company_location=models.CharField(max_length=100,null=True)
    qualification=models.CharField(max_length=100,null=True)
    deadline=models.CharField(max_length=100,null=True)
    salary=models.CharField(max_length=100,null=True)
    created_by=models.ForeignKey(customuser,on_delete=models.CASCADE,null=True)
    
class seekerprofilemodel(models.Model):
    myuser=models.OneToOneField(customuser,on_delete=models.CASCADE,related_name='SeekerProfileModel',null=True)
    education_qualification=models.CharField(max_length=100,null=True)
    word_experience=models.CharField(max_length=100,null=True)
    
    
    
class jobapplymodel(models.Model):
    applied_by=models.ForeignKey(customuser,on_delete=models.CASCADE,null=True)
    apply_to=models.ForeignKey(jobmodel,on_delete=models.CASCADE,null=True)
    skills=models.CharField(max_length=100,null=True)
    education=models.CharField(max_length=100,null=True)
    resume=models.FileField(upload_to='static/resume',null=True)
from django.db import models
from django.contrib.auth.models import AbstractUser


class customUser(AbstractUser):
    user_type_data = [('Recruiter', 'Recruiter'), ('Jobseeker', 'Jobseeker')]
    user_type = models.CharField(choices=user_type_data, max_length=10)
    Gender = [('male','Male'),('female','Female'),('other','Other')]
    gender=models.CharField(max_length=10,choices=Gender)
    profile_pic=models.ImageField(upload_to='media/profile_pic')
    city=models.CharField(max_length=100)

    def __str__(self):
        return self.username + ' ' + self.user_type
    
class jobModel(models.Model):
    company_name=models.CharField(max_length=100)
    company_logo=models.ImageField(upload_to='media/company_logo')
    company_location=models.CharField(max_length=200)
    job_title=models.CharField(max_length=100)
    job_description=models.TextField()
    job_salary=models.CharField(max_length=100, null=True)
    qualification=models.CharField(max_length=100)
    deadline=models.CharField(max_length=100, null=True)
    user=models.ForeignKey(customUser,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.company_name + ' ' + self.job_title
    
    
class applyJob(models.Model):
    applicant = models.ForeignKey(customUser,on_delete=models.CASCADE)
    job = models.ForeignKey(jobModel,on_delete=models.CASCADE)
    
    skill = models.CharField(max_length=100)
    experience = models.TextField()
    resume = models.FileField(upload_to='media/resume',)
    photo = models.ImageField(upload_to='media/applicant_photo')
    status = models.CharField(max_length=100, default='Pending',null=True)
    def __str__(self) -> str:
        return self.applicant.username +' - '+ self.job.job_title
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash 
from .serializers import *
from rest_framework import mixins
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password= request.POST.get('confirm_password')
        gender = request.POST.get('gender')
        user_type = request.POST.get('user_type')
        city = request.POST.get('city')
        profile_pic = request.FILES.get('profile_pic')

        if password == confirm_password:
            user = customUser.objects.create_user(
                first_name=first_name, 
                last_name=last_name ,
                username=username, 
                email=email, 
                password=password, 
                gender=gender,
                user_type=user_type,
                city=city,
                profile_pic=profile_pic
                )
            user.save()
            messages.success(request, 'User created successfully')
            return redirect('signin')
        else:
            messages.error(request, 'Password and confirm password not matched')
            return redirect('signup')

    return render(request, 'resistretion/signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Username or password is incorrect')
            return redirect('signin')
    return render(request, 'resistretion/signin.html')

@login_required
def signout(request):
    logout(request)
    return redirect('dashboard')

def recruiter_dashboard(request):
    return render(request, 'dashboard/recruiter_dashboard.html')

def dashboard(request):
    counts = 0
    user = request.user
    if not user.is_authenticated:
        jobs = jobModel.objects.all()[0:8]
        counts = jobModel.objects.all().count()
    else:
        if user.user_type == 'Recruiter':
            jobs = jobModel.objects.filter(user=user)[0:4]
            counts = jobModel.objects.filter(user=user).count()
        else:
            jobs = jobModel.objects.all()[0:8]
            counts = jobModel.objects.all().count()
    
    return render(request, 'dashboard/jobseeker_dashboard.html', {'jobs':jobs, 'counts':counts})

def searchJob(request):
    
    search = request.GET.get('search_job')
    search_location = request.GET.get('search_location')
    if search_location and search:      
        jobs = jobModel.objects.filter(
                (Q(job_title__icontains=search) | 
                Q(job_description__icontains=search)
                )&
                (Q(job_title__icontains=search_location) | 
                Q(company_location__icontains=search_location) | 
                Q(company_name__icontains=search_location)
            ))
    elif search:
        jobs = jobModel.objects.filter(
            Q(job_title__icontains=search)|
            Q(company_location__icontains=search) | 
            Q(company_name__icontains=search)|
            Q(job_description__icontains=search)
            )
    elif search_location:
        jobs = jobModel.objects.filter(
            Q(job_title__icontains=search_location) | 
            Q(company_location__icontains=search_location) | 
            Q(company_name__icontains=search_location)
        )   
    else:
        jobs = jobModel.objects.all() 
    return render(request, 'jobs/jobslist.html', {'myJob':jobs})  


def jobListApi(request):
    jobs = jobModel.objects.all()
    serializer = jobModelSerializer(jobs, many=True)
    return HttpResponse(serializer.data)

class jobList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = jobModel.objects.all()
    serializer_class = jobModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class jobDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = jobModel.objects.all()
    serializer_class = jobModelSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

class customUserList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = customUser.objects.all()
    serializer_class = customUserSerializer
    

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class customUserDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = customUser.objects.all()
    serializer_class = customUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

# @login_required
# def recruiter_dashboard(request):
    
#     jobs = jobModel.objects.filter(user=request.user)[0:4]

#     return render(request, 'dashboard/recruiter_dashboard.html',{'jobs':jobs})

@login_required
def profilepage(request):
    user = customUser.objects.get(id=request.user.id)
    return render(request, 'profile/profilepage.html', {'user':user})

@login_required
def addjobpage(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        company_logo = request.FILES.get('company_logo')
        company_location = request.POST.get('company_location')
        job_title = request.POST.get('job_title')
        job_description = request.POST.get('job_description')
        job_salary = request.POST.get('job_salary')
        qualification = request.POST.get('qualification')
        deadline = request.POST.get('deadline')
        user = request.user

        job = jobModel(
            company_name=company_name,
            company_logo=company_logo,
            company_location=company_location,
            job_title=job_title,
            job_description=job_description,
            job_salary=job_salary,
            qualification=qualification,
            deadline=deadline,
            user=user
        )
        job.save()
        messages.success(request, 'Job added successfully')
        return redirect('dashboard')
    
    return render(request, 'jobs/addjobspage.html')


def job_list(request):   
    if not request.user.is_authenticated:
        myJob = jobModel.objects.all()
    else:
        user = request.user
        if user.user_type == 'Recruiter':
            myJob = jobModel.objects.filter(user=user)
        else:
            jobs = jobModel.objects.all()
            myJob = []
            for job in jobs:
                applied_jobs = applyJob.objects.filter(applicant=user, job=job).exists()
                myJob.append((job, applied_jobs))

        # next_url = request.GET.get('next')
        
    return render(request, 'jobs/jobslist.html', {'myJob':myJob})

@login_required
def apply_job(request,id):
    job = get_object_or_404(jobModel, id=id)
    
    if request.method == 'POST':
        skill = request.POST.get('skill')
        experience = request.POST.get('experience')
        resume = request.FILES.get('resume')
        photo = request.FILES.get('photo')
        
        if skill and experience and resume and photo:
            apply = applyJob(
                skill=skill,
                experience=experience,
                resume = resume,
                photo=photo,
                job=job,
                applicant = request.user      
            )
            apply.save()
            return redirect('job_list')
    
    
    return render(request, 'jobs/apply_job.html',{'job':job})
 


def job_detail(request, id):
    job = jobModel.objects.get(id=id)
    return render(request, 'jobs/jobdetail.html', {'job':job})

@login_required
def job_delate(request, id):
    jobModel.objects.get(id=id).delete()
    return redirect('job_list')


@login_required
def editjobspage(request, id):
    job = jobModel.objects.get(id=id)
    if request.method == 'POST':
        id = request.POST.get('id')
        company_name = request.POST.get('company_name')
        company_logo = request.FILES.get('company_logo')
        company_logo1 = request.POST.get('company_logo1')
        company_location = request.POST.get('company_location')
        job_title = request.POST.get('job_title')
        job_description = request.POST.get('job_description')
        job_salary = request.POST.get('job_salary')
        qualification = request.POST.get('qualification')
        deadline = request.POST.get('deadline')
        user=request.user

        jobs = jobModel(
            id=id,
            company_name=company_name,
            company_location=company_location,
            job_title=job_title,
            job_description=job_description,
            job_salary=job_salary,
            qualification=qualification,
            deadline=deadline,
            user=user,
        )
        if company_logo:
            jobs.company_logo = company_logo
        else:
            jobs.company_logo = company_logo1
        jobs.save()
        return redirect('job_list')

    return render(request, 'jobs/editjobspage.html', {'job':job})


@login_required
def changepassword(request):
    if request.method=='POST':
        current_password=request.POST.get('current_password')
        new_password=request.POST.get('new_password')
        confirm_password=request.POST.get('confirm_password')

        if check_password(current_password,request.user.password):
            if new_password==confirm_password:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                return redirect('profilepage')

    return render(request, 'profile/changepassword.html')

@login_required
def applyedjobpage(request):
    user = request.user
    jobs = applyJob.objects.filter(applicant=user)
    return render(request, 'profile/applyedjobpage.html', {'jobs':jobs})


@login_required
def applicantspage(request,id):
    job = get_object_or_404(jobModel, id=id)
    applicants = applyJob.objects.filter(job=job)
    return render(request, 'profile/applicantspage.html',{'applicants':applicants, 'job':job})


@login_required
def applicant_reject(request, id):

    applicant = get_object_or_404(applyJob, id=id)
    applicant.status = 'Rejected'
    applicant.save()

    return redirect('applicantspage',id=applicant.job.id)

@login_required
def applicant_approved(request,id):

    applicant = get_object_or_404(applyJob, id=id)
    applicant.status = 'Approved'
    applicant.save()
    return redirect('applicantspage',applicant.job.id)
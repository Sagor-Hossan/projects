from django.shortcuts import render, redirect, get_object_or_404
from myApp.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash


def signup(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        role=request.POST.get('role')
        city=request.POST.get('city')
        gender=request.POST.get('gender')
        profile_picture=request.FILES.get('profile_picture')
        email=request.POST.get('email')
        
        if password == confirm_password:
            user=customuser.objects.create_user(username=username, password=password)
            user.city=city
            user.role=role
            user.gender=gender
            user.profile_picture=profile_picture
            user.email=email
            if role == 'job_seeker':
                seekerprofilemodel.objects.create(myuser=user).save()
            user.save()
            messages.success(request,'Account Created Successfull')
            return redirect("signin")
    return render(request,'signup.html')


def signin(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username, password=password)
        if user:
            login(request,user)
            messages.success(request,'Login Successfull')
            return redirect("dashboard")
        else:
            messages.warning(request,'Wrong username or password')
    return render(request,'signin.html')





def signout(request):
    logout(request)
    return redirect("signin")




@login_required
def index(request):
    return render(request,'index.html')



@login_required
def dashboard(request):
    return render(request,'dashboard.html')

@login_required
def addjob(request):
    if request.method == 'POST':
        job_title=request.POST.get('job_title')
        company_description=request.POST.get('company_description')
        company_logo=request.FILES.get('company_logo')
        company_name=request.POST.get('company_name')
        company_location=request.POST.get('company_location')
        qualification=request.POST.get('qualification')
        deadline=request.POST.get('deadline')
        salary=request.POST.get('salary')
        current_user=request.user
        myjob=jobmodel(
            job_title=job_title,
            company_description=company_description,
            company_logo=company_logo,
            company_name=company_name,
            company_location=company_location,
            qualification=qualification,
            deadline=deadline,
            salary=salary,
            created_by=current_user,
        )
        myjob.save()
        messages.success(request,'Job add successfull')
        return redirect("joblistforall")
    return render(request,'addjob.html')

@login_required
def joblistforall(request):
    myjob=jobmodel.objects.all()
    current_user=request.user
    data=[]
    for i in myjob:
        already_applid=jobapplymodel.objects.filter(apply_to=i,applied_by=current_user).exists()
        data.append((i,already_applid))
    
    return render(request,'joblistforall.html',{'data':data})

@login_required
def viewjob(request,myid):
    
    job=jobmodel.objects.get(id=myid)
    
    
    return render(request,'viewjob.html',{'job':job})

@login_required
def applyjob(request,myid):
    myjob=get_object_or_404(jobmodel,id=myid)
    current_user=request.user
    already_applid=jobapplymodel.objects.filter(apply_to=myjob,applied_by=current_user).exists()
    # if already_applid:
    #     messages.warning(request,'Already Applied')
    #     return redirect("joblistforall")
    if request.method == 'POST':
        skills=request.POST.get('skills')
        education=request.POST.get('education')
        resume=request.FILES.get('resume')
        application=jobapplymodel.objects.create(
            applied_by=current_user,
            apply_to=myjob,
            skills=skills,
            education=education,
            resume=resume,
        )
        application.save()
        messages.success(request,'Apply Successfull')
        return redirect("joblistforall")
    return render(request,'applyjob.html',{'myjob':myjob})


@login_required
def appliedjob(request):
    current_user=request.user
    myjob=jobmodel.objects.all()
    applied=jobapplymodel.objects.filter(applied_by=current_user)
    return render(request,'appliedjob.html',{'applied':applied})

@login_required
def viewapplicant(request,myid):
    myjob=jobmodel.objects.get(id=myid)
    applicant=jobapplymodel.objects.filter(apply_to=myjob)
    
    return render(request,'viewapplicant.html',{'applicant':applicant,'myjob':myjob})


@login_required
def profile(request):
    return render(request,'profile.html')

@login_required
def resumeprofile(request):
    return render(request,'resumeprofile.html')

@login_required
def postedjob(request):
    current_user=request.user
    myjob=jobmodel.objects.filter(created_by=current_user)
    return render(request,'postedjob.html',{'myjob':myjob})

@login_required
def deletejob(request,myid):
    myjob=jobmodel.objects.get(id=myid)
    myjob.delete()
    return redirect("postedjob")


@login_required
def editjob(request,myid):
    current_user=request.user
    myjob=jobmodel.objects.filter(id=myid,created_by=current_user)
    if request.method == 'POST':
        id=request.POST.get('id')
        job_title=request.POST.get('job_title')
        company_description=request.POST.get('company_description')
        company_logo_new=request.FILES.get('company_logo_new')
        company_name=request.POST.get('company_name')
        company_location=request.POST.get('company_location')
        qualification=request.POST.get('qualification')
        deadline=request.POST.get('deadline')
        salary=request.POST.get('salary')
        current_user=request.user
        myjob=jobmodel(
            id=id,
            job_title=job_title,
            company_description=company_description,
            
            company_name=company_name,
            company_location=company_location,
            qualification=qualification,
            deadline=deadline,
            salary=salary,
            created_by=current_user,
        )
        if company_logo_new:
            myjob.company_logo=company_logo_new
        
        myjob.save()
        return redirect("postedjob")
    return render(request,'editjob.html',{'myjob':myjob})

@login_required
def changepassword(request):
    if request.method == 'POST':
        old_password=request.POST.get('old_password')
        new_password=request.POST.get('new_password')
        confirm_new_password=request.POST.get('confirm_new_password')
        
        if check_password(old_password,request.user.password):
            if new_password == confirm_new_password:
                current_user=request.user
                current_user.set_password(new_password)
                current_user.save()
                update_session_auth_hash(request,current_user)
                return redirect("resumeprofile")
    return render(request,'changepassword.html')

@login_required
def editprofile(request):
    current_user=request.user
    if request.method == 'POST':
        
        password=request.POST.get('password')
        city=request.POST.get('city')
        gender=request.POST.get('gender')
        new_profile_picture=request.FILES.get('new_profile_picture')
        email=request.POST.get('email')
        father_name=request.POST.get('father_name')
        mother_name=request.POST.get('mother_name')
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        emergency_contact=request.POST.get('emergency_contact')
        
        # seekerprofilemodel
        education_qualification=request.POST.get('education_qualification')
        word_experience=request.POST.get('word_experience')
        
        if check_password(password,current_user.password):
            
            current_user.city=city
            current_user.gender=gender
            current_user.email=email
            current_user.father_name=father_name
            current_user.mother_name=mother_name
            current_user.address=address
            current_user.phone=phone
            current_user.emergency_contact=emergency_contact
        
            if new_profile_picture:
                current_user.profile_picture=new_profile_picture
            
            if current_user.role == 'job_seeker':
                current_user.SeekerProfileModel.education_qualification=education_qualification
                current_user.SeekerProfileModel.word_experience=word_experience
                current_user.SeekerProfileModel.save()
            current_user.save()
            return redirect("resumeprofile")
    return render(request,'editprofile.html')
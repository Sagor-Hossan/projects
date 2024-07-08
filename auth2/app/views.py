from django.shortcuts import render,redirect
from app.models import *
from .forms import*

# Create your views here.

def signin(r):
    return render(r,'signin.html')

def signup(r):
    if r.method == 'POST':
        form = SignUpForm(r.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
    else:
        form = SignUpForm()
    return render(r, 'signup.html',{'form': form})
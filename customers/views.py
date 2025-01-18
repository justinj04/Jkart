from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from . models import Customers

# Create your views here.

#def sign_out(request):
#    logout(request)
#    return redirect('home')

def show_account(request):

    if request.POST and 'register' in request.POST:
        try:    
            username=request.POST.get('username')
            password=request.POST.get('password')
            email=request.POST.get('email')
            address=request.POST.get('address')
            phone=request.POST.get('phone')
            # create user accounts
            user=User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            # create customer account
            customer=Customers.objects.create(
                user=user,
                phone=phone,
                adress=address
            )
            success_message="user registred successfully!!"
            messages.success(request,success_message)
        except Exception as e:
                error_message="duplicate username or invalid inputs"
                messages.error(request,error_message)
    if request.POST and 'login' in request.POST:
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(username=username,password=password)
            if user:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,'invalid user credentials. please register')    

    return render(request,'account.html')
from django.shortcuts import render,redirect,get_object_or_404
from . models import CustomUser,Profile
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from users.forms import UserOForm,UserPForm
from app_ems.models import EventInfo
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user_email = request.POST.get('u_email')
        user_password = request.POST.get('password')
        confirm_password = request.POST.get('password1')
        user_role = request.POST.get('role')

        if user_password != confirm_password:
            messages.warning(request,f"Password and Confirm Password does not match")
            return redirect('user_register')

        if CustomUser.objects.filter(email=user_email).exists():
            messages.warning(request,f"Email Already Exists")
            return redirect('user_register')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request,f"Username Already Exists")
            return redirect('user_register')
        
        CustomUser.objects.create_user(username=username,email=user_email,password=user_password,role=user_role)
        messages.success(request,f"Account created successfully")
        return redirect('users_login')

    return render(request,'users/users_register.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not CustomUser.objects.filter(username=username).exists():
            messages.warning(request,f"Username Does not exist")
            return redirect('users_login')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('event_home')
        else:
            messages.warning(request,f"Invalid Password")
            return redirect('users_login')
        
    return render(request,'users/users_login.html')


def user_logout(request):
    logout(request)
    return render(request,'users/users_logout.html')

def organizer_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        o_form = UserOForm(request.POST,request.FILES,instance=profile)
        if 'o_save' in request.POST and o_form.is_valid():
            o_instance = o_form.save(commit=False)
            #o_instance.user = request.user
            o_instance.save()
            messages.success(request,f"Account has been updated")
            return redirect('user_profile')
    else:
        o_form = UserOForm(instance=profile)
       
    user_profile_data = Profile.objects.filter(user=request.user)

    return render(request,'users/organizer_profile.html',{'O_form':o_form,'user_profile_data':user_profile_data})

def participant_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        p_form  = UserPForm(request.POST,request.FILES,instance=profile)
        if 'p_save' in request.POST and p_form.is_valid():
            p_instance = p_form.save(commit=False)
            #p_instance.user = request.user
            p_instance.save()
            messages.success(request,f"Account has been updated")
            return redirect('participant_profile')
        
    else:
        p_form  = UserPForm(instance=profile)
        
    user_profile_data = Profile.objects.filter(user=request.user)

    return render(request,'users/participant_profile.html',{'P_form':p_form,'user_profile_data':user_profile_data})


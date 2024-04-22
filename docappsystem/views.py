from django.shortcuts import render,redirect,HttpResponse
from dasapp.EmailBackEnd import EmailBackEnd
from django.contrib.auth import  logout,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dasapp.models import CustomUser
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from dasapp.forms import UserForm
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()
def BASE(request):
    return render(request,'base.html')


def LOGIN(request):
    return render(request,'llogin.html')

def doLogout(request):
    logout(request)
    return redirect('login')

def doLogin(request):
    if request.method == 'POST':
        user = EmailBackEnd.authenticate(request,
                                         username=request.POST.get('email'),
                                         password=request.POST.get('password')
                                         )
        if user!=None:
            login(request,user)
            user_type = user.user_type
            if user_type == '1':
                 return redirect('admin_home')
            elif user_type == '2':
                 return redirect('doctor_home')
            elif user_type == '3':
                return HttpResponse("This is User panel")
            
            
        else:
                messages.error(request,'Email or Password is not valid')
                return redirect('login')
    else:
            messages.error(request,'Email or Password is not valid')
            return redirect('login')


login_required(login_url='/')
def PROFILE(request):
    user = CustomUser.objects.get(id = request.user.id)
    context = {
        "user":user,
    }
    return render(request,'profile.html',context)
@login_required(login_url = '/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        print(profile_pic)
        

        try:
            customuser = CustomUser.objects.get(id = request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            

            
            if profile_pic !=None and profile_pic != "":
               customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request,"Your profile has been updated successfully")
            return redirect('profile')

        except:
            messages.error(request,"Your profile updation has been failed")
    return render(request, 'profile.html')


def CHANGE_PASSWORD(request):
    context = {}
    ch = User.objects.filter(id=request.user.id)
     
    if len(ch) > 0:
        data = User.objects.get(id=request.user.id)
        context["data"] = data            
    if request.method == "POST":        
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']
        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
            user.set_password(new_pas)
            user.save()
            messages.success(request, 'Password Changed Successfully!!!')
            user = User.objects.get(username=un)
            login(request, user)
        else:
            messages.error(request, 'Current Password is incorrect!!!')
            return redirect("change_password")
    return render(request, 'change-password.html', context)






def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('create_appointment')  # Redirect to the appointment booking page after login
        else:
            # Invalid login, display an error message
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    return render(request, 'login.html')
# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext as _

from django.contrib.auth.models import Permission

from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser, Group

from django.conf import settings
from django.shortcuts import render,redirect,HttpResponse
from dasapp.EmailBackEnd import EmailBackEnd
from django.contrib.auth import  logout,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dasapp.models import CustomUser
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect,HttpResponse
from dasapp.EmailBackEnd import EmailBackEnd
from django.contrib.auth import  logout,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dasapp.models import CustomUser
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from dasapp.forms import UserForm




# def rregistration(request):
#     if request.method == 'POST':
#         form =UserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = UserForm()
#     return render(request, 'rregistration.html', {'form': form})
# def login_user(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('create_appointment')  # Redirect to the appointment booking page after login
#         else:
#             # Invalid login, display an error message
#             return render(request, 'login.html', {'error_message': 'Invalid username or password'})
#     return render(request, 'login.html')
# # views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext as _

from django.contrib.auth.models import Permission

from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser, Group

from django.conf import settings
from dasapp.forms import UserForm
from django.contrib import messages

# views.py
from django.contrib.auth.forms import AuthenticationForm

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('search')  # Redirect to the search page upon successful login
        else:
            # Invalid login
            messages.error(request, 'Invalid email or password')
    else:
        form = AuthenticationForm()
    return render(request, 'llogin.html', {'form': form})

def rregistration(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Additional steps after registration, if needed
            # For example, sending a welcome email
            send_welcome_email(user.email)
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('user_login')  # Redirect to the login page after successful registration
        else:
            # If form is not valid, re-render the registration form with error messages
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'userregistration.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to maintain the session
            # Additional steps after password change, if needed
            # For example, sending a notification email
            send_password_changed_email(user.email)
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})

def send_welcome_email(email):
    # Customize the email content as needed
    subject = 'Welcome to Our Website'
    message = 'Thank you for registering with us!'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

def send_password_changed_email(email):
    # Customize the email content as needed
    subject = 'Your Password Has Been Changed'
    message = 'Your password has been changed successfully.'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

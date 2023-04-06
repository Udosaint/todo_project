from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.decorators import login_required

from rest_framework.authtoken.models import Token

from api.models import User
from todo.models import Otp, Todo

from .emails import *
from todo.forms import TodoForm, UserChangePassword, UserProfile, UserRegisterForm

from django.core.mail import send_mail
from django.template.loader import render_to_string

from .tasks import test_func
# Create your views here.
import random

def test(request):
    users = User.objects.all().exclude(username='admin') 
    todos =Todo.objects.all()
    for user in users:
        
        username = user.username
        todo = user.todo_set.all().filter(status=0)
        todo_count = user.todo_set.all().filter(status=0).count()
        html = render_to_string('todo/emails/uncomplete_todo.html',{
        'username':username,
        'todo_count':todo_count,
        'todo':todo
        })
        send_mail(
            'Uncompleted Task',
            f'Hi, {user.username}, you have {todo_count} uncompleted Todo',
            'noreply@tbnotes.com',
            [user.email],
            html_message=html
            )

        
    context = {'users':users, 'todos':todos}
    return render (request, 'todo/test.html', context)





def Index(request):

    #test_func.delay()
    #send_verify_link('udosaint@gmail.com', 'hfjsfjhgsgf8r234628946234234hsgdfhg')

    if request.user.is_authenticated:
        return redirect('todo')

    
    if request.method == "POST":
        message = None

        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            
        except:
            
            messages.warning(request, "Username not found" )

        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_verified:

                login(request,user)
                messages.success(request, "Login Successful" )
                return redirect('todo')
            else:
                otp = send_otp(user.email)
                Otp.objects.create(user=user, pin=otp)
                messages.success(request, "Please verify your account, check your email for OTP" )
                return redirect('verify-account')
        else:
            messages.warning(request, "Username or Password not valid" )
            return render(request, 'todo/index.html')
    return render(request, 'todo/index.html')



def Signup(request):
    message = None
    form = UserRegisterForm()
    if request.method == "POST":
        user_name = request.POST.get('username')
        user_email = request.POST.get('email').lower()
        user_password1 = request.POST.get('password')
        user_password2 = request.POST.get('password2')


        if User.objects.filter(username=user_name).exists():
            messages.warning(request, "Username already exist" )

        elif User.objects.filter(email=user_email).exists():
           messages.warning(request, "Email already exist" )

        elif user_password1 != user_password2:
            messages.warning(request, "Password do not match" )
        else:
            user = User(
                email = user_email,
                username = user_name,
            )

            user.set_password(user_password1)
            user.save()

            #create API Token for the user
            token, created = Token.objects.get_or_create(user=user)

            # send welcome email
            send_welcome_mail(user_email, user_name)


            # send the user otp for account verification
            otp = send_otp(user_email)
            Otp.objects.create(user=user, pin=otp)
            
            #send_verify_link(user_email, token)

            messages.success(request, "Registration Successful" )
            return redirect ('verify-account')
       
    return render(request, 'todo/register.html', {'form':form})

def VerifyAccount(request):
    if request.method == "POST":
        digit1 = request.POST.get('otp1')
        digit2 = request.POST.get('otp2')
        digit3 = request.POST.get('otp3')
        digit4 = request.POST.get('otp4')
        digit5 = request.POST.get('otp5')
        digit6 = request.POST.get('otp6')

        otp = digit1 + digit2 + digit3 + digit4 + digit5 + digit6
        try:
            #get the user that has the otp
            getPin = Otp.objects.get(pin=otp)
            user = getPin.user
            #verify the user
            User.objects.filter(username=user).update(is_verified=1)

            username = User.objects.get(username=user)
            # email to show account success
            account_success(username.email, username)
            messages.success(request, "Account verified successfully" )
            return redirect('index')
        except Otp.DoesNotExist:
            messages.warning(request, "The OTP code is invalid" )
            return render(request, 'todo/verify_account.html')
    return render(request, 'todo/verify_account.html')

@login_required(login_url='index')
def Todos(request):
    user = request.user
    todos = user.todo_set.all()

    context = {'todos':todos}
    return render(request, 'todo/todo.html', context)


@login_required(login_url='index')
def AddTodo(request):
    page = "Add"
    form = TodoForm()
    
    if request.method == "POST":
        form = TodoForm(request.POST)

        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, "Todo added successfully" )
            return redirect('todo')

    context = {'page':page, 'form':form}
    return render(request, 'todo/add_edit_todo.html', context)


@login_required(login_url='index')
def EditTodo(request, id):
    page = "Edit"
    todo = Todo.objects.get(id=id)
    form = TodoForm(instance=todo)
    
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)

        if form.is_valid():
            form.save()
            messages.success(request, "Todo updated successfully" )
            return redirect('todo')

    context = {'page':page, 'form':form}
    return render(request, 'todo/add_edit_todo.html', context)


@login_required(login_url='index')
def CompleteTodo(request, id):
   
    if request.method == "GET":
        Todo.objects.filter(id=id ).update(status=1)
        return redirect('todo')

    return render(request, 'todo/add_edit_todo.html')



@login_required(login_url='index')
def DeleteTodo(request, id):
    if request.method == "GET":
        todo = Todo.objects.get(id=id)
        todo.delete()
        messages.success(request, "Todo deleted successfully" )
        return redirect('todo')
    
    context = {}
    return render(request, 'todo/todo.html', context)



@login_required(login_url='index')
def Profile(request):
    user = request.user
    return render(request, 'todo/profile.html', {'user':user})

@login_required(login_url='index')
def UpdateProfile(request):
    form = UserProfile(instance=request.user)
    if request.method == "POST":
        form = UserProfile(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully" )
            return redirect('profile')

    return render(request, 'todo/edit_profile.html', {'form':form})


@login_required(login_url='index')
def ChangePassword(request):
    user = request.user

    if request.method == "POST":
        password = request.POST.get('new_password1')
        password2 = request.POST.get('new_password2')

        if password == password2:
            set_user = User.objects.get(username=user)
            set_user.set_password(password)
            set_user.save()

            update_session_auth_hash(request,set_user)
            password_success(set_user.email, set_user.username)
            messages.success(request, "Password Change successful" )
            return redirect('index')
        else:
            messages.warning(request, "Password does not match" )
    
    return render(request, 'todo/change_password.html')


def RegisterSuccess(request):
    return render(request, 'todo/register_success.html')


def VerifyEmail(request, token):
    if User.objects.filter(auth_token=token).update(is_verified=1):
        messages.success(request, "Email verification successful" )
        return render(request, 'todo/verify_success.html')
    else:
        return redirect('index')
    

def VerifySuccess(request):
    return render(request, 'todo/verify_success.html')


def UserLogout(request):
    logout(request)
    return redirect('index')

def PasswordReset(request):
    if request.method == "POST":
        email = request.POST.get('email')

        if User.objects.filter(email=email):
            user = User.objects.get(email=email)
            
            otp = forgot_password_otp(email)
            Otp.objects.create(user=user, pin=otp)

            messages.success(request, "Email verified, an OTP has been sent to your Eamil")
            return redirect('reset')
        else:
            messages.warning(request, "Email is not correct" )

    context = {"page":"Password-reset"}
        
    return render(request,  'todo/password_reset.html', context)

def Reset(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if Otp.objects.filter(pin=otp):
            if password == password2:
                get_user = Otp.objects.get(pin=otp)
                set_user = User.objects.get(username=get_user.user)
                set_user.set_password(password)
                set_user.save()
                forgot_password_success(set_user.email, set_user.username)
                messages.success(request, "Password Reset Successful" )
                return redirect('index')
            else:
                messages.warning(request, "Password does not match" )
        else:
            messages.warning(request, "OTP is not Correct" )

    return render(request, 'todo/password_reset.html')
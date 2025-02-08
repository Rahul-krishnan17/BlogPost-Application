from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.validators import EmailValidator, ValidationError
from .models import Profile
from django.contrib import messages
import traceback
import re

# Create your views here.

def register(request):
    try:
        if request.method == "POST":
            # Fetching values from the form
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            phone_number = request.POST['phone_number']
            password = request.POST['password']

            # Check if any field is empty
            if not first_name or not last_name or not username or not email or not phone_number or not password:
                messages.error(request, 'All fields are required.')
                return redirect('user-register')

            # Validate email
            try:
                EmailValidator()(email)
            except ValidationError:
                messages.error(request, 'Enter a valid email address.')
                return redirect('user-register')

            # Validate phone number (only digits, 10-15 length)
            if not re.match(r'^\d{10,15}$', phone_number):
                messages.error(request, 'Enter a valid phone number (only digits, 10-15 characters).')
                return redirect('user-register')
            
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken.")
                return redirect('user-register')

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered.")
                return redirect('user-register')

            # Saving the data into database
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            Profile.objects.create(user=user, phone_number=phone_number)
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('user-login')
    
        return render(request, 'registration/register.html')
    except Exception as e:
        messages.error(request, 'An unexpected error occurred. Please contact support.')
        traceback_str = traceback.format_exc()
        print('Exception in register:', e)
        print('Traceback:', traceback_str)
        return redirect('user-register')

def user_login(request):
    try:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('blog-home')
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('user-login')

        return render(request, 'registration/login.html')
    except Exception as e:
        messages.error(request, 'An unexpected error occurred. Please contact support.')
        traceback_str = traceback.format_exc()
        print('Exception in user_login:', e)
        print('Traceback:', traceback_str)
        return redirect('user-login')

def user_logout(request):
    try:
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect('user-login')
    except Exception as e:
        messages.error(request, 'An unexpected error occurred. Please contact support.')
        traceback_str = traceback.format_exc()
        print('Exception in user_logout:', e)
        print('Traceback:', traceback_str)
        return redirect('blog-home')

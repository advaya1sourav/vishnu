from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django import forms
from .forms import RegistrationForm
from users.models import Volunteer
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime


def generate_otp():
    """
    Generates a 6-digit one-time password (OTP) using a random
    combination of digits.

    Returns:
        str: a 6-digit OTP
    """
    return get_random_string(length=4, allowed_chars='0123456789')



def is_gmail(email):
    """Checks if the email belongs to Gmail."""
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", email))

def register_view(request):
    if request.method == 'POST':
        if 'get_otp' in request.POST:
            email = request.POST.get('email')

            if not email:
                messages.error(request, 'Please enter a valid email address.')
                return redirect('register')

            # Validate email format
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, 'Invalid email format.')
                return redirect('register')

            # Enforce Gmail-only restriction
            if not is_gmail(email):
                messages.error(request, 'Only Gmail addresses are allowed for registration.')
                return redirect('register')

            if Volunteer.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered.')
                return redirect('register')

            otp = generate_otp()
            request.session['otp'] = otp
            request.session['email'] = email
            request.session['otp_sent'] = True

            subject = "VISHNU : OTP for Registration"
            message = f"""
Hello,

Welcome to VISHNU! 🎉
You are one step closer to changing the world with us! 
🌍 Together, we can make a difference, and we’re excited to have you join our community. 
To complete your registration process, 
please use the following One-Time Password (OTP):{otp}
Thank you for joining us! If you have any questions, feel free to reach out.

Best regards,
The VISHNU Team
[vishnucomminity@gmail.com]
"""
            from_email = settings.DEFAULT_FROM_EMAIL
            send_mail(subject, message, from_email, [email])

            messages.success(request, 'OTP has been sent to your email.')
            return render(request, 'authentication/register.html', {'otp_sent': True, 'email': email})

        elif 'verify_otp' in request.POST:
            user_otp = request.POST.get('otp')
            stored_otp = request.session.get('otp')

            if not user_otp or len(user_otp) != 4:
                messages.error(request, 'Invalid OTP format. It must be a 4-digit number.')
                return render(request, 'authentication/register.html', {'otp_sent': True, 'email': request.session.get('email')})

            if user_otp == stored_otp:
                request.session['otp_verified'] = True
                return render(request, 'authentication/register.html', {'otp_verified': True, 'email': request.session.get('email')})
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
                return render(request, 'authentication/register.html', {'otp_sent': True, 'email': request.session.get('email')})

        elif 'complete_registration' in request.POST:
            if request.session.get('otp_verified'):
                form = RegistrationForm(request.POST)
                if form.is_valid():
                    dob = form.cleaned_data.get('dob')
                    if dob and dob > datetime.today().date():
                        messages.error(request, 'Date of Birth cannot be in the future.')
                        return render(request, 'authentication/register.html', {'otp_verified': True, 'form': form, 'email': request.session.get('email')})
                    
                    user = form.save(commit=False)
                    user.email = request.session.get('email')
                    user.is_active = True
                    user.save()
                    
                    del request.session['otp']
                    del request.session['email']
                    del request.session['otp_sent']
                    del request.session['otp_verified']

                    messages.success(request, 'Registration successful! Please login.')
                    return redirect('login')
                else:
                    messages.error(request, 'Form submission contains errors. Please check the details and try again.')
                    return render(request, 'authentication/register.html', {'otp_verified': True, 'form': form, 'email': request.session.get('email')})
            else:
                messages.error(request, 'OTP verification is required.')
                return redirect('register')

    else:
        if 'otp_verified' in request.session:
            return render(request, 'authentication/register.html', {'otp_verified': True, 'email': request.session.get('email')})
        else:
            return render(request, 'authentication/register.html')



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('projects:project_list')  # Redirect on successful login
        else:
            messages.error(request, "Enter a valid username and password.")  # Add error message

    else:
        form = AuthenticationForm()
    
    return render(request, 'authentication/login.html', {'form': form})

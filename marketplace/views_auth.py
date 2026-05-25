from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegistrationForm
from .models import EmailVerificationToken, CustomUser

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.email_verified and user.email:
                    messages.warning(request, 'Please verify your email before logging in. Check your inbox.')
                    return render(request, 'registration/login.html', {'form': form})
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_verified = False
            user.save()
            send_verification_email(user)
            messages.info(request, 'Account created! Please check your email to verify your account.')
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def send_verification_email(user):
    token = EmailVerificationToken.objects.create(user=user)
    domain = 'localhost:8000'
    verification_url = f'http://{domain}/verify-email/{token.token}/'
    send_mail(
        subject='Verify your email - சந்தை பேரங்காடி',
        message=f'Hi {user.username},\n\nClick the link below to verify your email:\n{verification_url}\n\nIf you did not register, please ignore this email.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )

def verify_email(request, token):
    try:
        verification_token = EmailVerificationToken.objects.get(token=token)
        user = verification_token.user
        user.email_verified = True
        user.save()
        verification_token.delete()
        messages.success(request, 'Email verified successfully!')
    except EmailVerificationToken.DoesNotExist:
        messages.error(request, 'Invalid or expired verification link.')
    return redirect('home')

def resend_verification(request):
    if request.user.is_authenticated and not request.user.email_verified and request.user.email:
        EmailVerificationToken.objects.filter(user=request.user).delete()
        send_verification_email(request.user)
        messages.info(request, 'Verification email resent. Check your inbox.')
    return redirect('home')

def home(request):
    return render(request, 'marketplace/home.html')

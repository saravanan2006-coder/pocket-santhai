from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from .forms import UserRegistrationForm
from .models import EmailVerificationToken, CustomUser, SellerProfile, TN_DISTRICTS

def is_dev_mode():
    return settings.DEBUG

@ratelimit(key='ip', rate='5/m', block=True)
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
                    msg = 'Please verify your email before logging in. '
                    if is_dev_mode():
                        token = EmailVerificationToken.objects.filter(user=user).last()
                        if token:
                            url = f'{request.scheme}://{settings.VERIFICATION_DOMAIN}/verify-email/{token.token}/'
                            msg += f'<a href="{url}" style="color:#856404;font-weight:600;">Click here to verify</a>'
                        else:
                            msg += 'Check your inbox (or sent_emails/ folder).'
                    else:
                        msg += 'Check your inbox.'
                    messages.warning(request, msg)
                    return render(request, 'registration/login.html', {'form': form})
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@ratelimit(key='ip', rate='5/m', block=True)
def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_verified = False
            user.save()
            
            if user.role == 'seller':
                SellerProfile.objects.create(
                    user=user,
                    business_name=f"{user.username}'s Business",
                    address='',
                    district=TN_DISTRICTS[0],
                    phone=user.phone,
                    email=user.email
                )

            send_verification_email(request, user)
            token = EmailVerificationToken.objects.filter(user=user).last()
            if is_dev_mode() and token:
                url = f'{request.scheme}://{settings.VERIFICATION_DOMAIN}/verify-email/{token.token}/'
                messages.success(request, f'Account created! <a href="{url}" style="color:#155724;font-weight:600;">Click here to verify your email</a> (dev mode)')
            else:
                messages.success(request, 'Account created! Please check your email to verify your account.')
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def send_verification_email(request, user):
    token = EmailVerificationToken.objects.create(user=user)
    from .tasks import send_verification_email_async
    send_verification_email_async.delay(user.pk, token.pk, settings.VERIFICATION_DOMAIN, request.scheme)

def verify_email(request, token):
    try:
        verification_token = EmailVerificationToken.objects.get(token=token)
        if verification_token.is_expired:
            verification_token.delete()
            messages.error(request, 'This verification link has expired. Please request a new one.')
            return redirect('home')
        user = verification_token.user
        user.email_verified = True
        user.save()
        verification_token.delete()
        messages.success(request, 'Email verified successfully!')
    except EmailVerificationToken.DoesNotExist:
        messages.error(request, 'Invalid or expired verification link.')
    return redirect('home')

@ratelimit(key='ip', rate='3/m', block=True)
def resend_verification(request):
    if request.user.is_authenticated and not request.user.email_verified and request.user.email:
        EmailVerificationToken.objects.filter(user=request.user).delete()
        send_verification_email(request, request.user)
        token = EmailVerificationToken.objects.filter(user=request.user).last()
        if is_dev_mode() and token:
            url = f'{request.scheme}://{settings.VERIFICATION_DOMAIN}/verify-email/{token.token}/'
            messages.info(request, f'Verification email resent. <a href="{url}" style="color:#856404;font-weight:600;">Click here to verify</a> (dev mode)')
        else:
            messages.info(request, 'Verification email resent. Check your inbox.')
    return redirect('home')

def home(request):
    return render(request, 'marketplace/home.html')

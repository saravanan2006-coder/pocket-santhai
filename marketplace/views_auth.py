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
                        from urllib.parse import quote_plus
                        from django.urls import reverse
                        resend_url = f"{reverse('resend_verification')}?email={quote_plus(user.email)}"
                        msg += f'Check your inbox or <a href="{resend_url}" style="color:#856404;font-weight:600;text-decoration:underline;">click here to resend verification email</a>.'
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
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def send_verification_email(request, user):
    token = EmailVerificationToken.objects.create(user=user)
    try:
        from .tasks import send_verification_email_async
        send_verification_email_async.delay(user.pk, token.pk, settings.VERIFICATION_DOMAIN, request.scheme)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Celery dispatch failed ({e}), falling back to synchronous email")
        from django.template.loader import render_to_string
        from django.utils.html import strip_tags
        try:
            verification_url = f'{request.scheme}://{settings.VERIFICATION_DOMAIN}/verify-email/{token.token}/'
            context = {'user': user, 'verification_url': verification_url}
            html_message = render_to_string('emails/verification_email.html', context)
            plain_message = strip_tags(html_message)
            send_mail(
                subject='Verify your email - PocketSanthai',
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
                html_message=html_message
            )
        except Exception as mail_err:
            logger.error(f"Synchronous email fallback failed: {mail_err}")

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
        messages.success(request, 'Email verified successfully! You can now log in.')
        return redirect('login')
    except EmailVerificationToken.DoesNotExist:
        messages.error(request, 'Invalid or expired verification link.')
    return redirect('home')

@ratelimit(key='ip', rate='3/m', block=True)
def resend_verification(request):
    target_user = None
    if request.user.is_authenticated:
        target_user = request.user
    else:
        raw_email = request.GET.get('email') or request.POST.get('email', '')
        email = raw_email.strip().lower() if raw_email else ''
        if email:
            target_user = CustomUser.objects.filter(email__iexact=email).first()

    if target_user:
        if target_user.email_verified:
            messages.info(request, 'Your email is already verified. You can log in.')
            return redirect('login')
        EmailVerificationToken.objects.filter(user=target_user).delete()
        send_verification_email(request, target_user)
        token = EmailVerificationToken.objects.filter(user=target_user).last()
        if is_dev_mode() and token:
            url = f'{request.scheme}://{settings.VERIFICATION_DOMAIN}/verify-email/{token.token}/'
            messages.info(request, f'Verification email resent. <a href="{url}" style="color:#856404;font-weight:600;">Click here to verify</a> (dev mode)')
        else:
            messages.info(request, 'Verification email resent. Please check your inbox.')
    else:
        messages.warning(request, 'Please log in or provide a registered email to resend verification.')

    return redirect('login' if not request.user.is_authenticated else 'home')

def home(request):
    return render(request, 'marketplace/home.html')

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_verification_email_async(user_id, token_id, domain, scheme):
    from .models import CustomUser, EmailVerificationToken
    try:
        user = CustomUser.objects.get(pk=user_id)
        token = EmailVerificationToken.objects.get(pk=token_id)
        verification_url = f'{scheme}://{domain}/verify-email/{token.token}/'
        send_mail(
            subject='Verify your email - சந்தை பேரங்காடி',
            message=f'Hi {user.username},\n\nClick the link below to verify your email:\n{verification_url}\n\nIf you did not register, please ignore this email. This link will expire in 24 hours.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception:
        pass

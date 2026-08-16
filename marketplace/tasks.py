from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_verification_email_async(user_id, token_id, domain, scheme):
    from .models import CustomUser, EmailVerificationToken
    from django.template.loader import render_to_string
    from django.utils.html import strip_tags
    try:
        user = CustomUser.objects.get(pk=user_id)
        token = EmailVerificationToken.objects.get(pk=token_id)
        verification_url = f'{scheme}://{domain}/verify-email/{token.token}/'
        
        context = {
            'user': user,
            'verification_url': verification_url
        }
        
        html_message = render_to_string('emails/verification_email.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject='Verify your email - PocketSanthai',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
            html_message=html_message
        )
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to send email: {e}")


from django.core.mail import send_mail
from django.conf import settings


def send_approval_email(user_email, seller_name):
    """
    Sends an email to the seller notifying that their KYC has been approved.
    
    Args:
        user_email (str): The recipient's email address.
        seller_name (str): Name of the seller.
    """
    if not user_email:
        raise ValueError("User email is required to send approval email.")
    
    subject = "KYC Approved ✅"
    message = (
        f"Hello {seller_name},\n\n"
        "Your KYC has been approved successfully. You can now access your account."
    )
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False
        )
    except Exception as e:
        # Log the error in production
        print(f"Error sending approval email: {e}")





def send_rejection_email(user_email, seller_name, reason):
    """
    Sends an email to the seller notifying that their KYC has been rejected.
    
    Args:
        user_email (str): The recipient's email address.
        seller_name (str): Name of the seller.
        reason (str): Reason for rejection.
    """
    if not user_email:
        raise ValueError("User email is required to send rejection email.")
    
    subject = "KYC Rejected ❌"
    message = (
        f"Hello {seller_name},\n\n"
        "Your KYC application has been rejected.\n"
        f"Reason: {reason}\n\n"
        "Please contact support if you have any questions."
    )
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False
        )
    except Exception as e:
        # Log the error in production
        print(f"Error sending rejection email: {e}")






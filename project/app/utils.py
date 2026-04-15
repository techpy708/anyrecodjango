import random
import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage

def send_otp_email(email, otp, subject, message_template):
    """Send OTP email with error handling and BCC support."""
    try:
        email_message = EmailMessage(
            subject=subject,
            body=message_template.format(otp=otp),
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
            bcc=[settings.DEFAULT_BCC] if hasattr(settings, 'DEFAULT_BCC') else []
        )
        email_message.send()
        return True
    except Exception as e:
        # Log error in production
        print(f"Email sending failed: {e}")
        return False

# Constants
OTP_EXPIRY_SECONDS = 600  # 10 minutes
OTP_LENGTH = 6

def generate_otp():
    """Generate a 6-digit OTP."""
    return str(random.randint(100000, 999999))

def is_otp_expired(otp_time_str, expiry_seconds=OTP_EXPIRY_SECONDS):
    """Check if OTP has expired."""
    if not otp_time_str:
        return True
    
    otp_time = datetime.datetime.fromisoformat(otp_time_str)
    otp_age = (datetime.datetime.now() - otp_time).total_seconds()
    return otp_age > expiry_seconds

def clear_session_keys(session, keys):
    """Clear specified keys from session."""
    for key in keys:
        session.pop(key, None)


def validate_email_and_password(email, password):
    """Basic validation for email and password."""
    if not email or not email.strip():
        return False, "Email is required."
    
    if not password:
        return False, "Password is required."
    
    # Add more validation as needed (email format, password strength, etc.)
    return True, ""

def generate_username_from_email(email):
    """Generate username from email address."""
    return email.split('@')[0]

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
Link= ""

# document-control_gcp\documents\emails\user_credentials_email.txt
def send_user_credentials_email(user, raw_password):
    """
    Sends a welcome email to a newly created user with their credentials.
    """
    subject = "Welcome! Your Account Has Been Created Successfully"

    # Compose the plain text email body using f-string
    text_body = f"""
                    Hi {user.first_name},

                    An account has been created for you. Please find your login credentials and assigned permissions below.
                    It is strongly recommended that you change your password upon your first login.

                    - Username: {user.username}
                    - Password: {raw_password}

                    - Group: {user.group.name if user.group else 'N/A'}
                    - Companies: {", ".join(c.name for c in user.companies.all())}
                    - Department: {user.department.name if user.department else 'N/A'}
                    - Role: {user.get_access_rights_display()}

                    You can log in at: {Link}/login/

                    This is an automated message. Please do not reply.
                    """.strip()

    try:
        send_mail(
            subject=subject,
            message=text_body,  # Plain text version
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False












from django.http import JsonResponse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .models import GroupLicense, ProcessingHistory  # Ensure models are imported

def check_license_validity(user, original_file1, original_file2, row_count_f1, row_count_f2):
    """
    Validates license expiry and credit limits.
    Returns: (is_valid, result)
        - is_valid (bool): True if allowed to proceed, False if blocked.
        - result: If valid, returns 'existing_history_record' (or None).
                  If invalid, returns a JsonResponse with the error.
    """
    user_group = getattr(user, 'company_group', None)
    
    # 1. Check Group Existence
    if not user_group:
        return False, JsonResponse({'status': 'error', 'message': 'User does not belong to any Company Group.'}, status=403)

    unique_key_str = f"{original_file1}|{original_file2}_{row_count_f1}_{row_count_f2}"
    print(f"Checking License for Key: {unique_key_str}")

    try:
        license_obj = GroupLicense.objects.get(group=user_group)
        
        # 2. Check Expiry Date
        if license_obj.expiry_date < timezone.now().date():
            return False, JsonResponse({'status': 'error', 'message': 'License Expired. Please update.'}, status=403)
        
        # 3. Check for Duplicate Processing (No credit deduction if exists)
        existing_history_record = ProcessingHistory.objects.filter(
            group=user_group, 
            unique_key=unique_key_str
        ).first()

        if existing_history_record:
            print("Record exists - Skipping credit check")
            return True, existing_history_record
        else:
            # 4. Check Credit Limit
            # Note: .count() is generally faster than len() for DB queries
            credits_used = ProcessingHistory.objects.filter(group=user_group).count()
            
            if credits_used >= license_obj.row_limit:
                return False, JsonResponse({'status': 'error', 'message': 'License Credit Limit Reached.'}, status=403)
            
            return True, None

    except ObjectDoesNotExist:
        return False, JsonResponse({'status': 'error', 'message': 'No valid license found.'}, status=403)
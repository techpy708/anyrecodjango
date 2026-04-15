from django.core.mail import send_mail
from django.utils.timezone import now
from django.conf import settings
from datetime import timedelta
from .models import Document

def send_expiry_reminders():
    today = now().date()
    cutoff = today + timedelta(days=21)

    expiring_docs = Document.objects.filter(
        is_deleted=False,
        email__isnull=False,
        expiry_date__lte=cutoff,
        expiry_date__gte=today
    )

    for doc in expiring_docs:
        send_mail(
            subject=f"Reminder: '{doc.title}' expires on {doc.expiry_date.strftime('%d-%m-%Y')}",
            message=f"This document will expire on {doc.expiry_date}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[doc.email],
        )
    print(f"{expiring_docs.count()} reminders sent.")

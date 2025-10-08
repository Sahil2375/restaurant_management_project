from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Order

@receiver(post_save, sender=Order)
def send_order_status_email(sender, instance, created, **kwargs):
    """
    Sends an email notification to the admin whenever an order's status changes.
    """

    # If order is newly created, skip status change email
    if created:
        return

    # Retrieve the previous status from the database
    try:
        previous = Order.objects.get(pk=instance.pk)
    except Order.DoesNotExist:
        previous = None

    # Compare old vs new status
    if previous and previous.status != instance.status:
        subject = f"Order #{instance.id} Status Updated"
        message = (
            f"Hello Admin,\n\n"
            f"The status of Order #{instance.id} has changed.\n\n"
            f"Customer: {instance.customer_name}\n"
            f"Old Status: {previous.status}\n"
            f"New Status: {instance.status}\n"
            f"Total Price: ₹{instance.total_price}\n\n"
            f"Regards,\nYour Restaurant System"
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # Sender
            [settings.ADMIN_EMAIL],       # Recipient (Admin email)
            fail_silently=False,
        )

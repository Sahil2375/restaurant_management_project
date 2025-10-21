from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'

    def ready(self):
        import orders.signals
        from django.db.models.signals import post_save
        from .models import Reservation, log_new_reservation

        # Connect the signal to Reservation model
        post_save.connect(log_new_reservation, sender=Reservation)

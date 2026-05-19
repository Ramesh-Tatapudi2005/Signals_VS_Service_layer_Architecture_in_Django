from django.db import transaction
from django.contrib.auth.models import User
from .models import Order, UserStats

def create_order(user: User, total: float) -> Order:
    """
    Explicit service handler wrapping record modification safely within database transactions.
    """
    with transaction.atomic():
        order = Order.objects.create(user=user, total=total)
        stats, _ = UserStats.objects.get_or_create(user=user)
        stats.order_count += 1
        stats.total_spent += order.total
        stats.save()
    return order
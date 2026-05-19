# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from .models import Order, UserStats

# @receiver(post_save, sender=Order)
# def update_user_stats_on_order_save(sender, instance, created, **kwargs):
#     """
#     Implicit signal receiver tracking order placement aggregates.
#     """
#     if created:
#         stats, _ = UserStats.objects.get_or_create(user=instance.user)
#         stats.order_count += 1
#         stats.total_spent += instance.total
#         stats.save()
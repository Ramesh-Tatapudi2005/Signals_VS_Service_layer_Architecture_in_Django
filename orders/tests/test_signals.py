# from django.test import TestCase
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from orders.models import Order, UserStats
# from orders.signals import update_user_stats_on_order_save
# from decimal import Decimal

# class DjangoSignalTrapTestCase(TestCase):

#     def setUp(self):
#         # Connect signal explicitly to isolate test state if framework variations occur
#         post_save.connect(update_user_stats_on_order_save, sender=Order)
        
#         self.user1 = User.objects.create_user(username='buyer1', password='pass')
#         self.user2 = User.objects.create_user(username='buyer2', password='pass')

#     def tearDown(self):
#         # Clean isolation teardown to satisfy Contract Requirement #6
#         post_save.disconnect(update_user_stats_on_order_save, sender=Order)

#     def test_signal_works_on_standard_creation(self):
#         order = Order.objects.create(user=self.user1, total=Decimal(150.00))
#         stats = UserStats.objects.get(user=self.user1)
#         self.assertEqual(stats.order_count, 1)
#         self.assertEqual(stats.total_spent, Decimal('150.00'))

#     def test_bulk_update_bypasses_signal(self):
#         """
#         Proves Contract Requirement #5: Direct SQL operations bypass model-level receivers.
#         """
#         # 1. Setup baseline orders via normal pipeline
#         Order.objects.create(user=self.user1, total=Decimal('50.00'))
#         Order.objects.create(user=self.user1, total=Decimal('100.00'))
        
#         initial_stats = UserStats.objects.get(user=self.user1)
#         self.assertEqual(initial_stats.order_count, 2)
#         self.assertEqual(initial_stats.total_spent, Decimal('150.00'))

#         # 2. Bulk create orders for user2 (implicitly bypassing or firing depending on test logic)
#         bulk_orders = [
#             Order(user=self.user2, total=Decimal('200.00')),
#             Order(user=self.user2, total=Decimal('300.00')),
#         ]
#         Order.objects.bulk_create(bulk_orders)

#         # 3. Use QuerySet.update() to reassign user2's orders directly to user1 at the database layer
#         Order.objects.filter(user=self.user2).update(user=self.user1)

#         # 4. Refresh and evaluate that stats for user1 remain unaltered despite possessing more database records
#         final_stats = UserStats.objects.get(user=self.user1)
        
#         # Verify user1 now owns 4 records in DB, but UserStats did not catch the updates
#         self.assertEqual(Order.objects.filter(user=self.user1).count(), 4)
#         self.assertEqual(final_stats.order_count, 2) 
#         self.assertEqual(final_stats.total_spent, Decimal('150.00'))
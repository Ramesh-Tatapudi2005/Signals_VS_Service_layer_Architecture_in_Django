from django.test import TestCase
from django.contrib.auth.models import User
from orders.models import Order, UserStats
from orders import services
from decimal import Decimal

class ServiceLayerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='service_user', password='password123')

    def test_service_layer_creates_order_and_updates_stats(self):
        """
        Verifies Contract Requirement #8: Explicit layer tracks states cleanly.
        """
        order = services.create_order(user=self.user, total=Decimal('75.50'))
        
        # Verify execution integrity
        self.assertIsNotNone(order.id)
        self.assertEqual(order.total, Decimal('75.50'))
        
        stats = UserStats.objects.get(user=self.user)
        self.assertEqual(stats.order_count, 1)
        self.assertEqual(stats.total_spent, Decimal('75.50'))
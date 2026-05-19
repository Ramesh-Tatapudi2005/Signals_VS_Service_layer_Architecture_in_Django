import time
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import F
from orders.models import Order, UserStats
from decimal import Decimal
class Command(BaseCommand):
    help = "Benchmarks chatty Signal-simulated inserts vs Optimized Batch Service actions."

    def handle(self, *args, **options):
        # Establish sandbox records
        user_signal = User.objects.create_user(username='sig_bench', password='pwd')
        user_service = User.objects.create_user(username='srv_bench', password='pwd')
        
        total_records = 1000
        fixed_amount = Decimal('10.00')

        # --- Approach 1: Simulated Signal Processing Loop (Chatty N+1 Execution) ---
        start_signal = time.perf_counter()
        with transaction.atomic():
            for _ in range(total_records):
                # Simulated inline behavior: 1 Insert + 1 Read + 1 Update per iteration
                Order.objects.create(user=user_signal, total=fixed_amount)
                stats, _ = UserStats.objects.get_or_create(user=user_signal)
                stats.order_count += 1
                stats.total_spent += fixed_amount
                stats.save()
        end_signal = time.perf_counter()
        signal_duration = end_signal - start_signal

        # --- Approach 2: Optimized Service Architecture Execution ---
        start_service = time.perf_counter()
        with transaction.atomic():
            # 1. High-speed database bulk insert layer operation
            bulk_orders = [Order(user=user_service, total=fixed_amount) for _ in range(total_records)]
            Order.objects.bulk_create(bulk_orders)
            
            # 2. Unified summary aggregation applied using efficient F expressions
            calculated_aggregate_sum = total_records * fixed_amount
            stats, _ = UserStats.objects.get_or_create(user=user_service)
            
            UserStats.objects.filter(id=stats.id).update(
                order_count=F('order_count') + total_records,
                total_spent=F('total_spent') + calculated_aggregate_sum
            )
        end_service = time.perf_counter()
        service_duration = end_service - start_service

        # --- Standard Output Formatting Parse Calculations (Req 10) ---
        speedup_factor = signal_duration / service_duration if service_duration > 0 else 0

        self.stdout.write(f"Signal approach time: {signal_duration:.4f}s")
        self.stdout.write(f"Optimized service time: {service_duration:.4f}s")
        self.stdout.write(f"Speedup factor: {speedup_factor:.2f}x")
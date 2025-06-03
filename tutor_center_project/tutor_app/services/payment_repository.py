from .base import BaseRepository
from ..models.payment import Payment
from django.db.models import Sum

class PaymentRepository(BaseRepository):
    model = Payment

    def get_total_amount_paid(self):
        return Payment.objects.aggregate(total_amount=Sum('amount'))['total_amount']

    def get_total_number_of_payments(self):
        return Payment.objects.count()

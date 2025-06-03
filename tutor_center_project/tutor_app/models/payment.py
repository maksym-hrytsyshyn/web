from django.db import models
from .student import Student

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=15, choices=[('Cash', 'Cash'), ('Card', 'Card'), ('Online payment', 'Online payment')])

    class Meta:
        db_table = 'payment'
        managed = False
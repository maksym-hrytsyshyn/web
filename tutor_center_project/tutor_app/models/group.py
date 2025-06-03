from django.db import models
from .subject import Subject

class Group(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    lesson_type = models.CharField(max_length=10, choices=[('Group', 'Group'), ('Individual', 'Individual')])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    describtion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'group'
        managed = False
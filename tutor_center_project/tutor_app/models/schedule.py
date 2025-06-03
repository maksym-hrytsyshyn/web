from django.db import models
from .group import Group
from .tutor import Tutor

class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10)
    start_time = models.DateTimeField()
    lesson_type = models.CharField(max_length=10, choices=[('Online', 'Online'), ('Offline', 'Offline')])
    duration = models.IntegerField()
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)

    class Meta:
        db_table = 'schedule'
        managed = False

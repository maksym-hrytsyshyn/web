from django.db import models
from .student import Student
from .schedule import Schedule

class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    attended = models.BooleanField()
    note = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'attendance'
        managed = False
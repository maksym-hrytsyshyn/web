from django.db import models
from .student import Student
from .group import Group

class StudentGroup(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    class Meta:
        db_table = 'student_group'
        managed = False
        unique_together = ('student', 'group')
from django.db import models

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'subject'
        managed = False
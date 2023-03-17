from django.db import models

# Create your models here.

class files(models.Model):
    file = models.FileField(blank = False,null = False)

    class Meta:
        managed = False
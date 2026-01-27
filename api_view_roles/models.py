from django.db import models

# Create your models here.
class Role(models.Model):
    id_role = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['id_role']


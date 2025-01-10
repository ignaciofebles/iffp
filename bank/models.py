from django.db import models

# Create your models here.
class Bank(models.Model):
    description=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table='banks'
        verbose_name='Bank'
        verbose_name_plural='Banks'

    def __str__(self):
        return self.description

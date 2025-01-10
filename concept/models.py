from django.db import models

# Create your models here.
class Concept(models.Model):
    description=models.CharField(max_length=80)    
    type=models.CharField(max_length=2, default='IN')
    TYPE_CHOICES = [
    ('IN', 'Ingreso'),
    ('EG', 'Egreso'),
    ]
    type = models.CharField(
    max_length=2,
    choices=TYPE_CHOICES,
    default='IN',)
    transfer=models.BooleanField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table='concepts'
        verbose_name='Concept'
        verbose_name_plural='Concepts'

    def __str__(self):
        return self.description

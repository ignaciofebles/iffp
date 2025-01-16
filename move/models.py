from django.contrib.auth.models import User
from django.db import models
from concept.models import Concept
from bank.models import Bank
from django.utils import timezone

# Create your models here.
class Move(models.Model):
    date=models.DateField(default=timezone.now().date())
    comentary=models.CharField(max_length=80, null=False, blank=False)    
    amount = models.DecimalField(
        max_digits=10,     
        decimal_places=2,  
        null=False,        
        blank=False,       
    )
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    bank=models.ForeignKey(Bank, on_delete=models.CASCADE)
    concept=models.ForeignKey(Concept, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table='moves'
        verbose_name='Move'
        verbose_name_plural='Moves'

    def __str__(self):
        return self.comentary

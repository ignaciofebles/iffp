from django.db import models
from concept.models import Concept
from bank.models import Bank
from django.utils.timezone import now

# Create your models here.
class Move(models.Model):
    date=models.DateField(default=now)
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

    class Meta:
        db_table='moves'
        verbose_name='Move'
        verbose_name_plural='Moves'

    def __str__(self):
        return self.comentary

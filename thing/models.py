from django.db import models

# Create your models here.
class Thing(models.Model):
    code=models.CharField()    
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table='things'
        verbose_name='Thing'
        verbose_name_plural='Things'

    def __str__(self):
        return self.code

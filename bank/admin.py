from django.contrib import admin
from .models import Bank

# Register your models here.
class BankAdmin(admin.ModelAdmin):
    readonly_fields=('created_at','updated_at')

admin.site.register(Bank, BankAdmin)
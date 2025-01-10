from django.contrib import admin
from .models import Thing


# Register your models here.
class ThingAdmin(admin.ModelAdmin):
    readonly_fields=('created_at','updated_at')

admin.site.register(Thing, ThingAdmin)
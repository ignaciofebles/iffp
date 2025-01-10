from django.contrib import admin
from .models import Concept

# Register your models here.
class ConceptAdmin(admin.ModelAdmin):
    readonly_fields=('created_at','updated_at')

admin.site.register(Concept, ConceptAdmin)
from django.contrib import admin
from .models import Move

# Register your models here.
class MoveAdmin(admin.ModelAdmin):
    readonly_fields=('created_at','updated_at')

admin.site.register(Move, MoveAdmin)

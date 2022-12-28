from django.contrib import admin
from .models import Todo

from api.models import User

# Register your models here.


class TodoAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'user']



admin.site.register(Todo, TodoAdmin)
admin.site.register(User)
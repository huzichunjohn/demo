from django.contrib import admin
from todo.models import Todo
from . import models 

class TodoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Todo, TodoAdmin)
admin.site.register(models.Category)
admin.site.register(models.Task)

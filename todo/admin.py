from django.contrib import admin
from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple
from bitfield.admin import BitFieldListFilter
from todo.models import Todo, MyModel
from . import models 

class TodoAdmin(admin.ModelAdmin):
    pass

class MyModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
	BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }

    list_filter = (
	('flags', BitFieldListFilter),
    )

admin.site.register(Todo, TodoAdmin)
admin.site.register(models.Category)
admin.site.register(models.Task)
admin.site.register(models.MyModel, MyModelAdmin)

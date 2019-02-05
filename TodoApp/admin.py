from django.contrib import admin
from . import models

admin.site.register(models.TodoList)
admin.site.register(models.TodoItem)

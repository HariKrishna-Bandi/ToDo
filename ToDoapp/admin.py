from django.contrib import admin

# Register your models here.
from ToDoapp.models import Task

admin.site.register(Task)
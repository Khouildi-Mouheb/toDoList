from django.contrib import admin
from .models import Task

# Register your models here.


#registering the Task model in the admin panel
admin.site.register(Task)
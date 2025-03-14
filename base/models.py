from django.contrib.auth.models import User
from django.db import models

class Task(models.Model):
    STATUS = (
        ('todo', 'To Do'),
        ('doing', 'Doing'),
        ('done', 'Done'),
    )

    PRIORITIES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    # Many-to-one relationship (one user can have many tasks)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # Delete all tasks if user is deleted
        null=True,
        blank=True
    )

    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default="todo")
    priority = models.CharField(max_length=10, choices=PRIORITIES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else "Untitled Task"

    class Meta:
        ordering = ['-priority', 'status', '-created_at']





#if we edit the models we have to make migrations and migrate
#python manage.py makemigrations    
#python manage.py migrate

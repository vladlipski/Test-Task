from django.contrib.auth.models import User, AbstractUser
from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(default='')
    employees = models.ManyToManyField(User, blank=True, default=None)
    creation_date = models.DateField('creation date')

    def __str__(self):
        return self.title


class Task(models.Model):
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(default='')
    due_date = models.DateField('due date')
    performer = models.ForeignKey(User, null=True, related_name='tasks',  on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
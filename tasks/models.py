import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Project(models.Model):
    title = models.CharField(max_length=200)
    employees = models.ManyToManyField(User, blank=True, default=None)
    creation_date = models.DateTimeField('creation date')

    def __str__(self):
        return self.title


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField('due date')
    developer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save


def default_group(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='Developer'))
post_save.connect(default_group, sender=User)
from django.contrib.auth.models import User
from django.db import models
from django import forms


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(default='')
    employees = models.ManyToManyField(User, blank=True, default=None)
    creation_date = models.DateTimeField('creation date')

    def __str__(self):
        return self.title


class ProjectForm(forms.ModelForm):

    class Meta(object):
        model = Project
        fields = '__all__'


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(default='')
    due_date = models.DateTimeField('due date')
    developer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
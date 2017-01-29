from django.contrib import admin
from django.contrib.auth.models import Permission

from . import models

admin.site.register(models.Project)
admin.site.register(models.Task)
admin.site.register(Permission)
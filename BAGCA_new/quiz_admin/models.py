from django.db import models
from django.contrib.auth.models import Group

class Categories(models.Model):
    def __str__(self):
        return self.category_text

    groups = models.ManyToManyField(Group, related_name='group')
    category_text = models.CharField(max_length=200, unique=True)
    url = models.CharField(max_length=500)

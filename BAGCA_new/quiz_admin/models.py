from django.db import models
from django.contrib.auth.models import Group
import datetime

class Categories(models.Model):
    class Meta:
        verbose_name_plural = "quizzes"
    def __str__(self):
        return self.category_text

    groups = models.ManyToManyField(Group, related_name='group')
    category_text = models.CharField(max_length=200, unique=True )
    category_description = models.CharField(max_length=1000, default="")
    #url = models.URLField()
    course_code = models.CharField(max_length=40, default="CD"+datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
    due_date = models.DateField(default=datetime.date.today)
    duration_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    required_score = models.DecimalField(max_digits=3, decimal_places=0, default=100)
    training_text = models.CharField(max_length=10000, null=True)

class Videos(models.Model):
    def __str__(self):
        return self.url

    category_id = models.ForeignKey(Categories)
    name = models.CharField(max_length=100)
    url = models.URLField()

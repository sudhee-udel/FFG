import datetime

from django.utils import timezone
from django.db import models
from quiz_admin.models import Categories

class Question(models.Model):
    def __str__(self):
        return self.question_text

    def __unicode__(self):
        return u'%s' % self.question_text

    category = models.ForeignKey(Categories)
    question_text = models.CharField(max_length=500)

class Choice(models.Model):
    def __str__(self):
        return self.choice_text

    def __unicode__(self):
        return u'%s' % self.choice_text

    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    answer = models.BooleanField(default=False)

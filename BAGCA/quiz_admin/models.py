from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import Group
from BAGCA.settings import MEDIA_ROOT_FILES
import os
import datetime


class Quiz(models.Model):
    class Meta:
        verbose_name_plural = "quizzes"

    def __str__(self):
        return self.quiz_name

    def __unicode__(self):
        return u'%s' % self.quiz_name

    groups = models.ManyToManyField(Group, related_name='group')
    quiz_name = models.CharField(max_length=200, unique=True)
    quiz_description = models.CharField(max_length=1000, default="")
    trainer = models.CharField(max_length=100, default='TBD')
    course_code = models.CharField(max_length=40, default="CD")
    due_date = models.DateField(default=datetime.date.today)
    duration_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    required_score = models.DecimalField(max_digits=3, decimal_places=0, default=100)


class Files(models.Model):
    class Meta:
        verbose_name_plural = "Files"

    def __str__(self):
        return u'%s' % self.filename

    quiz_id = models.ForeignKey(Quiz)
    filename = models.CharField(max_length=100, blank=True)
    file = models.FileField(upload_to=MEDIA_ROOT_FILES, blank=True)


class Content(models.Model):
    class Meta:
        verbose_name_plural = "content"

    def __str__(self):
        return u'%s = %s' % (self.url_name, self.url)

    quiz_id = models.ForeignKey(Quiz)
    url_name = models.CharField(max_length=100, blank=True)
    url = models.URLField(blank=True)
    files = models.ManyToManyField(Files, blank=True)


# These two auto-delete files from filesystem when they are unneeded:
@receiver(models.signals.post_delete, sender=Files)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `Files` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=Files)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `Files` object is changed.
    """
    if not instance.pk:
        return False

    try:
        old_file = Files.objects.get(pk=instance.pk).file

        if not old_file:
            return False
    except Files.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

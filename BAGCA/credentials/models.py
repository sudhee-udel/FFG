from django.db import models

class Credentials(models.Model):
    class Meta:
        verbose_name_plural = "credentials"

    def __str__(self):
        return u'%s' % self.credential

    credential = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
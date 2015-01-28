from django.db import models

class Completed(models.Model):
    class Meta:
        verbose_name_plural = "completed"

    def __str__(self):
        return self.user + " passed " + self.category

    category = models.CharField(max_length=50)
    user = models.CharField(max_length=100)
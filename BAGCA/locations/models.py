from django.db import models

class Locations(models.Model):
    class Meta:
        verbose_name_plural = "locations"
    def __str__(self):
        return self.location

    location = models.CharField(max_length=500)
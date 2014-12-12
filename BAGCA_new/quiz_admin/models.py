from django.db import models

class Categories(models.Model):
    def __str__(self):
        return self.category_text

    category_text = models.CharField(max_length=200)
    url = models.CharField(max_length=500)

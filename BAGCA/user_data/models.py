from django.db import models
from quiz_admin.models import Categories
from django.contrib.auth.models import User


class Completed(models.Model):
    class Meta:
        verbose_name_plural = "completed"

    def __str__(self):
        return self.user.username + " passed " + str(self.category)

    category = models.ForeignKey(Categories)
    user = models.ForeignKey(User)
    date_completed = models.DateField()


class UserAssignment(models.Model):
    class Meta:
        verbose_name_plural = "UserAssignments"

    def __str__(self):
        return "Category = " + str(self.category) + ", User = " + str(self.user)

    category = models.ForeignKey(Categories)
    user = models.ForeignKey(User)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
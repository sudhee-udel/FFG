from django.contrib import admin
from user_data.models import Completed

class CompletedAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user', 'date_completed')

admin.site.register(Completed, CompletedAdmin)

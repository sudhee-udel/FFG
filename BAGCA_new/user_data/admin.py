from django.contrib import admin
from user_data.models import Completed

class CompletedAdmin(admin.ModelAdmin):
    list_display = ('category', 'user')

    search_fields = ['category', 'user']

admin.site.register(Completed, CompletedAdmin)

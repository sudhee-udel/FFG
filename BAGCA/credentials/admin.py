from django.contrib import admin
from .models import Credentials

class CredentialsAdmin(admin.ModelAdmin):
    list_display = ('credential', 'password')

    search_fields = ['credential']

admin.site.register(Credentials, CredentialsAdmin)
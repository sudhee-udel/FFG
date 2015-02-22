from django.contrib import admin
from .models import Choice, Question


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'category')
    inlines = [ChoiceInLine]

    search_fields = ['question_text', 'category']


admin.site.register(Choice)
admin.site.register(Question, QuestionAdmin)

from django.contrib import admin
from quizzes.models import Choice, Question

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                      {'fields': ['question_text']}),
        ('Date information',        {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]

    list_display = ('question_text', 'pub_date', 'was_published_recently')
    inlines = [ChoiceInLine]

    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Choice)
admin.site.register(Question, QuestionAdmin)

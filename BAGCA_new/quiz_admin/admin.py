from django.contrib import admin
from quiz_admin.models import Categories
from quizzes.models import Question

class QuestionInLine(admin.StackedInline):
    model = Question
    extra = 1

class CategoriesAdmin(admin.ModelAdmin):

    list_display = ('category_text', 'url')
    inlines = [QuestionInLine]

    search_fields = ['category_text']

admin.site.register(Categories, CategoriesAdmin)

from django.contrib import admin
from .models import Categories, Videos, Files
from quizzes.models import Question

class FilesInLine(admin.TabularInline):
    model = Files
    extra = 1

class VideosInLine(admin.TabularInline):
    model = Videos
    extra = 1

class QuestionInLine(admin.StackedInline):
    model = Question
    extra = 1

class CategoriesAdmin(admin.ModelAdmin):

    list_display = ('category_text', )
    inlines = [VideosInLine, FilesInLine, QuestionInLine]

    search_fields = ['category_text']

admin.site.register(Categories, CategoriesAdmin)

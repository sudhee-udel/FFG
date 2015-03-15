from django.contrib import admin
from .models import Quiz, Content, Files
from quizzes.models import Question


class FilesInLine(admin.TabularInline):
    model = Files
    extra = 1


class VideosInLine(admin.TabularInline):
    model = Content
    extra = 1


class QuestionInLine(admin.StackedInline):
    model = Question
    extra = 1


class QuizAdmin(admin.ModelAdmin):
    list_display = ('quiz_name', )
    inlines = [FilesInLine, VideosInLine, QuestionInLine]

    search_fields = ['quiz_name']


admin.site.register(Quiz, QuizAdmin)

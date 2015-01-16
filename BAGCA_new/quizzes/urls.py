from django.conf.urls import patterns, url
from quizzes import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^(?P<training_id>\d+)/$', views.training, name='training'),
                       url(r'^(?P<training_id>\d+)/quiz/$', views.quiz, name='quiz'),
                       url(r'^(?P<training_id>\d+)/quiz/results/$', views.results, name='results'),
                       url(r'^pdfs/$', views.pdfs, name='pdfs'),
#                       url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
#                       url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
#                       url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
                    )

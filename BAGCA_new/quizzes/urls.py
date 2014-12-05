from django.conf.urls import patterns, url
from quizzes import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^/results/', views.results, name='results'),
                       url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
                       url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote')

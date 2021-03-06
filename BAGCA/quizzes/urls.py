from django.conf.urls import patterns, url
from quizzes import views
from quizzes import helpers

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^(?P<training_id>\d+)/$', views.user_assigned_training, name='user_assigned_training'),
                       url(r'^(?P<training_id>\d+)/quiz/$', views.quiz, name='quiz'),
                       url(r'^(?P<training_id>\d+)/process_results/$', views.process_results, name='process_results'),
                       #url(r'^(?P<training_id>\d+)/quiz/results/$', views.results, name='results'),
                       url(r'^generate_certificate/(?P<training_id>\d+)/$', helpers.generate_certificate, name='generate_certificate'),
                       url(r'^print_quiz/(?P<training_id>\d+)/$', helpers.print_quiz, name='print_quiz'),
                       url(r'^download_file/(?P<file_id>\d+)/$', helpers.download_file, name='download_file'),
                       url(r'^add_groups/', helpers.add_groups, name='add_groups'),
                    )

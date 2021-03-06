from django.views.generic import TemplateView
from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings

admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BAGCA.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    #url(r'^$', TemplateView.as_view(template_name='accounts/signup.html'), name="signup"),
    url(r'^$', include('quizzes.urls', namespace='quizzes'), name='index'),
    url(r'^show_course_trainings/(?P<group_id>\d+)/$', 'quizzes.views.show_course_trainings', name='show_course_trainings'),
    url(r'^profile$', 'quizzes.views.profile', name='profile'),
    url(r'^trainings/$', 'quizzes.views.trainings', name='trainings'),
    url(r'^trainings/(?P<training_id>\d+)/remove_assignment/$', 'quizzes.views.remove_user_assignment'),
    url(r'^user_assigned_training/', include('quizzes.urls', namespace="quizzes"), name='user_assigned_training'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'accounts/logout.html'}),
    url(r'^create_quiz_form/', 'quizzes.helpers.create_quiz_form', name='create_quiz_form'),
    url(r'^send_reminder_to_group/$', 'quizzes.helpers.send_reminder_to_group', name='send_reminder_to_group'),
    url(r'^send_reminder_to_user/$', 'quizzes.helpers.send_reminder_to_user', name='send_reminder_to_user'),
    #url(r'^send_reminder_for_quiz/$', 'quizzes.helpers.send_reminder_for_quiz', name='send_reminder_for_quiz'),
    url(r'^send_reminder_mail/$', 'quizzes.helpers.send_reminder_mail', name='send_reminder_mail'),
    url(r'^print_past_certificates/', 'quizzes.views.print_past_certificates', name='print_past_certificates'),
    url(r'^check_user_status/', 'quizzes.views.check_user_status', name='check_user_status'),
    url(r'^register_user/', 'quizzes.views.register', name='register_user'),
    url(r'^access_past_trainings/(?P<training_id>\d+)/$', 'quizzes.views.access_past_trainings', name='access_past_trainings'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT}),

)

from django.views.generic import TemplateView
from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BAGCA.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    #url(r'^$', TemplateView.as_view(template_name='accounts/signup.html'), name="signup"),
    url(r'^$', include('quizzes.urls', namespace='quizzes'), name='index'),
    url(r'^profile$', 'quizzes.views.profile', name='profile'),
    url(r'^trainings/$', 'quizzes.views.trainings', name='trainings'),
    url(r'^trainings/(?P<training_id>\d+)/remove_assignment/$', 'quizzes.views.remove_user_assignment'),
    url(r'^user_assigned_training/', include('quizzes.urls', namespace="quizzes"), name='user_assigned_training'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'accounts/logout.html'}),
    url(r'^create_quiz_form/', 'quizzes.helpers.create_quiz_form', name='create_quiz_form'),
    url(r'^print_past_certificates/', 'quizzes.views.print_past_certificates', name='print_past_certificates'),
    url(r'^register_user/', 'quizzes.views.register', name='register_user'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT}),

)

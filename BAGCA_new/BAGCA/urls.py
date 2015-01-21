from django.views.generic import TemplateView
from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BAGCA.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    #url(r'^$', TemplateView.as_view(template_name='accounts/signup.html'), name="signup"),
    url(r'^$', include('quizzes.urls', namespace="quizzes"), name="quizzes"),
    url(r'^trainings/', include('quizzes.urls', namespace="quizzes"), name="trainings"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'accounts/logout.html'}),
    

)

urlpatterns += patterns('',
               (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT}),
              )
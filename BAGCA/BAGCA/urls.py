from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BAGCA.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^quizzes/', include('quizzes.urls', namespace="quizzes")),
    url(r'^admin/', include(admin.site.urls)),
)

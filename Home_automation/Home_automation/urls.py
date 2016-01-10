from django.conf.urls import include, url
from django.contrib import admin
from application.views import index, switch, wire

urlpatterns = [
    # Examples:
    # url(r'^$', 'Home_automation.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', view=index, name="index"),
    url(r'^switch/(?P<nr>[0-9]+)/(?P<on>[0-9])/$', view=switch, name="switch"),
    url(r'^wire/(?P<on>[0-9])/$', view=wire, name="wire"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
       {'template_name': 'admin/login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
]

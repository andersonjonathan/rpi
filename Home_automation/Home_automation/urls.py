from django.conf.urls import include, url
from django.contrib import admin
from application.views import oldindex, index, switch, wire, plug

urlpatterns = [
    # Examples:
    # url(r'^$', 'Home_automation.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', view=oldindex, name="oldindex"),
    url(r'^new/$', view=index, name="index"),
    url(r'^plug/(?P<pk>[0-9]+)/(?P<status>[^/]+)/$', view=plug, name="plug"),
    url(r'^switch/(?P<nr>[0-9]+)/(?P<on>[^/]+)/$', view=switch, name="switch"),
    url(r'^wire/(?P<on>[^/]+)/$', view=wire, name="wire"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
       {'template_name': 'admin/login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
]

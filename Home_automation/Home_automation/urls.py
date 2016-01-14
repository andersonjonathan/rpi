from django.conf.urls import include, url
from django.contrib import admin
from application.views import index, switch
from django.contrib.auth.views import login, logout

urlpatterns = [
    # Examples:
    # url(r'^$', 'Home_automation.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', view=index, name="index"),
    url(r'^api/switch/(?P<pk>[0-9]+)/(?P<status>[^/]+)/$', view=switch, name="switch"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login, {'template_name': 'admin/login.html'}),
    url(r'^accounts/logout/$', logout),
]

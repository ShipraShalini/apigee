from django.conf.urls import patterns, include, url
from django.contrib import admin
from api import views as api
from items import views as items



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bidengine.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('^', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user_add/', api.add_user),
    url(r'^user_login/', api.user_login),
    url(r'^user_logout/', api.user_logout),
)



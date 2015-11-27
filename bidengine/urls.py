from django.conf.urls import patterns, include, url
from django.contrib import admin
from api import views



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bidengine.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('^', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user_add/', views.add_user),
    url(r'^user_login/', views.user_login),
    url(r'^user_logout/', views.user_logout),
)



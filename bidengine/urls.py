from django.conf.urls import patterns, include, url
from django.contrib import admin
from api import views



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bidengine.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', views.add_user),
    #url(r'^item/', views.item)

)



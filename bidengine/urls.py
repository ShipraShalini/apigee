from django.conf.urls import patterns, include, url
from django.contrib import admin
from users.user import user
from users.views import  login_message
from users.log_in_out import user_login, user_logout
from items.views_fold.item import item
from items.views_fold.bid import bid


urlpatterns = patterns('',
                       # Examples:
    # url(r'^$', 'bidengine.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('^', include('django.contrib.auth.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^user/', user),
                       url(r'^login_message/', login_message),
                       url(r'^user_login/', user_login),
                       url(r'^user_logout/', user_logout),
                       url(r'^item/', item),
                       url(r'^bid/', bid),
                       )



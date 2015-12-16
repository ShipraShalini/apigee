from django.conf.urls import patterns, include, url
from django.contrib import admin
from users import views as user
from items import views as item



urlpatterns = patterns('',
                       # Examples:
    # url(r'^$', 'bidengine.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('^', include('django.contrib.auth.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^user_add/', user.add_user),
                       url(r'^user_delete/', user.user_delete),
                       url(r'^user_modify/', user.user_modify),
                       url(r'^welcome/', item.welcome),
                       url(r'^user_login/', user.user_login),
                       url(r'^user_logout/', user.user_logout),
                       url(r'^add_item/', item.add_items),
                       url(r'^del_item/', item.del_items),
                       url(r'^view_item/', item.view_items),
                       url(r'^sell_item/', item.sell_items),
                       url(r'^login_message/', item.login_message),
                       url(r'^add_bid/', item.add_bid),
                       url(r'^del_bid/', item.del_bids),
                       url(r'^view_bids/', item.view_bids),
                       )



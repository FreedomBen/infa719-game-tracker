from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gameTracker.views.home', name='home'),
    # url(r'^gameTracker/', include('gameTracker.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

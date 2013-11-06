from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns( '',
    url( r'^$', 'gameTrackerApp.views.home' ),
    url( r'^home/$', 'gameTrackerApp.views.home' ),
    url( r'^login/$', 'gameTrackerApp.views.loginView' ),
    url( r'^register/$', 'gameTrackerApp.views.register' ),
    url( r'^prevTourn/$', 'gameTrackerApp.views.prevTourn' ),
    url( r'^create/$', 'gameTrackerApp.views.create' ),
    url( r'^join/$', 'gameTrackerApp.views.join' ),
    url( r'^view/$', 'gameTrackerApp.views.view' ),
	url( r'^logoutView/$', 'gameTrackerApp.views.logoutView' ),
    url( r'^admin/doc/', include( 'django.contrib.admindocs.urls' ) ),
    url( r'^admin/', include( admin.site.urls ) ),
) + static( settings.STATIC_URL, document_root=settings.STATIC_ROOT )

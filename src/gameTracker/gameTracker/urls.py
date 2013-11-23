from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

# These regular expressions translate a URL request into a python view function.  The view function pointed to is responsible for responding to the request with HTML
urlpatterns = patterns( '',
    url( r'^$', 'gameTrackerApp.views.home' ),
    url( r'^home/$', 'gameTrackerApp.views.home' ),
    url( r'^login/$', 'gameTrackerApp.views.loginView' ),
    url( r'^register/$', 'gameTrackerApp.views.register' ),
    url( r'^prevTourn/$', 'gameTrackerApp.views.prevTourn' ),
    url( r'^create/$', 'gameTrackerApp.views.create' ),
    url( r'^join/$', 'gameTrackerApp.views.join' ),
    url( r'^view/$', 'gameTrackerApp.views.view' ),
    url( r'^view/(\d{4}[A-Z]{2}\d{3}[A-Z]{2}\d+)$', 'gameTrackerApp.views.view' ),
    url( r'^joinack/(\d{4}[A-Z]{2}\d{3}[A-Z]{2}\d+)/([A-Z][A-Za-z" "]+[49ers]*)$', 'gameTrackerApp.views.joinack' ),
    url( r'^joinyes/(\d{4}[A-Z]{2}\d{3}[A-Z]{2}\d+)/([A-Z][A-Za-z" "]+[49ers]*)$', 'gameTrackerApp.views.joinyes' ),
    url( r'^declareWinner/(\d{4}[A-Z]{2}\d{3}[A-Z]{2}\d+)/(\d{1,2})$', 'gameTrackerApp.views.declareWinner' ),
    url( r'^joinno/$', 'gameTrackerApp.views.joinno' ),
	url( r'^logoutView/$', 'gameTrackerApp.views.logoutView' ),
    url( r'^admin/doc/', include( 'django.contrib.admindocs.urls' ) ),
    url( r'^admin/', include( admin.site.urls ) ),
) + static( settings.STATIC_URL, document_root=settings.STATIC_ROOT )

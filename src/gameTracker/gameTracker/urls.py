from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns( '',
    url( r'^login/$', 'gameTrackerApp.views.login' ),
    url( r'^register/createuser/$', 'gameTrackerApp.views.register_user' ),
    url( r'^register/$', 'gameTrackerApp.views.register' ),
    url( r'^default/$', 'gameTrackerApp.views.default' ),
    url( r'^admin/doc/', include( 'django.contrib.admindocs.urls' ) ),
    url( r'^admin/', include( admin.site.urls ) ),
) + static( settings.STATIC_URL, document_root=settings.STATIC_ROOT )

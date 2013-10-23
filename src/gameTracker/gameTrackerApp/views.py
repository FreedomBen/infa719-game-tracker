# main definition of view code

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

def login( request ):
    return render_to_response( 'login.html', { } )

def register( request ):
    return render_to_response( "register.html", { }, context_instance=RequestContext( request ) )

def default( request ):
    return render_to_response( "default.html", { } )

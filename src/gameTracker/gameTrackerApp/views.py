# main definition of view code

from django.http import HttpResponse
from django.shortcuts import render_to_response

def login( request ):
    return render_to_response( 'login.html', { } )

def register( request ):
    return render_to_response( "register.html", { } )


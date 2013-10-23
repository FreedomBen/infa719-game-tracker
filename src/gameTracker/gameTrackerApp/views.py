# main definition of view code

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

# This view serves the login page
def login( request ):
    return render_to_response( 'login.html', { } )

# This view serves the register page
def register( request ):
    return render_to_response( "register.html", { }, context_instance=RequestContext( request ) )

# This view processes the registration request
def register_user( request ):
    # validate our data server side before processing it
    pass

# This view is for testing the default template
def default( request ):
    return render_to_response( "default.html", { } )

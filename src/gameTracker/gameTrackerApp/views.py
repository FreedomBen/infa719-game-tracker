# main definition of view code

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from gameTrackerApp.models import *

import validate

# This view serves the login page
def login( request ):
    return render_to_response( 'login.html', { } )

# This view serves the register page
def register( request ):
    return render_to_response( "register.html", { }, context_instance=RequestContext( request ) )

# This view processes the registration request
def register_user( request ):
    # validate our data server side before processing it
    first    = validate.validateName( request.POST['firstName'] )
    last     = validate.validateName( request.POST['lastName'] )
    email    = validate.validateEmail( request.POST['emailAddress'] )
    password = validate.validatePassword( request.POST['password'] )
    twitter  = validate.validateTwitter( request.POST['twitter'] )

    if( request.POST['password'] != request.POST['passwordCheck'] ):
        password = "Passwords must match"

    if not first or not last or not email or not password or not twitter or not passwordCheck:
        return render_to_response( 'register.html', {
            'firstName'    : first,
            'lastName'     : last,
            'emailAddress' : email,
            'password'     : password,
            'twitter'      : twitter
        }, context_instance=RequestContext( request ) )

    else:
        # Create the user
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return render_to_response( 'register_success.html', {
            'firstName'    : request.POST['firstName'],
            'lastName'     : request.POST['lastName'],
            'emailAddress' : request.POST['email'],
            'password'     : request.POST['password'],
            'twitter'      : request.POST['twitter']
        }, context_instance=RequestContext( request ) ) 


# This view is for testing the default template
def default( request ):
    return render_to_response( "default.html", { } )

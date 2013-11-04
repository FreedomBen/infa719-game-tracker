# main definition of view code

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from gameTrackerApp.models import *

import validate


# This view processes the registration request and handles displaying the register page
# If registration succeeds the user is served to a success page
def register( request ):
    # if this is a GET then just return the normal page
    if request.method == 'GET':
        return render_to_response( "register.html", { }, context_instance=RequestContext( request ) )

    else:
        # validate our data server side before processing it
        first    = validate.validateName( request.POST['firstName'] )
        last     = validate.validateName( request.POST['lastName'] )
        email    = validate.validateEmail( request.POST['emailAddress'] )
        password = validate.validatePassword( request.POST['password'] )

        if( request.POST['password'] != request.POST['passwordCheck'] ):
            password = "Passwords must match"

        if len( first ) > 0 or len( last ) > 0  or len( email ) > 0 or len( password ) > 0:
            return render_to_response( 'register.html', {
                'firstName'         : first,
                'lastName'          : last,
                'emailAddress'      : email,
                'password'          : password,
                'prevFirstName'     : request.POST['firstName'],
                'prevLastName'      : request.POST['lastName'],
                'prevEmailAddress'  : request.POST['emailAddress'],
                'prevPassword'      : request.POST['password'],
                'prevPasswordCheck' : request.POST['passwordCheck'],
                'prevTwitter'       : request.POST['twitter']
            }, context_instance=RequestContext( request ) )

        else:
            # Create the user
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            try:
                new_user = User.objects.create_user( request.POST['username'], request.POST['emailAddress'], request.POST['password'] ) 
            except IntegrityError:
                # user already exists
                return render_to_response( 'register.html', {
                    'username'          : 'User already exists',
                    'prevFirstName'     : request.POST['firstName'],
                    'prevLastName'      : request.POST['lastName'],
                    'prevEmailAddress'  : request.POST['emailAddress'],
                    'prevPassword'      : request.POST['password'],
                    'prevPasswordCheck' : request.POST['passwordCheck'],
                    'prevTwitter'       : request.POST['twitter']
                }, context_instance=RequestContext( request ) )
            else:
                new_user.first_name = request.POST['firstName']
                new_user.last_name  = request.POST['lastName']
                new_user.email      = request.POST['emailAddress']
                new_user.password   = request.POST['password']
                # User table does not have a twitter member

                return render_to_response( 'register_success.html', {
                    'firstName'    : new_user.first_name,
                    'lastName'     : new_user.last_name,
                    'emailAddress' : new_user.email,
                    # 'twitter'      : new_user.first_name,
                }, context_instance=RequestContext( request ) ) 

# This view serves the home page
def home( request ):
	#direct user to login page if username session is not set
	if 'SESusername' not in request.session:
		return render_to_response( "login.html", { }, context_instance=RequestContext( request ) )
	
	else:
		request.session.modified = True
		return render_to_response( "home.html", {
		'username'		: request.session['SESusername'],
		},context_instance=RequestContext( request )
		)

# This view is for testing the default template
def default( request ):
    return render_to_response( "default.html", { } )

	
def login( request ):
    if request.method == 'GET':
		return render_to_response( "login.html", { }, context_instance=RequestContext( request ) )
	
    request.session['SESusername']=request.POST['user']
    request.session['SESpassword']=request.POST['password']
    request.session.modified = True
    return render_to_response( "home.html", {
	'username'		: request.session['SESusername'],
	},context_instance=RequestContext( request )
	)
	
def prevTourn( request ):
	#direct user to login page if username session is not set
	if 'SESusername' not in request.session:
		return render_to_response( "login.html", { }, context_instance=RequestContext( request ) )
	
	else:
		return render_to_response( "prevTourn.html", {
		'username'		: request.session['SESusername'],
		},context_instance=RequestContext( request )
		)
		
def create( request ):
	#direct user to login page if username session is not set
	if 'SESusername' not in request.session:
		return render_to_response( "login.html", { }, context_instance=RequestContext( request ) )
	
	#return blank form for GET request
	if request.method == 'GET':
		return render_to_response( "create.html", {
		'username'		: request.session['SESusername'],
		},context_instance=RequestContext( request )
		)
	#process input data before responding back
	else:
		startDate       = validate.validateStartDate( request.POST['startDate'] )
        startTime       = validate.validateStartTime( request.POST['startTime'] )
        difficulty      = validate.validateDifficulty( request.POST['difficulty'] )
        quarterLength   = validate.validateQuarterLength( request.POST['quarterLength'] )
        nextRound       = validate.validateNextRound( request.POST['startTime'] )
        randomBy        = validate.validateRandomBy( request.POST['randomBy'] )
        team            = validate.validateTeam( request.POST['team'] )

	return render_to_response( "home.html", {
	'username'		: request.session['SESusername'],
	'message'       : "Tournament Successfully Created",
	},context_instance=RequestContext( request )
	)

def join( request ):
	#direct user to login page if username session is not set
	if 'SESusername' not in request.session:
		return render_to_response( "login.html", { }, context_instance=RequestContext( request ) )
	
	else:
		return render_to_response( "join.html", {
		'username'		: request.session['SESusername'],
		},context_instance=RequestContext( request )
		)


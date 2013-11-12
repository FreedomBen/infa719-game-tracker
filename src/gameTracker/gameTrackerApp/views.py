# main definition of view code

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from gameTrackerApp.models import *
import validate
import time
import datetime
from gameTrackerApp.modelHelper import *
import functions


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
        username = validate.validateName( request.POST['username'] )
        email    = validate.validateEmail( request.POST['emailAddress'] )
        password = validate.validatePassword( request.POST['password'] )

        if( request.POST['password'] != request.POST['passwordCheck'] ):
            password = "Passwords must match"

        # if any of the validation returned an error, the error 
        # message will be displayed to the user
        if len( first ) > 0 or len( last ) > 0  or len( username ) > 0 or len( email ) > 0 or len( password ) > 0:
            return render_to_response( 'register.html', {
                'firstName'         : first,
                'lastName'          : last,
                'username'          : username,
                'emailAddress'      : email,
                'password'          : password,
                'prevFirstName'     : request.POST['firstName'],
                'prevLastName'      : request.POST['lastName'],
                'prevUsername'      : request.POST['username'],
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
        
        b = TournamentMembers.objects.filter(user_id=request.session['SESusername']) 
        registered=[]
        
        for a in b:
            tourny = Tournament.objects.get(id=a.tournament_id)
            registered.append(tourny.tournament_name)
        
        b = Tournament.objects.filter(is_private=0)
        for a in b:
            if a.tournament_name not in registered:
                registered.append(a.tournament_name)
        
        return render_to_response( "home.html", {
        'username'      : request.session['SESusername'],
        'reg'           : registered,
        'notreg'        : ' You are currently not registered for any tournaments',
        },context_instance=RequestContext( request )
        )
        
        return render_to_response( "home.html", {
        'username'      : request.session['SESusername'],
        },context_instance=RequestContext( request )
        )

# This view is for testing the default template
# This page is not accessable to the user, it is the 
# template for the web site.
def default( request ):
    return render_to_response( "default.html", { } )

# This view is used when a user requests to log out
def logoutView(request):
    logout( request )
    return render_to_response( "login.html", { 
        'message' : 'Successfully logged out' 
    }, context_instance=RequestContext( request ) )
    
# This view is used for POST and GET to the login page  
def loginView( request ):
    if request.method == 'GET':
        return render_to_response( "login.html", { }, context_instance=RequestContext( request ) )
    
    user = authenticate( username=request.POST['username'], password=request.POST['password'] )

    if user is not None and user.is_active:
            login( request, user )
            # success
            request.session['SESusername']=user.username
            request.session.modified = True
            return render_to_response( "home.html", {
                    'username'      : user.username,
                },context_instance=RequestContext( request )
            )
    else:
        # Not authenticated
        return render_to_response( "login.html", { 
            'error' : 'Your information was invalid.  Please try again' 
        }, context_instance=RequestContext( request ) )

# This view is used to display the past tournaments
# that the user has been in 
def prevTourn( request ):
    #direct user to login page if username session is not set
    if 'SESusername' not in request.session:
        return render_to_response( "login.html", { }, context_instance=RequestContext( request ) )
    
    else:
        return render_to_response( "prevTourn.html", {
        'username'      : request.session['SESusername'],
        },context_instance=RequestContext( request )
        )

# This view is used when a user requests to create a new 
# tournament.
def create( request ):
    #direct user to login page if username session is not set
    if 'SESusername' not in request.session:
        return render_to_response( "login.html", { }, context_instance=RequestContext( request ) )
    
    curday = time.strftime('%Y-%m-%d')

    #return blank form for GET request
    if request.method == 'GET':
        return render_to_response( "create.html", {
        'username'          : request.session['SESusername'],
        'prevSignStartDate' : curday,
        'prevPrivate'       : ['True','False'],
        'prevRoundLength'   : NEXT_ROUND,
        'prevQuarterLength' : QUARTER_LENGTH,
        'prevDifficulty'    : Tournament.DIFFICULTY_LEVELS,
        'prevRandomBy'      : RANDOM_BY,
        'prevteam'          : NFL_TEAMS,
        'dateMsg'           : "YYYY-MM-DD"
        },context_instance=RequestContext( request )
        )
    
    
    
    #process input data before responding back
    else:
        isPrivate           = validate.validatePrivate(request.POST['private'])
        signStartDate       = validate.validateDate( request.POST['signStartDate'] )
        signCloseDate       = validate.validateDate( request.POST['signCloseDate'] )
        tournyOpenDate      =validate.validateDate(request.POST['tournyOpenDate'])
        roundLength         =validate.validateRoundLength(request.POST['roundLength'])
        quarterLength   = validate.validateQuarterLength( request.POST['quarterLength'] )
        difficulty      = validate.validateDifficulty( request.POST['difficulty'] )
        randomBy        = validate.validateRandomBy( request.POST['randomBy'] )
        team            = validate.validateTeam( request.POST['team'] )
    
    if len(team) > 0 or len(difficulty) > 0 or len(quarterLength) >0 or len(randomBy) > 0 or len(signCloseDate) > 0 or len(roundLength) > 0 or len(signStartDate) > 0 or len(tournyOpenDate) > 0 or len(isPrivate) > 0:
        
        return render_to_response( "create.html", {
        'username'      : request.session['SESusername'],
        'private'       : isPrivate,
        'signStartDate' : signStartDate,
        'signCloseDate' : signCloseDate,
        'tournyOpenDate': tournyOpenDate,
        'roundLength'   : roundLength,
        'quarterLength' : quarterLength,
        'difficulty'    : difficulty,
        'randomBy'      : randomBy,
        'team'          : team,
        'prevPrivate'       : ['True','False'],
        'prevRoundLength'       : NEXT_ROUND,
        'prevQuarterLength' : QUARTER_LENGTH,
        'prevDifficulty'    : Tournament.DIFFICULTY_LEVELS,
        'prevRandomBy'      : RANDOM_BY,
        'prevteam'          : NFL_TEAMS,
        'message'           : "tournament not created due to error",
        # 'message'         : name,
        },context_instance=RequestContext( request )
        )

    else:
        #create the tournament in the database
        try:
            (year, month, day) = curday.split('-')
            year = int(year)
            month = int(month)
            day = int(day)
            t = time.mktime((year, month, day, 0, 0, 0, 0, 0, 0))
            num = Tournament.objects.filter(date_created = curday).count()
            julian = time.gmtime(t)[7]
            num = Tournament.objects.filter(date_created = curday).count()
            name = str(year) + functions.getLetter() + str(julian) + functions.getLetter() + str(num)
                
            newT = Tournament(
                is_private              = functions.getBoolean(request.POST['private']),
                tournament_name         = name,
                created_by              = request.session['SESusername'],
                date_created            = curday,
                signup_open_datetime    = request.POST['signStartDate'],
                signup_close_datetime   = request.POST['signCloseDate'],
                tournament_open_datetime= request.POST['tournyOpenDate'],
                round_length            = request.POST['roundLength'],
                quarter_length          = request.POST['quarterLength'],
                difficulty_level        = request.POST['difficulty'],
            )
            
        except:
            # This is in case there was an error inserting the tournament into the database and the tournament was not created
            return render_to_response( "create.html", {
            'username'          : request.session['SESusername'],
            'prevteam'          : NFL_TEAMS,
            'prevDifficulty'    : Tournament.DIFFICULTY_LEVELS,
            'prevQuarterLength' : QUARTER_LENGTH,
            'prevRandomBy'      : RANDOM_BY,
            'prevStartTime'     : START_TIME,
            'prevNextRound'     : NEXT_ROUND,
            'message'           : "failed to create tournament"
            },context_instance=RequestContext( request )
            )
            
        else:
            # This actually updates the database
            newT.save()
        
        try:
            newM=TournamentMembers(
                user_id      = request.session['SESusername'],
                tournament  = Tournament.objects.get(tournament_name=name),
                )
        except:
            # This is in case there was an error inserting the member into the database and the member was not created
            return render_to_response( "create.html", {
            'username'          : request.session['SESusername'],
            'prevteam'          : NFL_TEAMS,
            'prevDifficulty'    : Tournament.DIFFICULTY_LEVELS,
            'prevQuarterLength' : QUARTER_LENGTH,
            'prevRandomBy'      : RANDOM_BY,
            'prevStartTime'     : START_TIME,
            'prevNextRound'     : NEXT_ROUND,
            'message'           : "failed to create member"
            },context_instance=RequestContext( request )
            )
        
        else:
            newM.save()
        
        return render_to_response( "home.html", {
        'username'      : request.session['SESusername'],
        'message'       : 'Tournament Successfully Created',
        },context_instance=RequestContext( request )
        )

# This view is used to display the tournaments that the 
# user is eligable to join.
def join( request ):
    #direct user to login page if username session is not set
    if 'SESusername' not in request.session:
        return render_to_response( "login.html", { }, context_instance=RequestContext( request ) )
    
    else:
        curday = datetime.datetime.now()
        
        b = Tournament.objects.filter(tournament_open_datetime__gte=curday)
        
        # return render_to_response( "join.html", {
        # 'username'        : request.session['SESusername'],
        # 'message'     :  curday,
        # },context_instance=RequestContext( request )
        # )
        
        # this creates the header for the table
        c = ['Tournament','Creator','Signup Closes at','Tournament Starts at', 'Quarter Length', 'Difficulty']
        d = []
        d.append(c)
        
        # This finds the tournaments the the user is eligable to 
        # join.
        b = Tournament.objects.filter(signup_close_datetime__gt=str(curday)).exclude(is_private=1).exclude(created_by=request.session['SESusername'])
        
        if not b:
            return render_to_response( "join.html", {
            'username'      : request.session['SESusername'],
            'message'       : "You are not currently eligable to join in any tournaments",
            },context_instance=RequestContext( request )
            )
        
        for a in b:
            c = [a.tournament_name.encode('ascii','ignore'), 
            a.created_by, 
            a.signup_close_datetime.strftime('%Y-%m-%d'),
            a.tournament_open_datetime.strftime('%Y-%m-%d'), 
            a.quarter_length, 
            difAbbrToName(a.difficulty_level) ]
            d.append(c)
            
        return render_to_response( "join.html", {
        'username'      : request.session['SESusername'],
        'info'      : d,
        'message'   : curday,
        },context_instance=RequestContext( request )
        )

# This view allows the user to see the bracket for a selected 
# tournament
def view(request):
    if 'SESusername' not in request.session:
        return render_to_response( "login.html", { }, context_instance=RequestContext( request ) )
    
    else:
    
        
        return render_to_response( "view.html", {
        'username'      : request.session['SESusername'],
        },context_instance=RequestContext( request )
        )
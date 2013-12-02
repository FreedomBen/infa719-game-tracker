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
        q1       = validate.validateName( request.POST[ 'q1' ] )
        q2       = validate.validateName( request.POST[ 'q2' ] )
        q3       = validate.validateName( request.POST[ 'q3' ] )

        if( request.POST['password'] != request.POST['passwordCheck'] ):
            password = "Passwords must match"

        # if any of the validation returned an error, the error 
        # message will be displayed to the user
        if len( first ) > 0 or len( last ) > 0 or len( username ) > 0 or len( email ) > 0 or len( password ) > 0 \
                len( q1 ) > 0 or len( q2 ) > 0 or len( q3 ):
            return render_to_response( 'register.html', {
                'firstName'         : first,
                'lastName'          : last,
                'username'          : username,
                'emailAddress'      : email,
                'password'          : password,
                'q1'                : q1,
                'q2'                : q2,
                'q3'                : q3,
                'prevFirstName'     : request.POST['firstName'],
                'prevLastName'      : request.POST['lastName'],
                'prevUsername'      : request.POST['username'],
                'prevEmailAddress'  : request.POST['emailAddress'],
                'prevPassword'      : request.POST['password'],
                'prevPasswordCheck' : request.POST['passwordCheck'],
                'prevTwitter'       : request.POST['twitter']
                'prevq1'            : request.POST['q1']
                'prevq2'            : request.POST['q2']
                'prevq3'            : request.POST['q3']
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
                    'prevq1'            : request.POST['q1']
                    'prevq2'            : request.POST['q2']
                    'prevq3'            : request.POST['q3']
                }, context_instance=RequestContext( request ) )
            else:
                new_user.first_name = request.POST['firstName']
                new_user.last_name  = request.POST['lastName']
                new_user.email      = request.POST['emailAddress']
                new_user.password   = request.POST['password']
                # User table does not have a twitter member

                # Save questions in the new table
                cq              = ChallengeQuestions()
                cq.user_id      = new_user.pk
                cq.answer_one   = request.POST['q1']
                cq.answer_two   = request.POST['q2']
                cq.answer_three = request.POST['q3']

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
        
        registered = functions.getJoinedTournaments(request.session['SESusername'])
        
        return render_to_response( "home.html", {
        'username'      : request.session['SESusername'],
        'reg'           : registered,
        'notreg'        : ' You are currently not registered for any tournaments',
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
            registered = functions.getJoinedTournaments(request.session['SESusername'])
        
            return render_to_response( "home.html", {
            'username'      : request.session['SESusername'],
            'reg'           : registered,
            'notreg'        : ' You are currently not registered for any tournaments',
            },context_instance=RequestContext( request )
            )
            
    else:
        # Not authenticated
        return render_to_response( "login.html", { 
            'error' : 'Your information was invalid.  Please try again' 
        }, context_instance=RequestContext( request ) )


# This view is used for resetting a user's password
def forgotpassword( request ):
    if request.method == 'GET':
        return render_to_response( "forgot_password.html", { }, context_instance=RequestContext( request ) )
    

def resetpassword( request ):
    if ( request.method == 'GET' ) || ( len( User.objects.get( username__exact=request.POST[ 'username' ] ) ) != 1 ):
        # GET requeset or invalid username
        return render_to_response( "forgot_password.html", { 
            'error'        : 'Please enter a valid username',
        }, context_instance=RequestContext( request ) )

    else: 
        user = User.objects.get( username__exact=request.POST[ 'username' ] )
        for qa in ChallengeQuestions.objects.all():
            if qa.user_id == user.pk:
                q = qa
                break

        if len( request.POST[ 'q1' ] ) < 1 and len( request.POST[ 'q2' ] ) < 1 and len( request.POST[ 'q3' ] ) < 1: 
            # valid username no question answers, display page for answering questions

        elif ( request.POST[ 'q1' ] == q.answer_one ) and ( request.POST[ 'q2' ] == q.answer_two ) and ( request.POST[ 'q3' ] == q.answer_three ): 
            # valid username correct question answers, apply the change and return change success
            if len( validatePassword( request.POST[ 'newpassword' ] ) ) > 0:
                return render_to_response( "reset_password.html", {
                    'error' : validatePassword( request.POST[ 'newpassword' ] )
                }, context_instance=RequestContext( request ) )
            else:
                user.set_password( request.POST[ 'newpassword' ] )
                user.save()

        elif:
            # valid username wrong question answers
            return render_to_response( "reset_password.html", {
                'error' : 'Incorrect Answers.  Try again.' )
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
        'prevPrivate'       : ['True','False'],
        'prevRoundLength'   : NEXT_ROUND,
        'prevQuarterLength' : QUARTER_LENGTH,
        'prevDifficulty'    : Tournament.DIFFICULTY_LEVELS,
        'prevRandomBy'      : RANDOM_BY,
        'prevteam'          : NFL_TEAMS,
        'dateMsg'           : "YYYY-MM-DD",
        'timeMsg'           : "HH:MM - 24 Hour format, 1PM = 13:00",
        'message'           : curday,
        },context_instance=RequestContext( request )
        )
    
    
    
    #process input data before responding back
    else:
        isPrivate           = validate.validatePrivate(request.POST['private'])
        signStartDate       = validate.validateDate( request.POST['signStartDate'] )
        signStartTime       = validate.validateTime(request.POST['signStartTime'])
        signCloseDate       = validate.validateDate( request.POST['signCloseDate'] )
        signCloseTime       = validate.validateTime(request.POST['signCloseTime'])
        tournyOpenDate      = validate.validateDate(request.POST['tournyOpenDate'])
        tournyOpenTime      = validate.validateTime(request.POST['tournyOpenTime'])
        roundLength         = validate.validateRoundLength(request.POST['roundLength'])
        quarterLength       = validate.validateQuarterLength( request.POST['quarterLength'] )
        difficulty          = validate.validateDifficulty( request.POST['difficulty'] )
        randomBy            = validate.validateRandomBy( request.POST['randomBy'] )
        team                = validate.validateTeam( request.POST['team'] )
    
    if len(team) > 0 or len(difficulty) > 0 or len(quarterLength) >0 or len(randomBy) > 0 or len(signCloseDate) > 0 or len(roundLength) > 0 or len(signStartDate) > 0 or len(tournyOpenDate) > 0 or len(isPrivate) > 0 or len(signStartTime) > 0 or len(signCloseTime) > 0 or len(tournyOpenTime) > 0:
        
        return render_to_response( "create.html", {
        'username'      : request.session['SESusername'],
        'private'       : isPrivate,
        'signStartDate' : signStartDate,
        'signStartTime' : signStartTime,
        'signCloseDate' : signCloseDate,
        'signCloseTime' : signCloseTime,
        'tournyOpenDate': tournyOpenDate,
        'tournyOpenTime': tournyOpenTime,
        'roundLength'   : roundLength,
        'quarterLength' : quarterLength,
        'difficulty'    : difficulty,
        'randomBy'      : randomBy,
        'team'          : team,
        'prevPrivate'       : ['True','False'],
        'prevSignStartDate' : request.POST['signStartDate'],
        'prevSignStartTime' : request.POST['signStartTime'],
        'prevSignCloseDate' : request.POST['signCloseDate'],
        'prevSignCloseTime' : request.POST['signCloseTime'],
        'prevTournyOpenDate': request.POST['tournyOpenDate'],
        'prevTournyOpenTime': request.POST['tournyOpenTime'],
        'prevRoundLength'   : NEXT_ROUND,
        'prevQuarterLength' : QUARTER_LENGTH,
        'prevDifficulty'    : Tournament.DIFFICULTY_LEVELS,
        'prevRandomBy'      : RANDOM_BY,
        'prevteam'          : NFL_TEAMS,
        'message'           : "tournament not created due to error",
        'dateMsg'           : "YYYY-MM-DD",
        'timeMsg'           : "HH:MM - 24 Hour format, 1PM = 13:00",
        # 'message'         : name,
        },context_instance=RequestContext( request )
        )

    else:
        #create the tournament in the database
        try:
        #if True:
            (year, month, day) = curday.split('-')
            year = int(year)
            month = int(month)
            day = int(day)
            t = time.mktime((year, month, day, 0, 0, 0, 0, 0, 0))
            num = Tournament.objects.filter(date_created = curday).count()
            julian = time.gmtime(t)[7]
            num = Tournament.objects.filter(date_created = curday).count()
            name = str(year) + functions.getLetter() + str(julian) + functions.getLetter() + str(num)
                
            signOpen = functions.convertDate(request.POST['signStartDate'], request.POST['signStartTime'])
            signClose = functions.convertDate(request.POST['signCloseDate'], request.POST['signCloseTime'])
            tournyOpen = functions.convertDate(request.POST['tournyOpenDate'], request.POST['tournyOpenTime'])
            
            newT = Tournament(
                is_private              = functions.getBoolean(request.POST['private']),
                tournament_name         = name,
                created_by              = request.session['SESusername'],
                date_created            = curday,
                #signup_open_date        = str(request.POST['signStartDate']) + ' ' + str(request.POST['signStartTime']),
                signup_open_datetime        = signOpen,
                signup_close_datetime       = signClose,
                tournament_open_datetime    = tournyOpen,
                round_length            = request.POST['roundLength'],
                quarter_length          = request.POST['quarterLength'],
                difficulty_level        = request.POST['difficulty'],
                current_round           = 0,
            )
            
        except:
        #if True:
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
            #'message'           : signOpen
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
        
        tObject = Tournament.objects.get(tournament_name=name)
        
        functions.createGames(tObject,request.POST['difficulty'])
        
        try:
            #check if user selected team is team 1
            myGame = Game.objects.get(tournament_id=tObject.id,team_one=request.POST['team'])
            
            myGame.team_one_user = request.session['SESusername']
        except:
            try:
                #check if user selected team is team 2
            
        
                myGame = Game.objects.get(tournament_id=tObject.id,team_two=request.POST['team'])
            
                myGame.team_two_user = request.session['SESusername']
            
            except:
                #user selected team could not be found *error*
                registered = functions.getJoinedTournaments(request.session['SESusername'])
                return render_to_response( "home.html", {
                'username'      : request.session['SESusername'],
                'reg'           : registered,
                'notreg'        : ' You are currently not registered for any tournaments',
                'message'       : 'error selecting your team, the tournament was created, but you do not have your selected team',
                },context_instance=RequestContext( request )
                )
        myGame.save()
        registered = functions.getJoinedTournaments(request.session['SESusername'])
        return render_to_response( "home.html", {
        'username'      : request.session['SESusername'],
        'reg'           : registered,
        'notreg'        : ' You are currently not registered for any tournaments',
        'message'       : 'Tournament Successfully Created',
        #'message'       : signOpen,           
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

        # This finds the tournaments the the user is eligable to 
        # join.
        
        if request.method == 'GET':
            b = Tournament.objects.filter(signup_close_datetime__gt=str(curday), is_private=0).exclude(tournamentmembers__user_id__exact=request.session['SESusername'])
        
        else:
            name = request.POST['tournament']
            res = validate.validateTournyName(name)
            if len(res) > 0:
                return render_to_response( "join.html", {
                'username'      : request.session['SESusername'],
                'invalid'       : "That was an invalid tournament name",
                },context_instance=RequestContext( request )
                )
            b = Tournament.objects.filter(tournament_name=name)
        if not b:
            return render_to_response( "join.html", {
            'username'      : request.session['SESusername'],
            'message'       : "You are not currently eligable to join in any tournaments",
            },context_instance=RequestContext( request )
            )
        # this creates the header for the table
        c = ['Tournament','Creator','Signup Closes at','Tournament Starts at', 'Quarter Length', 'Difficulty']
        d = []
        d.append(c)
        for a in b:
            c = [a.tournament_name.encode('ascii','ignore'), 
            a.created_by, 
            #a.signup_close_datetime.strftime('%Y-%m-%d'),
            a.signup_close_datetime,
            #a.tournament_open_datetime.strftime('%Y-%m-%d'), 
            a.tournament_open_datetime, 
            a.quarter_length, 
            difAbbrToName(a.difficulty_level) ]
            d.append(c)
            
        return render_to_response( "join.html", {
        'username'      : request.session['SESusername'],
        'info'      : d,
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
        'message'       : "no tournament selected"
        },context_instance=RequestContext( request )
        )
              
def view(request, tourny):
    if 'SESusername' not in request.session:
        return render_to_response( "login.html", { }, context_instance=RequestContext( request ) )
    
    else:
    
        tObject = Tournament.objects.get(tournament_name=tourny)
        
        round = tObject.current_round
        
        if round < 6:
            curtime = time.strftime('%Y-%m-%d %H:%M')
            if round == 0:
                end = datetime.datetime.strptime(tObject.signup_close_datetime, '%Y-%m-%d %H:%M')
                end = end.strftime('%Y-%m-%d %H:%M')
                if curtime > end:
                    tObject.current_round = -1
                    tObject.save()
            
            else:
                start = datetime.datetime.strptime(tObject.tournament_open_datetime,'%Y-%m-%d %H:%M')
                length = tObject.round_length
                (H,M) = length.split(':')
                roundEnd = start + datetime.timedelta(hours=int(H))
                
                roundEnd = roundEnd.strftime('%Y-%m-%d %H:%M')
                
                if curtime > roundEnd:
                    functions.nextRound(tObject,roundEnd)
        
        round = tObject.current_round
        game1 = functions.getGame(tObject.id,1)
        game2 = functions.getGame(tObject.id,2)
        game3 = functions.getGame(tObject.id,3)
        game4 = functions.getGame(tObject.id,4)
        game5 = functions.getGame(tObject.id,5)
        game6 = functions.getGame(tObject.id,6)
        game7 = functions.getGame(tObject.id,7)
        game8 = functions.getGame(tObject.id,8)
        game9 = functions.getGame(tObject.id,9)
        game10 = functions.getGame(tObject.id,10)
        game11 = functions.getGame(tObject.id,11)
        game12 = functions.getGame(tObject.id,12)
        game13 = functions.getGame(tObject.id,13)
        game14 = functions.getGame(tObject.id,14)
        game15 = functions.getGame(tObject.id,15)
        game16 = functions.getGame(tObject.id,16)
        game17 = functions.getGame(tObject.id,17)
        game18 = functions.getGame(tObject.id,18)
        game19 = functions.getGame(tObject.id,19)
        game20 = functions.getGame(tObject.id,20)
        game21 = functions.getGame(tObject.id,21)
        game22 = functions.getGame(tObject.id,22)
        game23 = functions.getGame(tObject.id,23)
        game24 = functions.getGame(tObject.id,24)
        game25 = functions.getGame(tObject.id,25)
        game26 = functions.getGame(tObject.id,26)
        game27 = functions.getGame(tObject.id,27)
        game28 = functions.getGame(tObject.id,28)
        game29 = functions.getGame(tObject.id,29)
        game30 = functions.getGame(tObject.id,30)
        game31 = functions.getGame(tObject.id,31)
        return render_to_response( "view.html", {
        'username'      : request.session['SESusername'],
        'message'       : tourny,
        #'message'       : roundEnd,
        'round'       : round,   
        'game1'         : game1,
        'game2'         : game2,
        'game3'         : game3,
        'game4'         : game4,
        'game5'         : game5,
        'game6'         : game6,
        'game7'         : game7,
        'game8'         : game8,
        'game9'         : game9,
        'game10'         : game10,
        'game11'         : game11,
        'game12'         : game12,
        'game13'         : game13,
        'game14'         : game14,
        'game15'         : game15,
        'game16'         : game16,
        'game17'         : game17,
        'game18'         : game18,
        'game19'         : game19,
        'game20'         : game20,
        'game21'         : game21,
        'game22'         : game22,
        'game23'         : game23,
        'game24'         : game24,
        'game25'         : game25,
        'game26'         : game26,
        'game27'         : game27,
        'game28'         : game28,
        'game29'         : game29,
        'game30'         : game30,
        'game31'         : game31,
        },context_instance=RequestContext( request )
        )

    
        
def joinack(request, tourny, teamName):
    team = teamNameToAbbreviation(teamName)
    game = functions.findTeamInGame(tourny,team,request.session['SESusername'])

    if game == 1:
        registered = functions.getJoinedTournaments(request.session['SESusername'])
        return render_to_response( "home.html", {
            'username'      : request.session['SESusername'],
            'reg'           : registered,
            'notreg'        : ' You are currently not registered for any tournaments',
            'message'       : 'error finding the tournament you requested to join',
            },context_instance=RequestContext( request )
            )
    if game == 2:
        registered = functions.getJoinedTournaments(request.session['SESusername'])
        return render_to_response( "home.html", {
            'username'      : request.session['SESusername'],
            'reg'           : registered,
            'notreg'        : ' You are currently not registered for any tournaments',
            'message'       : 'you are only allowed to be entered in each tournament one time',
            },context_instance=RequestContext( request )
            )
    if game == 3:
                registered = functions.getJoinedTournaments(request.session['SESusername'])
                return render_to_response( "home.html", {
                'username'      : request.session['SESusername'],
                'reg'           : registered,
                'notreg'        : ' You are currently not registered for any tournaments',
                'message'       : 'there was an error selecting your team',
                },context_instance=RequestContext( request )
                )
    
    return render_to_response( "joinack.html", {
            'username'      : request.session['SESusername'],
            'tournament'    : tourny,
            'team'          : teamName,
            },context_instance=RequestContext( request )
            )
            
def joinyes(request, tourny, teamName):
    team = teamNameToAbbreviation(teamName)
    game = functions.findTeamInGame(tourny,team,request.session['SESusername'])
    
    if game == 1:
        registered = functions.getJoinedTournaments(request.session['SESusername'])
        return render_to_response( "home.html", {
            'username'      : request.session['SESusername'],
            'reg'           : registered,
            'notreg'        : ' You are currently not registered for any tournaments',
            'message'       : 'error finding the tournament you requested to join',
            },context_instance=RequestContext( request )
            )
    if game == 2:
        registered = functions.getJoinedTournaments(request.session['SESusername'])
        return render_to_response( "home.html", {
            'username'      : request.session['SESusername'],
            'reg'           : registered,
            'notreg'        : ' You are currently not registered for any tournaments',
            'message'       : 'you are only allowed to be entered in each tournament one time',
            },context_instance=RequestContext( request )
            )
    if game == 3:
                registered = functions.getJoinedTournaments(request.session['SESusername'])
                return render_to_response( "home.html", {
                'username'      : request.session['SESusername'],
                'reg'           : registered,
                'notreg'        : ' You are currently not registered for any tournaments',
                'message'       : 'there was an error selecting your team',
                },context_instance=RequestContext( request )
                )
    
    if game.team_one == team:
        if game.team_one_user == None:
            game.team_one_user = request.session['SESusername']
            game.save()
        else:
            registered = functions.getJoinedTournaments(request.session['SESusername'])
            return render_to_response( "home.html", {
                'username'      : request.session['SESusername'],
                'reg'           : registered,
                'notreg'        : ' You are currently not registered for any tournaments',
                'message'       : 'another user has already selected this team in this tournament',
                },context_instance=RequestContext( request )
                )
        
    else:
        if game.team_two_user == None:
            game.team_two_user = request.session['SESusername']
            game.save()
        else:
            registered = functions.getJoinedTournaments(request.session['SESusername'])
            return render_to_response( "home.html", {
                'username'      : request.session['SESusername'],
                'reg'           : registered,
                'notreg'        : ' You are currently not registered for   any tournaments',
                'message'       : 'another user has already selected this team in this tournament',
                },context_instance=RequestContext( request )
                )
    try:
        newM=TournamentMembers(
            user_id      = request.session['SESusername'],
            tournament  = Tournament.objects.get(tournament_name=tourny),
            )
    except:
        registered = functions.getJoinedTournaments(request.session['SESusername'])
        return render_to_response( "home.html", {
                'username'      : request.session['SESusername'],
                'reg'           : registered,
                'notreg'        : ' You are currently not registered for   any tournaments',
                'message'       : 'unable to successfully complete the process of joining you in the tournament, you are registered but this game will be simulated',
                },context_instance=RequestContext( request )
                )
    newM.save()    
    registered = functions.getJoinedTournaments(request.session['SESusername'])
    return render_to_response( "home.html", {
        'username'      : request.session['SESusername'],
        'reg'           : registered,
        'notreg'        : ' You are currently not registered for any tournaments',
        'message'       : 'You have successfully joined the tournament',
        },context_instance=RequestContext( request )
        )
    
def declareWinner(request, tourny, game):
    if 'SESusername' not in request.session:
        return render_to_response( "login.html", { }, context_instance=RequestContext( request ) )
    
    if request.method == 'GET':
        team = []
        user = []
        tournament = Tournament.objects.get(tournament_name = tourny)
        challenge = Game.objects.get(tournament_id=tournament.id, bracket_game=game)
        team.append(challenge.team_one)
        team.append(challenge.team_two)
        user.append(challenge.team_one_user)
        user.append(challenge.team_two_user)
        return render_to_response( "declareWinner.html", {
                'username'      : request.session['SESusername'],
                'team'          : team,
                'user'          : user,
                'message'       : tourny,
                'game'          : game,
                },context_instance=RequestContext( request )
                )
    if request.method == 'POST':
        tournament = Tournament.objects.get(tournament_name = tourny)
        challenge = Game.objects.get(tournament_id=tournament.id, bracket_game=game)
        
        if request.POST['team'] == challenge.team_one:
            challenge.winner = 0
            challenge.was_simulated = False
        elif request.POST['team'] == challenge.team_two:
            challenge.winner = 1
            challenge.was_simulated = False
        else:
            registered = functions.getJoinedTournaments(request.session['SESusername'])
            return render_to_response( "home.html", {
                'username'      : request.session['SESusername'],
                'reg'           : registered,
                'notreg'        : ' You are currently not registered for any tournaments',
                'message'       : 'we could not find your winning team in this matchup',
                },context_instance=RequestContext( request )
                )
        challenge.save()
        registered = functions.getJoinedTournaments(request.session['SESusername'])
        return render_to_response( "home.html", {
                'username'      : request.session['SESusername'],
                'reg'           : registered,
                'notreg'        : ' You are currently not registered for any tournaments',
                'message'       : 'your matchup was saved',
                },context_instance=RequestContext( request )
                )
def joinno(request):
    if 'SESusername' not in request.session:
        return render_to_response( "login.html", { }, context_instance=RequestContext( request ) )
    
    else:
        
        registered = functions.getJoinedTournaments(request.session['SESusername'])
        
        return render_to_response( "home.html", {
        'username'      : request.session['SESusername'],
        'reg'           : registered,
        'notreg'        : ' You are currently not registered for any tournaments',
        'message'       : 'You have not joined the tournament',
        },context_instance=RequestContext( request )
        )
    
    
    
    
    
    
    
    
    

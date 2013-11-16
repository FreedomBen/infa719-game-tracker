import random
from models import *
from modelHelper import *
#from django.http import HttpResponse, HttpResponseRedirect
#from django.shortcuts import render_to_response, get_object_or_404
#from django.template import RequestContext

def getBoolean(is_private):
    if is_private == 'True':
        return True
    return False
    
def getLetter():
    return chr(random.randint(ord('A'), ord('Z'))) + chr(random.randint(ord('A'), ord('Z')))
    
def createGames(newT, diff):
    
    
    rTeams = []
    for t in NFL_TEAMS:
        rTeams.append(t[0])
    random.shuffle(rTeams)
    
    team = 0
    
    for game in range(16):
        newG = Game(
            tournament      = newT,
            team_one        = rTeams[team],
            team_two        = rTeams[team+1],
            level           = diff,
            bracket_game    = game + 1,
        )
        newG.save()
        team += 2
        
        
def getGame(tid, num):
    obj = []
    try:
        tmp = Game.objects.get(tournament_id=tid, bracket_game=num)
    except:
        return [None,None,None,None]
    obj.append(teamAbbrToTeamName(tmp.team_one))
    obj.append(tmp.team_one_user)
    obj.append(teamAbbrToTeamName(tmp.team_two))
    obj.append(tmp.team_two_user)
    
    return obj

def getJoinedTournaments(usr):
    b = TournamentMembers.objects.filter(user_id=usr) 
    registered=[]
        
    for a in b:
        tourny = Tournament.objects.get(id=a.tournament_id)
        registered.append(tourny.tournament_name)
        
    return registered
    
def findTeamInGame(tourny,team):
    try:
        #find the tournament from the tournament table
        tObject = Tournament.objects.get(tournament_name=tourny)
    except:
        return 1
#    if Game.objects.filter(Q(tournament_id=tObject.id,team_one_user=request.session['SESusername']) | (tournament_id=tObject.id,team_two_user=request.session['SESusername'])) != None:
        #make sure each user is entered only 1 time in each tournament
        #return 2
    try:
            #check if user selected team is team 1
            myGame = Game.objects.get(tournament_id=tObject.id,team_one=team)
            
    except:
            try:
                #check if user selected team is team 2
                myGame = Game.objects.get(tournament_id=tObject.id,team_two=team)
            
            except:
                #user selected team could not be found *error*
                return 3
                
    return myGame

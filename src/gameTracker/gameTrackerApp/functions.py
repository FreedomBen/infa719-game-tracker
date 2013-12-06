import random
from models import *
from modelHelper import *
from django.db.models import Q
import datetime


def getBoolean(is_private):
    if is_private == 'True':
        return True
    return False
    
def getLetter():
    return chr(random.randint(ord('A'), ord('Z'))) + chr(random.randint(ord('A'), ord('Z')))
    
def createGames(newT, diff, rnd):
    
    
    rTeams = []
    
    
    if rnd == "All":  
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
            
    if rnd == "Conference":
        afc = []
        nfc = []
        for t in TEAMS_TO_CONFERENCES:
            if t[1] == 'AN' or t[1] == 'AS' or t[1] == 'AE' or t[1] == 'AW':
                afc.append(t[0])
            else:
                nfc.append(t[0])
        random.shuffle(nfc)
        random.shuffle(afc)
        team = 0
        for game in range(8):
            newG = Game(
                tournament      = newT,
                team_one        = afc[team],
                team_two        = afc[team+1],
                level           = diff,
                bracket_game    = game + 1,
            )
            newG.save()
            team += 2
        team = 0
        for game in range(8,16):
            newG = Game(
                tournament      = newT,
                team_one        = nfc[team],
                team_two        = nfc[team+1],
                level           = diff,
                bracket_game    = game + 1,
            )
            newG.save()
            team += 2
        
    if rnd == "Division":
        AW = []
        AE = []
        AS = []
        AN = []
        NW = []
        NE = []
        NS = []
        NN = []
        
        for t in TEAMS_TO_CONFERENCES:
            if t[1] == 'AW':
                AW.append(t[0])
            elif t[1] == 'AE':
                AE.append(t[0])
            elif t[1] == 'AS':
                AS.append(t[0])
            elif t[1] == 'AN':
                AN.append(t[0])
            elif t[1] == 'NW':
                NW.append(t[0])
            elif t[1] == 'NE':
                NE.append(t[0])
            elif t[1] == 'NS':
                NS.append(t[0])
            elif t[1] == 'NN':
                NN.append(t[0])
                
        random.shuffle(AW)
        random.shuffle(AE)
        random.shuffle(AS)
        random.shuffle(AN)
        random.shuffle(NW)
        random.shuffle(NE)
        random.shuffle(NS)
        random.shuffle(NN)
        team = 0
        for game in range(0,2):
            newG = Game(
                tournament      = newT,
                team_one        = AW[team],
                team_two        = AW[team+1],
                level           = diff,
                bracket_game    = game + 1,
            )
            newG.save()
            team += 2
        team = 0
        for game in range(2,4):
            newG = Game(
                tournament      = newT,
                team_one        = AE[team],
                team_two        = AE[team+1],
                level           = diff,
                bracket_game    = game + 1,
            )
            newG.save()
            team += 2
        team = 0
        for game in range(4,6):
            newG = Game(
                tournament      = newT,
                team_one        = AS[team],
                team_two        = AS[team+1],
                level           = diff,
                bracket_game    = game + 1,
            )
            newG.save()
            team += 2
        team = 0
        for game in range(6,8):
            newG = Game(
                tournament      = newT,
                team_one        = AN[team],
                team_two        = AN[team+1],
                level           = diff,
                bracket_game    = game + 1,
            )
            newG.save()
            team += 2
        team = 0
        for game in range(8,10):
            newG = Game(
                tournament      = newT,
                team_one        = NE[team],
                team_two        = NE[team+1],
                level           = diff,
                bracket_game    = game + 1,
            )
            newG.save()
            team += 2
        team = 0
        for game in range(10,12):
            newG = Game(
                tournament      = newT,
                team_one        = NW[team],
                team_two        = NW[team+1],
                level           = diff,
                bracket_game    = game + 1,
            )
            newG.save()
            team += 2
        team = 0
        for game in range(12,14):
            newG = Game(
                tournament      = newT,
                team_one        = NS[team],
                team_two        = NS[team+1],
                level           = diff,
                bracket_game    = game + 1,
            )
            newG.save()
            team += 2
        team = 0
        for game in range(14,16):
            newG = Game(
                tournament      = newT,
                team_one        = NN[team],
                team_two        = NN[team+1],
                level           = diff,
                bracket_game    = game + 1,
            )
            newG.save()
            team += 2

def convertDate(date, time):
    (H,M) = time.split(':')
    (year,month,day) = date.split('-')
    ret = year + '-' + month + '-' + day + ' ' + H + ':' + M
    #ret = datetime.datetime.strptime(ret,'%Y-%m-%d %H:%M')
    
    return ret

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

def getGameWinner(tid):
    obj = []
    try:
        tmp = Game.objects.get(tournament_id=tid, bracket_game=31)
    except:
        return [None,None]
    obj.append(teamAbbrToTeamName(tmp.winningTeam()))
    obj.append(tmp.winningUser)
    obj.append(teamAbbrToTeamName(tmp.team_two))
    obj.append(tmp.team_two_user)
    
    return obj
    
def getJoinedTournaments(usr):
    b = TournamentMembers.objects.filter(user_id=usr,tournament__current_round__lte=5) 
    registered=[]
    
    if not b:
        return None
    
    for a in b:
        tourny = Tournament.objects.get(id=a.tournament_id)
        registered.append(tourny.tournament_name)
        
    return registered
    
def getTournamentsPlayed(usr):
    count = TournamentMembers.objects.filter(user_id = usr)
    num = count.count()
    return num
    
def getTournamentsWon(usr):
    count = Game.objects.filter(team_one_user = usr, bracket_game = 31, winner = 0)
    num = count.count()
    
    count = Game.objects.filter(team_two_user = usr, bracket_game = 31, winner = 1)
    num += count.count()
    
    return num

def findTeamInGame(tourny,team,usr):
    try:
        #find the tournament from the tournament table
        tObject = Tournament.objects.get(tournament_name=tourny)
    except:
        return 1
    
    reg = TournamentMembers.objects.filter(tournament_id=tObject.id,user_id=usr)
    if reg:
        #make sure each user is entered only 1 time in each tournament
        return 2
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

def nextRound(tourny, start):
    if tourny.current_round == -1:
        tourny.current_round = 1
        tourny.save
        return
        
    tourny.tournament_open_datetime = start
    round = tourny.current_round = tourny.current_round + 1
    tourny.save()
    
    for game in Game.objects.filter(tournament_id = tourny.id):
        if game.winner == None:
            game.simulateGame()
            game.save()
    
    if round == 2:
        last = 1
        for n in range(17, 25):
            first = Game.objects.get(tournament_id=tourny.id, bracket_game=last)
            second = Game.objects.get(tournament_id=tourny.id, bracket_game=last + 1)
            newG = Game(
                tournament      = tourny,
                team_one        = first.winningTeam(),
                team_two        = second.winningTeam(),
                team_one_user   = first.winningUser(),
                team_two_user   = second.winningUser(),
                level           = tourny.difficulty_level,
                bracket_game    = n,
            )
            last += 2
            newG.save()
            
    if round == 3:
        last = 17
        for n in range(25, 29):
            first = Game.objects.get(tournament_id=tourny.id, bracket_game=last)
            second = Game.objects.get(tournament_id=tourny.id, bracket_game=last + 1)
            newG = Game(
                tournament      = tourny,
                team_one        = first.winningTeam(),
                team_two        = second.winningTeam(),
                team_one_user   = first.winningUser(),
                team_two_user   = second.winningUser(),
                level           = tourny.difficulty_level,
                bracket_game    = n,
            )
            last += 2
            newG.save()
            
    if round == 4:
        last =25
        for n in range(29, 31):
            first = Game.objects.get(tournament_id=tourny.id, bracket_game=last)
            second = Game.objects.get(tournament_id=tourny.id, bracket_game=last + 1)
            newG = Game(
                tournament      = tourny,
                team_one        = first.winningTeam(),
                team_two        = second.winningTeam(),
                team_one_user   = first.winningUser(),
                team_two_user   = second.winningUser(),
                level           = tourny.difficulty_level,
                bracket_game    = n,
            )
            last += 2
            newG.save()
            
    if round == 5:
        last = 29
        for n in range(31, 32):
            first = Game.objects.get(tournament_id=tourny.id, bracket_game=last)
            second = Game.objects.get(tournament_id=tourny.id, bracket_game=last + 1)
            newG = Game(
                tournament      = tourny,
                team_one        = first.winningTeam(),
                team_two        = second.winningTeam(),
                team_one_user   = first.winningUser(),
                team_two_user   = second.winningUser(),
                level           = tourny.difficulty_level,
                bracket_game    = n,
            )
            last += 2
            newG.save()
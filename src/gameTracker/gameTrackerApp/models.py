from django.db import models
import random

NFL_TEAMS = (
    ( 'ARI', 'Arizona Cardinals' ),
    ( 'ATL', 'Atlanta Falcons' ),
    ( 'BAL', 'Baltimore Ravens' ),
    ( 'BUF', 'Buffalo Bills' ),
    ( 'CAR', 'Carolina Panthers' ),
    ( 'CHI', 'Chicago Bears' ),
    ( 'CIN', 'Cincinnati Bengals' ),
    ( 'CLE', 'Cleveland Browns' ),
    ( 'DAL', 'Dallas Cowboys' ),
    ( 'DEN', 'Denver Broncos' ),
    ( 'DET', 'Detroit Lions' ),
    ( 'GB' , 'Green Bay Packers' ),
    ( 'HOU', 'Houston Texans' ),
    ( 'IND', 'Indianapolis Colts' ),
    ( 'JAX', 'Jacksonville Jaguars' ),
    ( 'KC' , 'Kansas City Chiefs' ),
    ( 'MIA', 'Miami Dolphins' ),
    ( 'MIN', 'Minnesota Vikings' ),
    ( 'NE' , 'New England Patriots' ),
    ( 'NO' , 'New Orleans Saints' ),
    ( 'NYG', 'New York Giants' ),
    ( 'NYJ', 'New York Jets' ),
    ( 'OAK', 'Oakland Raiders' ),
    ( 'PHI', 'Philadelphia Eagles' ),
    ( 'PIT', 'Pittsburgh Steelers' ),
    ( 'SD' , 'San Diego Chargers' ),
    ( 'SEA', 'Seattle Seahawks' ),
    ( 'SF' , 'San Francisco 49ers' ),
    ( 'STL', 'Saint Louis Rams' ),
    ( 'TB' , 'Tampa Bay Buccaneers' ),
    ( 'TEN', 'Tennessee Titans' ),
    ( 'WAS', 'Washington Redskins' ),
)

CONFERENCES = (
    ( 'AE', 'AFC East' ),
    ( 'AN', 'AFC North' ),
    ( 'AS', 'AFC South' ),
    ( 'AW', 'AFC West' ),
    ( 'NE', 'NFC East' ),
    ( 'NN', 'NFC North' ),
    ( 'NS', 'NFC South' ),
    ( 'NW', 'NFC West' ),
)

TEAMS_TO_CONFERENCES = (
    ( 'ARI', 'NW' ),
    ( 'ATL', 'NS' ),
    ( 'BAL', 'AN' ),
    ( 'BUF', 'AE' ),
    ( 'CAR', 'NS' ),
    ( 'CHI', 'NN' ),
    ( 'CIN', 'AN' ),
    ( 'CLE', 'AN' ),
    ( 'DAL', 'NE' ),
    ( 'DEN', 'AW' ),
    ( 'DET', 'NN' ),
    ( 'GB' , 'NN' ),
    ( 'HOU', 'NS' ),
    ( 'IND', 'NS' ),
    ( 'JAX', 'NS' ),
    ( 'KC' , 'AW' ),
    ( 'MIA', 'AE' ),
    ( 'MIN', 'NN' ),
    ( 'NE' , 'AE' ),
    ( 'NO' , 'NS' ),
    ( 'NYG', 'NE' ),
    ( 'NYJ', 'AE' ),
    ( 'OAK', 'AW' ),
    ( 'PHI', 'NE' ),
    ( 'PIT', 'AN' ),
    ( 'SD' , 'AW' ),
    ( 'SEA', 'NW' ),
    ( 'SF' , 'NW' ),
    ( 'STL', 'NW' ),
    ( 'TB' , 'NS' ),
    ( 'TEN', 'NS' ),
    ( 'WAS', 'NE' ),
)


class Conference( models.Model ):
    conference_name = models.CharField( max_length=2, choices=CONFERENCES )
    
    def __unicode__( self ):
        return self.conference_name


class NFLteam( models.Model ):
    team_name  = models.CharField( max_length=3, choices=NFL_TEAMS )

    def __unicode__( self ):
        return self.team_name


#----------------------------------------------------------------
# recieves an NFL team abbreviation and returns the corresponding
# NFLteam object from the DB
#----------------------------------------------------------------
def teamAbbrToNFLteam( teamAbbr ):
    """Looks through the NFLteam table and returns the NFLteam
       object that matches the abbreviation"""
    for nTeam in NFLteam.objects.all():
        if( nTeam.team_name == teamAbbr ):
            return nTeam

    # No luck, return None
    return None


#-----------------------------------------------------------------
# recieves a conference abbreviation and returns the corresponding
# Conference object from the DB
#-----------------------------------------------------------------
def confAbbrToConference( confAbbr ):
    """Looks through the Conference table and returns the NFLteam
       object that matches the abbreviation"""
    for conf in Conference.objects.all():
        if( conf.conference_name == confAbbr ):
            return conf

    # No luck, return None
    return None


#----------------------------------------------------------------
# recieves an NFL team name and returns the corresponding
# NFLteam object from the DB
#----------------------------------------------------------------
def teamNameToNFLteam( teamName ):
    """Looks through the NFLteam table and returns the NFLteam
       object that matches the name"""
    for nTeam in NFLteam.objects.all():
        if( nTeam.team_name == teamNameToAbbreviation( teamName ) ):
            return nTeam

    # No luck, return None
    return None


def teamNameToAbbreviation( teamName ):
    for team in NFL_TEAMS:
        if( team[1] == teamName ):
            return team[0]
    return None


def confNameToAbbreviation( confName ):
    for conf in CONFERENCES:
        if( conf[1] == confName ):
            return conf[0]
    return None

#-----------------------------------------------------------------
# recieves a conference name and returns the corresponding
# Conference object from the DB
#-----------------------------------------------------------------
def confNameToConference( confName ):
    """Looks through the Conference table and returns the NFLteam
       object that matches the abbreviation"""
    for conf in Conference.objects.all():
        if( conf.conference_name == confNameToAbbreviation( confName ) ):
            return conf

    # No luck, return None
    return None




#-----------------------------------------------------------
# recieves an NFL team abbreviation or an NFLteam object and 
# returns the Conference object 
#-----------------------------------------------------------
def teamToConference( nflTeam ):
    """Receives an NFLteam object or abbreviation and returns a Conference"""

    # Check to see if this is an NFLteam object or just a String.  
    # Objects have a team_name attribute
    if( hasattr( nflTeam, 'team_name' ) ):
        team = nflTeam.team_name   
    else:
        team = nflTeam

    for teamAbbr in TEAMS_TO_CONFERENCES:
        if( teamAbbr[0] == team ):
            for confAbbr in CONFERENCES:
                if( teamAbbr[1] == confAbbr[0] ):
                    return confAbbrToConference( confAbbr[0] )

    # Couldn't find it.  Return null
    return None


# recieved an NFL team abbreviation or an NFLteam object and 
# returns the Conference object 
def conferenceToTeams( conference ):
    """Receives Conference object or abbreviation and returns a list of NFLteam"""
    pass


class Tournament( models.Model ):
    DIFFICULTY_LEVELS = (
        ( 'RK', 'Rookie'     ),
        ( 'PR', 'Pro'        ),
        ( 'AP', 'All-Pro'    ),
        ( 'AM', 'All-Madden' ),
    )

    tournament_name       = models.CharField( max_length=25 )
    signup_open_datetime  = models.DateTimeField()
    signup_close_datetime = models.DateTimeField()
    round_open_datetime   = models.DateTimeField()
    round_close_datetime  = models.DateTimeField()
    quarter_length        = models.IntegerField() # in minutes
    difficulty_level      = models.CharField( max_length=2, choices=DIFFICULTY_LEVELS )

    def __unicode__( self ):
        return 'Tournament: ' + str( self.name )

class Game( models.Model ):
    GAME_LEVELS = (
        ( 'RO', 'Round One' ),
        ( 'DC', 'Division Champ' ),
        ( 'SF', 'Semi-Finals' ),
        ( 'CC', 'Conference Champ' ),
        ( 'CH', 'Championship' )
    )

    was_simulated = models.BooleanField()
    winner        = models.IntegerField()
    team_one      = models.ForeignKey( NFLteam, related_name='teamOneAsNFLteam' )
    team_two      = models.ForeignKey( NFLteam, related_name='teamTwoAsNFLteam' )
    tournament    = models.ForeignKey( Tournament )
    level         = models.CharField( max_length=2, choices=GAME_LEVELS )
    bracket_round = models.IntegerField()

    def simulateGame( self ):
        # randomly select a winner and set the flag
        winner = random.randint( 0,1 )
        self.was_simulated = true
        
    def winningTeam( self ):
        if( self.winner == 1 ): 
            return self.team_one
        else:
            return self.team_two
    
    def __unicode__( self ):
        return str( self.team_one ) + " v. " + str( self.team_two )


class Bracket():
    "Brackets are not part of the model themselves but are constructed from information in the model"
    ROUNDS = (
        ( 1, "ROUND_ONE" ),
        ( 2, "CONFERENCE_CHAMPION" )
        # TODO make match bracket outline
    )

    def games( roundNumber=1 ):
        "Return list of the games that make up requested round of the bracket. " \
                "If roundNumber is 0, all games are returned"
        pass



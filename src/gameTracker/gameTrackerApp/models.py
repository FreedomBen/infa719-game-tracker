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
    # conference = models.ForeignKey( 'Conference' )

    def __unicode__( self ):
        return self.team_name

#TODO
def teamToConference( nflTeam ):
    "Receives an NFL team abbreviation and returns a conference abbreviation"
    pass

#TODO
def conferenceToTeams( conference ):
    "Receives conference abbreviation and returns a tuple of team abbreviations"
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



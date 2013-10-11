from django.db import models
import random


#------------------------------------------------------------
# Security feature and code error catcher
# This class, when used a parent class for a model object,
# will prevent additional items from being saved to the table
#------------------------------------------------------------
class NonUpdateAbleModelMixin():
    """When used as a parent class, prevents a table from being inadvertently modified"""
    def save(self, *args, **kwargs):
        pass

 
# A sequence of NFL team abbreviations to team names
# This can be used to regenerate the tables in the DB if necessary
# and we aren't worried about corruption
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

# Conference abbreviations with full names
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

# team abbreviations mapped to respective conference
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


#---------------------------------------------------------------------------------------------
# Represent a conference in the NFL
# Exists as a table in the DB so that we can use a Conference as a foreign key in other tables
#---------------------------------------------------------------------------------------------
class Conference( models.Model ):
    """Represents a conference in the NFL"""
    conference_name = models.CharField( max_length=2, choices=CONFERENCES )
    
    def __unicode__( self ):
        return self.conference_name


#---------------------------------------------------------------------------------------------
# Represent an NFL team in the NFL
# Exists as a table in the DB so that we can use an NFL team as a foreign key in other tables
#---------------------------------------------------------------------------------------------
class NFLteam( models.Model ):
    """Represents an NFL team in the NFL"""
    team_name  = models.CharField( max_length=3, choices=NFL_TEAMS )

    def __unicode__( self ):
        return self.team_name


#---------------------------------------------------------------------------------------------
# Represents a Madden tournament
# All characteristics that we need to track are in this table
# The Bracket class uses this table and the Game table in the DB to generate itself
# Every Game belongs to a Tournament, tracked by foreign key
#---------------------------------------------------------------------------------------------
class Tournament( models.Model ):
    """Represents a Madden tournamennt"""
    DIFFICULTY_LEVELS = (
        ( 'RK', 'Rookie'     ),
        ( 'PR', 'Pro'        ),
        ( 'AP', 'All-Pro'    ),
        ( 'AM', 'All-Madden' ),
    )

    owner_id              = models.IntegerField()
    is_public             = models.BooleanField()
    tournament_name       = models.CharField( max_length=25 )
    signup_open_datetime  = models.DateTimeField()
    signup_close_datetime = models.DateTimeField()
    round_open_datetime   = models.DateTimeField()
    round_close_datetime  = models.DateTimeField()
    quarter_length        = models.IntegerField() # in minutes
    difficulty_level      = models.CharField( max_length=2, choices=DIFFICULTY_LEVELS )

    def __unicode__( self ):
        return 'Tournament: ' + str( self.name )


#---------------------------------------------------------------------------------------------
# Keeps track of which users have been authorized to view a tournament by the tournament owner
#---------------------------------------------------------------------------------------------
class TournamentMembers( models.Model ):
    user_id = models.IntegerField()
    tournament = models.ForeignKey( Tournament )


#---------------------------------------------------------------------------------------------
# Represent a Madden game
# All characteristics that we need to track are in this table
# The Bracket class uses this table and the Tournament table in the DB to generate itself
# Every Game belongs to a Tournament, tracked by foreign key
#---------------------------------------------------------------------------------------------
class Game( models.Model ):
    """Represents a Madden game that has been or will be played"""
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



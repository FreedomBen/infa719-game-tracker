from django.db import models
import random

NFL_TEAMS = (
    ( 'ARI' 'Arizona Cardinals' )
    ( 'ATL' 'Atlanta Falcons' )
    ( 'BAL' 'Baltimore Ravens' )
    ( 'BUF' 'Buffalo Bills' )
    ( 'CAR' 'Carolina Panthers' )
    ( 'CHI' 'Chicago Bears' )
    ( 'CIN' 'Cincinnati Bengals' )
    ( 'CLE' 'Cleveland Browns' )
    ( 'DAL' 'Dallas Cowboys' )
    ( 'DEN' 'Denver Broncos' )
    ( 'DET' 'Detroit Lions' )
    ( 'GB'  'Green Bay Packers' )
    ( 'HOU' 'Houston Texans' )
    ( 'IND' 'Indianapolis Colts' )
    ( 'JAX' 'Jacksonville Jaguars' )
    ( 'KC'  'Kansas City Chiefs' )
    ( 'MIA' 'Miami Dolphins' )
    ( 'MIN' 'Minnesota Vikings' )
    ( 'NE'  'New England Patriots' )
    ( 'NO'  'New Orleans Saints' )
    ( 'NYG' 'New York Giants' )
    ( 'NYJ' 'New York Jets' )
    ( 'OAK' 'Oakland Raiders' )
    ( 'PHI' 'Philadelphia Eagles' )
    ( 'PIT' 'Pittsburgh Steelers' )
    ( 'SD'  'San Diego Chargers' )
    ( 'SEA' 'Seattle Seahawks' )
    ( 'SF'  'San Francisco 49ers' )
    ( 'STL' 'Saint Louis Rams' )
    ( 'TB'  'Tampa Bay Buccaneers' )
    ( 'TEN' 'Tennessee Titans' )
    ( 'WAS' 'Washington Redskins' )
)

CONFERENCES = (
    ( 'AE' 'AFC East' )
    ( 'AN' 'AFC North' )
    ( 'AS' 'AFC South' )
    ( 'AW' 'AFC West' )
    ( 'NE' 'NFC East' )
    ( 'NN' 'NFC North' )
    ( 'NS' 'NFC South' )
    ( 'NW' 'NFC West' )
)

TEAMS_TO_CONFERENCES = (
    ( 'ARI' 'NW' )
    ( 'ATL' 'NS' )
    ( 'BAL' 'AN' )
    ( 'BUF' 'AE' )
    ( 'CAR' 'NS' )
    ( 'CHI' 'NN' )
    ( 'CIN' 'AN' )
    ( 'CLE' 'AN' )
    ( 'DAL' 'NE' )
    ( 'DEN' 'AW' )
    ( 'DET' 'NN' )
    ( 'GB'  'NN' )
    ( 'HOU' 'NS' )
    ( 'IND' 'NS' )
    ( 'JAX' 'NS' )
    ( 'KC'  'AW' )
    ( 'MIA' 'AE' )
    ( 'MIN' 'NN' )
    ( 'NE'  'AE' )
    ( 'NO'  'NS' )
    ( 'NYG' 'NE' )
    ( 'NYJ' 'AE' )
    ( 'OAK' 'AW' )
    ( 'PHI' 'NE' )
    ( 'PIT' 'AN' )
    ( 'SD'  'AW' )
    ( 'SEA' 'NW' )
    ( 'SF'  'NW' )
    ( 'STL' 'NW' )
    ( 'TB'  'NS' )
    ( 'TEN' 'NS' )
    ( 'WAS' 'NE' )
)


#TODO
def teamToConference( nflTeam ):
    "Receives an NFL team abbreviation and returns a conference abbreviation"
    pass

#TODO
def conferenceToTeams( conference ):
    "Receives conference abbreviation and returns a tuple of team abbreviations"
    pass


class Tournament( models.Model ):
    DIFFICULTY_LEVELS (
        ( 'RK' 'Rookie'     )
        ( 'PR' 'Pro'        )
        ( 'AP' 'All-Pro'    )
        ( 'AM' 'All-Madden' )
    )

    signup_open_datetime  = models.DateTimeField()
    signup_close_datetime = models.DateTimeField()
    round_open_datetime   = models.DateTimeField()
    round_close_datetime  = models.DateTimeField()
    quarter_length        = models.IntegerField() # in minutes
    difficulty_level      = models.CharFiel( max_length=2, choices=DIFFICULTY_LEVELS )
    games                 = models.ManyToManyField( Game )


class Game( models.Model ):
    was_simulated = models.BooleanField()
    winner        = models.IntegerField()
    team_one      = models.ForeignKey( NFLteam )
    team_two      = models.ForeignKey( NFLteam )
    tournament    = models.ForeignKey( Tournament )

    def simulateGame( self ):
        # randomly select a winner and set the flag
        winner = random.randint( 0,1 )
        self.was_simulated = true
        
    def winningTeam( self ):
        if( self.winner == 1 ): 
            return self.team_one
        else:
            return self.team_two
    

class NFLteam( models.Model ):
    team_name  = models.CharField( max_length=3, choices=NFL_TEAMS )
    conference = models.CharField( max_length=2, choices=CONFERENCES )


class Bracket( models.Model ):
    # 4 regions
    pass



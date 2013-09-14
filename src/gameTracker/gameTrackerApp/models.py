from django.db import models

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
    quarter_length = # mins
    difficulty_level = 

    # Has games
    # Property - Quarter length in minutes
    # Difficulty Level
    # Defined Dates for sign-up (date/time for open & close of sign-up)
    # Defined Dates for each round of play (date/time for round open & round close)
    # Since un-played games have random winner picked, store whether was simulated or not

class Game( models.Model ):
    was_simulated = models.BooleanField()
    winner = 
    team_one = NFLteam
    team_two = NFLteam
    # Belong to a tournament
    # Has two teams

    def simulateGame( self ):
        # randomly select a winner and set the flag
        self.was_simulated = true
        pass
        
    

class NFLteam( models.Model ):
    team = models.CharField( max_length=3, choices=NFL_TEAMS )
    conference = models.CharField

class Bracket( models.Model ):
    # 4 regions



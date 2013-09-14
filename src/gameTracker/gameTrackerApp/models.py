from django.db import models

class Tournament( models.Model ):
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

class Bracket( models.Model ):
    # 4 regions



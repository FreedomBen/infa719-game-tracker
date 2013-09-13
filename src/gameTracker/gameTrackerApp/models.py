from django.db import models

class Tournament( models.Model ):
    # Has games
    # Property - Quarter length in minutes
    # Difficulty Level
    # Defined Dates for sign-up (date/time for open & close of sign-up)
    # Defined Dates for each round of play (date/time for round open & round close)
    # Since un-played games have random winner picked, store whether was simulated or not

class Game( models.Model ):
    # Belong to a tournament
    # Has two teams
    

class NFLteam( models.Model ):


class Bracket( models.Model ):
    # 4 regions



from gameTrackerApp.models import *


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


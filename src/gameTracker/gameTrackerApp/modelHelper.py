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


#----------------------------------------------------------------------
# recieves an NFL team name and returns the corresponding abbreviation
#----------------------------------------------------------------------
def teamNameToAbbreviation( teamName ):
    for team in NFL_TEAMS:
        if( team[1] == teamName ):
            return team[0]
    return None


#----------------------------------------------------------------------
# recieves a Conference name and returns the corresponding abbreviation
#----------------------------------------------------------------------
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


#-----------------------------------------------------------
# recieves a Conference object or abbreviation and 
# returns the teams that belong
#-----------------------------------------------------------
def conferenceToTeams( conference ):
    """Receives Conference object or abbreviation and returns a list of NFLteam"""

    # Check to see if this is a Conference object or just a String.  
    # Objects have a conference_name attribute
    if( hasattr( conference, 'conference_name' ) ):
        conf = conference.team_name   
    else:
        conf = conference

    retval = []
    for ttc in TEAMS_TO_CONFERENCES:
        if( ttc[1] == conf ):
            retval.append( teamAbbrToNFLteam( ttc[0] ) )

    # return results
    return retval
#-----------------------------------------------------------
# recieves a difficulty_level abbreviation and 
# returns that difficulty_level name
#-----------------------------------------------------------
def difAbbrToName(level):
    for dif in Tournament.DIFFICULTY_LEVELS:
        if( dif[0] == level ):
            return dif[1]
    return None
    
def teamAbbrToTeamName(teamAbbr):
    for team in NFL_TEAMS:
        if( team[0] == teamAbbr ):
            return team[1]
    return None
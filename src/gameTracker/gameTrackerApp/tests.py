"""
These tests should pass when you run "manage.py test".
"""

from django.test import TestCase
from gameTrackerApp.models import *
from gameTrackerApp.modelHelper import *


class ModelHelperTest( TestCase ):
    def setUp( self ):
        l = []
        for i in NFL_TEAMS:
            l.append( NFLteam( team_name=i[0] ) )
        for i in l:
            i.save()
        l=[]
        for i in CONFERENCES:
            l.append( Conference( conference_name=i[0] ) )
        for i in l:
            i.save()

    def test( self ):
        self.assertEqual( teamAbbrToNFLteam( "ARI" ).team_name, "ARI" )
        for team in NFL_TEAMS:
            self.assertEqual( teamAbbrToNFLteam( team[0] ).team_name, team[0] )

        self.assertEqual( confAbbrToConference( "NN" ).conference_name, "NN" )
        for conf in CONFERENCES:
            self.assertEqual( confAbbrToConference( conf[0] ).conference_name, conf[0] )

        self.assertEqual( teamNameToNFLteam( "Baltimore Ravens" ).team_name, "BAL" )
        for team in NFL_TEAMS:
            self.assertEqual( teamNameToNFLteam( team[1] ).team_name, team[0] )

        self.assertEqual( teamNameToAbbreviation( "Baltimore Ravens" ), "BAL" )
        for team in NFL_TEAMS:
            self.assertEqual( teamNameToAbbreviation( team[1] ), team[0] )

        self.assertEqual( confNameToAbbreviation( "NFC North" ), "NN" )
        for conf in CONFERENCES:
            self.assertEqual( confNameToAbbreviation( conf[1] ), conf[0] )

        self.assertEqual( confNameToConference( "NFC North" ).conference_name, "NN" )
        for conf in CONFERENCES:
            self.assertEqual( confNameToConference( conf[1] ).conference_name, conf[0] )

        self.assertEqual( teamToConference( "BAL" ).conference_name, "AN" )
        self.assertEqual( teamToConference( "DET" ).conference_name, "NN" )
        self.assertEqual( teamToConference( "HOU" ).conference_name, "NS" )
        self.assertEqual( teamToConference( "OAK" ).conference_name, "AW" )
        self.assertEqual( teamToConference( "SEA" ).conference_name, "NW" )
        self.assertEqual( teamToConference( "MIA" ).conference_name, "AE" )

        
        self.assertIn( teamAbbrToNFLteam( "BAL" ), conferenceToTeams( "AN" ) )
        self.assertIn( teamAbbrToNFLteam( "CIN" ), conferenceToTeams( "AN" ) )
        self.assertIn( teamAbbrToNFLteam( "CLE" ), conferenceToTeams( "AN" ) )
        self.assertIn( teamAbbrToNFLteam( "PIT" ), conferenceToTeams( "AN" ) )

        self.assertIn( teamAbbrToNFLteam( "SEA" ), conferenceToTeams( "NW" ) )
        self.assertIn( teamAbbrToNFLteam( "SF"  ), conferenceToTeams( "NW" ) )
        self.assertIn( teamAbbrToNFLteam( "STL" ), conferenceToTeams( "NW" ) )
        self.assertIn( teamAbbrToNFLteam( "ARI" ), conferenceToTeams( "NW" ) )


    def test_2( self ):
        # Just a placeholder right now
        pass

from gameTrackerApp.models import *


class Bracket():
    "Brackets are not part of the model themselves but are constructed from information in the model"
    ROUNDS = (
        ( 1, "ROUND_ONE" ),
        ( 2, "CONFERENCE_CHAMPION" )
        # TODO make match bracket outline
    )

    def games( self, roundNumber=1 ):
        "Return list of the games that make up requested round of the bracket. " \
                "If roundNumber is 0, all games are returned"
        pass


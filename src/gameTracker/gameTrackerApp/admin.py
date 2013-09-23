from gameTrackerApp.models import Conference
from gameTrackerApp.models import NFLteam
from gameTrackerApp.models import Tournament
from gameTrackerApp.models import Game

from django.contrib import admin

admin.site.register( Conference )
admin.site.register( NFLteam )
admin.site.register( Tournament )
admin.site.register( Game )


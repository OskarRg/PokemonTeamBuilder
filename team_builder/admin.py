from django.contrib import admin
from .models import Pokemon, Move, Team, TeamPokemon

admin.site.register(Pokemon)
admin.site.register(Move)
admin.site.register(Team)
admin.site.register(TeamPokemon)
from django.contrib import admin
from .models import Pokemon, Move, Team, TeamPokemon, FavoriteTeam, FavoritePokemon, Comment, BuiltInTeamPokemon, BuiltInTeam, Type

admin.site.register(Pokemon)
admin.site.register(Type)
admin.site.register(Move)
admin.site.register(Team)
admin.site.register(TeamPokemon)
admin.site.register(FavoritePokemon)
admin.site.register(FavoriteTeam)
admin.site.register(BuiltInTeamPokemon)
admin.site.register(BuiltInTeam)
admin.site.register(Comment)
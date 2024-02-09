from django.contrib import admin
from .models import PokemonComment, TeamComment, Vote

admin.site.register(PokemonComment)
admin.site.register(TeamComment)
admin.site.register(Vote)


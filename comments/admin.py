from django.contrib import admin
from .models import PokemonComment, TeamComment, Upvote, Downvote

admin.site.register(PokemonComment)
admin.site.register(TeamComment)
admin.site.register(Upvote)
admin.site.register(Downvote)


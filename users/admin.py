from django.contrib import admin
from .models import UserProfile, FavoritePokemon, FavoriteTeam

admin.site.register(UserProfile)
admin.site.register(FavoritePokemon)
admin.site.register(FavoriteTeam)

from django.urls import path
from .views import TeamDetail, TeamPokemonDetail, MoveList, PokemonList, TeamListCreate, PokemonDetailView

urlpatterns = [
    path('pokemon-details/<int:pk>/', PokemonDetailView.as_view(), name='pokemon-detail'),
    path('create-new-team/', TeamListCreate.as_view(), name='team-create'),
    path('team-details/<int:team_id>/', TeamDetail.as_view(), name='team-details'),
    path('team-pokemon/<int:team_id>/<int:slot>/', TeamPokemonDetail.as_view(), name='team-pokemon-detail'),
    path('moves-list/', MoveList.as_view(), name='moves-list'),
    path('pokemons-list/', PokemonList.as_view(), name='pokemon-list'),
]

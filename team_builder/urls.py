from django.urls import path
from .views import TeamDetail, TeamPokemonDetail, MoveList, PokemonList, TeamListCreate, PokemonDetailView, \
    TeamPokemonListCreate

urlpatterns = [

    path('moves-list/', MoveList.as_view(), name='moves-list'),
    path('pokemons-list/', PokemonList.as_view(), name='pokemon-list'),
    path('pokemon-details/<int:pk>/', PokemonDetailView.as_view(), name='pokemon-detail'),
    path('team-create/', TeamListCreate.as_view(), name='team-create'),
    path('team-details/<int:pk>/', TeamDetail.as_view(), name='team-details'),
    path('teampokemons-list/<int:team_id>/', TeamPokemonListCreate.as_view(), name='teampokemon-list-create'),
    path('teampokemon-details/<int:pk>/', TeamPokemonDetail.as_view(), name='team-pokemon-detail'),
]

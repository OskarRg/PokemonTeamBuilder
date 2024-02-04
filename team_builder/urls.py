from django.urls import path
from .views import TeamDetailAPIView, TeamListCreateAPIView, TeamPokemonCreateAPIView, TeamPokemonDeleteAPIView, \
    TeamPokemonUpdateAPIView, UserTeamListAPIView

urlpatterns = [
    path('create-new-team/', TeamListCreateAPIView.as_view(), name='team-create'),
    path('team-details/<int:team_id>/', TeamDetailAPIView.as_view(), name='team-details'),
    path('create-new-team-pokemon/<int:team_id>/', TeamPokemonCreateAPIView.as_view(), name='create_new_team_pokemon'),
    path('delete-team-pokemon/<int:team_id>/<int:slot>/', TeamPokemonDeleteAPIView.as_view(), name='delete-team-pokemon'),
    path('update-team-pokemon/<int:team_id>/<int:slot>/', TeamPokemonUpdateAPIView.as_view(), name='update-team-pokemon'),
    path('user-teams-list/', UserTeamListAPIView.as_view(), name='user-teams-list'),
]

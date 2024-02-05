from django.urls import path
from .views import TeamDetail, TeamCreate, UserTeamListAPIView, TeamPokemonDetail, MoveList

urlpatterns = [
    path('create-new-team/', TeamCreate.as_view(), name='team-create'),
    path('team-details/<int:team_id>/', TeamDetail.as_view(), name='team-details'),
    path('detail-team-pokemon/<int:team_id>/<int:slot>/', TeamPokemonDetail.as_view(), name='team-pokemon-detail'),
    path('user-teams-list/', UserTeamListAPIView.as_view(), name='user-teams-list'),
    path('moves-list/', MoveList.as_view(), name='moves-list'),
]

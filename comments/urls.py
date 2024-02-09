from django.urls import path
from .views import TeamCommentListCreate, PokemonCommentListCreate, TeamCommentDetail, PokemonCommentDetail


urlpatterns = [
    path('team-comments/<int:pk>/', TeamCommentListCreate.as_view(), name='team_comment_list_create'),
    path('team-comment-details/<int:pk>/', TeamCommentDetail.as_view(), name='team_comment_detail'),
    path('pokemon-comments/', PokemonCommentListCreate.as_view(), name='pokemon_comment_list_create'),
    path('pokemon-comments/<int:pk>/', PokemonCommentDetail.as_view(), name='pokemon_comment_detail'),
]

from django.urls import path
from .views import TeamCommentListCreate, PokemonCommentListCreate, TeamCommentDetail, PokemonCommentDetail, CreateVote, \
    DeleteVote

urlpatterns = [
    path('team-comments/<int:pk>/', TeamCommentListCreate.as_view(), name='team_comment_list_create'),
    path('team-comment-details/<int:pk>/', TeamCommentDetail.as_view(), name='team_comment_detail'),
    path('pokemon-comments/', PokemonCommentListCreate.as_view(), name='pokemon_comment_list_create'),
    path('pokemon-comments/<int:pk>/', PokemonCommentDetail.as_view(), name='pokemon_comment_detail'),
    path('comments/<str:comment_type>/<int:pk>/unvote/', DeleteVote.as_view(), name='delete_vote'),
    path('comments/<str:comment_type>/<int:pk>/<str:vote_type>/', CreateVote.as_view(), name='create_vote'),
]

from django.urls import path
from .views import TeamCommentListCreate, TeamCommentDetail, UpvoteCreateAPIView, DownvoteCreateAPIView, \
    PokemonCommentListCreate, \
    PokemonCommentDetail, UpvoteDelete, DownvoteDelete

urlpatterns = [
    path('team-comment/<int:team_id>/', TeamCommentListCreate.as_view(), name='team-comment-list-create'),
    path('team-comment/<int:team_id>/<int:pk>/', TeamCommentDetail.as_view(), name='team-comment-detail'),
    path('pokemon-comment/<int:pokemon_id>/', PokemonCommentListCreate.as_view(), name='pokemon-comment-list-create'),
    path('pokemon-comment/<int:pokemon_id>/<int:pk>/', PokemonCommentDetail.as_view(), name='pokemon-comment-detail'),
    path('team-comment/<int:team_id>/<int:pk>/upvote/', UpvoteCreateAPIView.as_view(),         name='comment-upvote'),
    path('team-comment/<int:team_id>/<int:pk>/downvote/', DownvoteCreateAPIView.as_view(),         name='comment-downvote'),
    path('pokemon-comment/<int:pokemon_id>/<int:pk>/upvote/', UpvoteCreateAPIView.as_view(),         name='comment-upvote'),
    path('pokemon-comment/<int:pokemon_id>/<int:pk>/downvote/', DownvoteCreateAPIView.as_view(),         name='comment-downvote'),
    path('upvote/<int:pk>/', UpvoteDelete.as_view(), name='upvote-delete'),
    path('upvote/<int:pk>/', DownvoteDelete.as_view(), name='downvote-delete'),
]

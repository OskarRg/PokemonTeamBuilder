from rest_framework import generics, permissions, status

from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from comments.models import TeamComment, PokemonComment, Upvote, Downvote
from .filters import TeamCommentFilter, PokemonCommentFilter
from team_builder.models import Team, Pokemon
from .serializers import TeamCommentSerializer, PokemonCommentSerializer, UpvoteSerializer, \
    DownvoteSerializer, TeamCommentDetailSerializer, PokemonCommentDetailSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.user == request.user


class IsAuthenticatedToCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        return True


class TeamCommentListCreate(generics.ListCreateAPIView):
    serializer_class = TeamCommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeamCommentFilter
    permission_classes = [IsAuthenticatedToCreate]

    def get_queryset(self):
        team_id = self.kwargs.get('team_id')
        queryset = TeamComment.objects.filter(team_id=team_id)

        order_by = self.request.query_params.get('ordering')

        if order_by == 'upvotes':
            queryset = queryset.annotate(upvotes_count=Count('upvotes')).order_by('-upvotes_count')
        elif order_by == 'downvotes':
            queryset = queryset.annotate(downvotes_count=Count('downvotes')).order_by('-downvotes_count')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def perform_create(self, serializer):
        team_id = self.kwargs.get('team_id')
        team = generics.get_object_or_404(Team, pk=team_id)
        serializer.save(user=self.request.user, team=team)


class TeamCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeamComment.objects.all()
    serializer_class = TeamCommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class PokemonCommentListCreate(generics.ListCreateAPIView):
    serializer_class = PokemonCommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PokemonCommentFilter
    permission_classes = [IsAuthenticatedToCreate]

    def get_queryset(self):
        pokemon_id = self.kwargs.get('pokemon_id')
        queryset = PokemonComment.objects.filter(pokemon_id=pokemon_id)

        order_by = self.request.query_params.get('ordering')

        if order_by == 'upvotes':
            queryset = queryset.annotate(upvotes_count=Count('upvotes')).order_by('-upvotes_count')
        elif order_by == 'downvotes':
            queryset = queryset.annotate(downvotes_count=Count('downvotes')).order_by('-downvotes_count')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def perform_create(self, serializer):
        pokemon_id = self.kwargs.get('pokemon_id')
        pokemon = generics.get_object_or_404(Pokemon, pk=pokemon_id)
        serializer.save(user=self.request.user, pokemon=pokemon)


class PokemonCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PokemonComment.objects.all()
    serializer_class = PokemonCommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class UpvoteCreateAPIView(generics.CreateAPIView):
    queryset = Upvote.objects.all()
    serializer_class = UpvoteSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        pk = self.kwargs.get('pk')

        if 'team_id' in self.kwargs:
            team_comment = generics.get_object_or_404(TeamComment, pk=pk)
            existing_upvote = Upvote.objects.filter(user=user, team_comment=team_comment).exists()
            existing_downvote = Downvote.objects.filter(user=user, team_comment=team_comment).exists()
            if existing_upvote or existing_downvote:
                return Response({'message': 'You have already upvoted this team comment.'}, status=status.HTTP_200_OK)

            return Response({'message': 'You have not upvoted this team comment.'},
                            status=status.HTTP_200_OK)
        elif 'pokemon_id' in self.kwargs:
            pokemon_comment = generics.get_object_or_404(PokemonComment, pk=pk)
            existing_upvote = Upvote.objects.filter(user=user, pokemon_comment=pokemon_comment).exists()
            existing_downvote = Downvote.objects.filter(user=user, pokemon_comment=pokemon_comment).exists()
            if existing_upvote or existing_downvote:
                return Response({'message': 'You have already upvoted this pokemon comment.'},
                                status=status.HTTP_200_OK)
            serializer = self.serializer_class()
            return Response({'message': 'You have not upvoted this pokemon comment.'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid request. Please provide team_comment_id or pokemon_comment_id.'},
                            status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        user = self.request.user
        pk = self.kwargs.get('pk')

        if 'team_id' in self.kwargs:
            team_comment = generics.get_object_or_404(TeamComment, pk=pk)
            existing_upvote = Upvote.objects.filter(user=user, team_comment=team_comment).exists()
            existing_downvote = Downvote.objects.filter(user=user, team_comment=team_comment).exists()
            if existing_upvote or existing_downvote:
                return Response({'message': 'You have already upvoted this team comment.'}, status=status.HTTP_200_OK)
            serializer.save(user=user, team_comment=team_comment)
        elif 'pokemon_id' in self.kwargs:
            pokemon_comment = generics.get_object_or_404(PokemonComment, pk=pk)
            existing_upvote = Upvote.objects.filter(user=user, pokemon_comment=pokemon_comment).exists()
            existing_downvote = Downvote.objects.filter(user=user, pokemon_comment=pokemon_comment).exists()
            if existing_upvote or existing_downvote:
                return Response({'message': 'You have already upvoted this pokemon comment.'},
                                status=status.HTTP_200_OK)
            serializer.save(user=user, pokemon_comment=pokemon_comment)
        else:
            return Response({'message': 'Invalid request. Please provide team_comment_id or pokemon_comment_id.'},
                            status=status.HTTP_400_BAD_REQUEST)


class DownvoteCreateAPIView(generics.CreateAPIView):
    queryset = Downvote.objects.all()
    serializer_class = DownvoteSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        pk = self.kwargs.get('pk')

        if 'team_id' in self.kwargs:
            team_comment = generics.get_object_or_404(TeamComment, pk=pk)
            existing_upvote = Upvote.objects.filter(user=user, team_comment=team_comment).exists()
            existing_downvote = Downvote.objects.filter(user=user, team_comment=team_comment).exists()
            if existing_upvote or existing_downvote:
                return Response({'message': 'You have already upvoted this team comment.'}, status=status.HTTP_200_OK)

            return Response({'message': 'You have not upvoted this team comment.'},
                            status=status.HTTP_200_OK)
        elif 'pokemon_id' in self.kwargs:
            pokemon_comment = generics.get_object_or_404(PokemonComment, pk=pk)
            existing_upvote = Upvote.objects.filter(user=user, pokemon_comment=pokemon_comment).exists()
            existing_downvote = Downvote.objects.filter(user=user, pokemon_comment=pokemon_comment).exists()
            if existing_upvote or existing_downvote:
                return Response({'message': 'You have already upvoted this pokemon comment.'},
                                status=status.HTTP_200_OK)
            serializer = self.serializer_class()
            return Response({'message': 'You have not upvoted this pokemon comment.'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid request. Please provide team_comment_id or pokemon_comment_id.'},
                            status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        user = self.request.user
        pk = self.kwargs.get('pk')

        if 'team_id' in self.kwargs:
            team_comment = generics.get_object_or_404(TeamComment, pk=pk)
            existing_upvote = Upvote.objects.filter(user=user, team_comment=team_comment).exists()
            existing_downvote = Downvote.objects.filter(user=user, team_comment=team_comment).exists()
            if existing_upvote or existing_downvote:
                return Response({'message': 'You have already downvoted this team comment.'}, status=status.HTTP_200_OK)
            serializer.save(user=user, team_comment=team_comment)
        elif 'pokemon_id' in self.kwargs:
            pokemon_comment = generics.get_object_or_404(PokemonComment, pk=pk)
            existing_upvote = Upvote.objects.filter(user=user, pokemon_comment=pokemon_comment).exists()
            existing_downvote = Downvote.objects.filter(user=user, pokemon_comment=pokemon_comment).exists()
            if existing_upvote or existing_downvote:
                return Response({'message': 'You have already downvoted this pokemon comment.'},
                                status=status.HTTP_200_OK)
            serializer.save(user=user, pokemon_comment=pokemon_comment)
        else:
            return Response(
                {'message': 'Invalid request. Please provide team_comment_id or pokemon_comment_id (from url).'},
                status=status.HTTP_400_BAD_REQUEST)

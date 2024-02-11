import django_filters
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q, OuterRef, Subquery
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import TeamComment, PokemonComment, Vote
from .serializers import TeamCommentSerializer, PokemonCommentSerializer, VoteSerializer
from .filters import TeamCommentFilter, PokemonCommentFilter
from django.contrib.auth import get_user_model


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


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CommentListCreate(generics.ListCreateAPIView):
    serializer_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = None
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedToCreate]

    def get_queryset(self):
        team_id = self.kwargs['pk']
        queryset = self.serializer_class.Meta.model.objects.filter(team_id=team_id)

        order_by = self.request.query_params.get('ordering')

        if order_by == 'upvotes':
            queryset = queryset.annotate(upvotes_count=Count('votes', filter=Q(votes__is_upvote=True))).order_by(
                '-upvotes_count')
        elif order_by == 'downvotes':
            queryset = queryset.annotate(downvotes_count=Count('votes', filter=Q(votes__is_upvote=False))).order_by(
                '-downvotes_count')
        elif order_by == 'date':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TeamCommentListCreate(CommentListCreate):
    serializer_class = TeamCommentSerializer
    filterset_class = TeamCommentFilter


class PokemonCommentListCreate(CommentListCreate):
    serializer_class = PokemonCommentSerializer
    filterset_class = PokemonCommentFilter


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = None
    serializer_class = None
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


class TeamCommentDetail(CommentDetail):
    queryset = TeamComment.objects.all()
    serializer_class = TeamCommentSerializer


class PokemonCommentDetail(CommentDetail):
    queryset = PokemonComment.objects.all()
    serializer_class = PokemonCommentSerializer


class CreateVote(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticatedToCreate]

    def post(self, request, *args, **kwargs):
        comment_type = self.kwargs.get('comment_type')
        comment_id = self.kwargs.get('pk')
        vote_type = self.kwargs.get('vote_type')

        if vote_type == 'upvote':
            is_upvote = True
        elif vote_type == 'downvote':
            is_upvote = False
        else:
            return Response({'detail': 'Invalid vote type.'}, status=status.HTTP_400_BAD_REQUEST)

        if comment_type == 'team':
            comment_model = TeamComment
        elif comment_type == 'pokemon':
            comment_model = PokemonComment
        else:
            return Response({'comment_type': ['Invalid comment type.']}, status=status.HTTP_400_BAD_REQUEST)

        comment = generics.get_object_or_404(comment_model, pk=comment_id)
        user = request.user

        existing_vote = Vote.objects.filter(user=user, content_type_id=ContentType.objects.get_for_model(comment).id,
                                            object_id=comment_id).first()
        if existing_vote:
            return Response({'detail': 'You have already voted for this comment.'}, status=status.HTTP_400_BAD_REQUEST)

        Vote.objects.create(user=user, content_type=ContentType.objects.get_for_model(comment), object_id=comment_id,
                            is_upvote=is_upvote)
        return Response({'detail': 'Vote added successfully.'}, status=status.HTTP_201_CREATED)


class DeleteVote(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        comment_type = self.kwargs.get('comment_type')
        comment_id = self.kwargs.get('pk')

        if comment_type == 'team':
            comment_model = TeamComment
        elif comment_type == 'pokemon':
            comment_model = PokemonComment
        else:
            return Response({'comment_type': ['Invalid comment type.']}, status=status.HTTP_400_BAD_REQUEST)

        comment = generics.get_object_or_404(comment_model, pk=comment_id)
        user = request.user

        existing_vote = Vote.objects.filter(user=user, content_type_id=ContentType.objects.get_for_model(comment).id,
                                            object_id=comment_id).first()
        if not existing_vote:
            return Response({'detail': 'You have not voted for this comment.'}, status=status.HTTP_400_BAD_REQUEST)

        existing_vote.delete()
        return Response({'detail': 'Vote deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

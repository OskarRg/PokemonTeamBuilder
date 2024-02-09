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
        # It could work, but first I need to figure out upvotes & downvotes logic
        '''
        order_by = self.request.query_params.get('ordering')

        if order_by == 'upvotes':
            queryset = queryset.annotate(upvotes_count=Count('votes', filter=Q(votes__is_upvote=True))).order_by('-upvotes_count')
        elif order_by == 'downvotes':
            queryset = queryset.annotate(downvotes_count=Count('votes', filter=Q(votes__is_upvote=False))).order_by('-downvotes_count')
        elif order_by == 'date':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at')
        '''

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


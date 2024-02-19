from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics, permissions
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from .models import Team, TeamPokemon, Move, Pokemon
from .serializers import TeamSerializer, TeamPokemonDetailSerializer, \
    PokemonSerializer, MoveSerializer, TeamPokemonListSerializer
from .filters import PokemonFilter, MoveFilter, TeamFilter, TeamPokemonFilter


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.user == request.user


class IsPokemonTeamOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.team.user == request.user


class IsAuthenticatedToCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        return True


class PokemonList(generics.ListAPIView):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PokemonFilter
    ordering_fields = '__all__'


class PokemonDetailView(generics.RetrieveAPIView):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer


class MoveList(generics.ListAPIView):
    queryset = Move.objects.all()
    serializer_class = MoveSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MoveFilter
    ordering_fields = '__all__'


class TeamListCreate(generics.ListCreateAPIView):
    serializer_class = TeamSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TeamFilter
    ordering_fields = ['name', 'is_complete', 'is_private']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Response({"error": "You need to be logged in to see your teams."}, status=status.HTTP_403_FORBIDDEN)
        return Team.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            return Response({"error": "You need to be logged in to create a team."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(user=self.request.user)


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsOwnerOrReadOnly]


class TeamPokemonListCreate(generics.ListCreateAPIView):
    serializer_class = TeamPokemonListSerializer
    permission_classes = [IsPokemonTeamOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TeamPokemonFilter
    ordering_fields = ['slot', 'pokemon__name']

    def get_queryset(self):
        team_id = self.kwargs.get('team_id')
        team = generics.get_object_or_404(Team, id=team_id)
        return TeamPokemon.objects.filter(team=team)

    def perform_create(self, serializer):
        team_id = self.kwargs.get('team_id')
        team = generics.get_object_or_404(Team, id=team_id)
        serializer.save(team=team, context={'team_id': team_id})


class TeamPokemonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeamPokemon.objects.all()
    serializer_class = TeamPokemonDetailSerializer
    permission_classes = [IsPokemonTeamOwner]

    def perform_update(self, serializer):
        serializer.save(team=self.get_object().team)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics, permissions
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Team, TeamPokemon, Move, Pokemon
from .serializers import TeamSerializer, TeamPokemonShortListSerializer, TeamDetailSerializer, TeamPokemonSerializer, \
    PokemonSerializer, MoveSerializer
from .filters import PokemonFilter, MoveFilter, TeamFilter
from rest_framework.authentication import SessionAuthentication


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


class TeamDetail(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def update_is_complete(self, team):
        if team.pokemons.count() >= 6:
            team.is_complete = True
        else:
            team.is_complete = False
        team.save()

    def post(self, request, team_id):
        try:
            team = Team.objects.get(pk=team_id)
            if team.user == request.user:
                if team.is_complete:
                    return Response({"error": "Team is already complete."},
                                    status=status.HTTP_400_BAD_REQUEST)
                serializer = TeamPokemonSerializer(data=request.data, context={'team_id': team_id})
                if serializer.is_valid():
                    slot = serializer.validated_data.get('slot')
                    if TeamPokemon.objects.filter(team=team, slot=slot).exists():
                        return Response({"error": "A Pokemon with this slot already exists in this team."},
                                        status=status.HTTP_400_BAD_REQUEST)
                    serializer.save()
                    self.update_is_complete(team)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "You don't have permission to add a Pokemon to this team."},
                                status=status.HTTP_403_FORBIDDEN)
        except Team.DoesNotExist:
            return Response({"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, team_id):
        try:
            team = Team.objects.get(pk=team_id)
            if team.user != request.user and team.is_private:
                return Response({"error": "You don't have permission to access this team."},
                                status=status.HTTP_403_FORBIDDEN)
            else:
                serializer = TeamDetailSerializer(team)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Team.DoesNotExist:
            return Response({"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, team_id):
        try:
            team = Team.objects.get(pk=team_id)
            if team.user == request.user:
                serializer = TeamDetailSerializer(team, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    pokemons_data = request.data.get('pokemons')
                    if pokemons_data:
                        for pokemon_data in pokemons_data:
                            pokemon_id = pokemon_data.get('id')
                            pokemon_instance = TeamPokemon.objects.get(id=pokemon_id, team=team)
                            pokemon_serializer = TeamPokemonSerializer(pokemon_instance, data=pokemon_data,
                                                                       partial=True)
                            if pokemon_serializer.is_valid():
                                pokemon_serializer.save()
                            else:
                                return Response(pokemon_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "You don't have permission to update this team."},
                                status=status.HTTP_403_FORBIDDEN)
        except Team.DoesNotExist:
            return Response({"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, team_id):
        try:
            team = Team.objects.get(pk=team_id)
            if team.user == request.user:
                serializer = TeamDetailSerializer(team, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    pokemons_data = request.data.get('pokemons')
                    if pokemons_data:
                        for pokemon_data in pokemons_data:
                            pokemon_id = pokemon_data.get('id')
                            pokemon_instance = TeamPokemon.objects.get(id=pokemon_id, team=team)
                            pokemon_serializer = TeamPokemonSerializer(pokemon_instance, data=pokemon_data,
                                                                       partial=True)
                            if pokemon_serializer.is_valid():
                                pokemon_serializer.save()
                            else:
                                return Response(pokemon_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "You don't have permission to update this team."},
                                status=status.HTTP_403_FORBIDDEN)
        except Team.DoesNotExist:
            return Response({"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, team_id):
        try:
            team = Team.objects.get(pk=team_id)
            if team.user == request.user:
                team.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"error": "You don't have permission to delete this team."},
                                status=status.HTTP_403_FORBIDDEN)
        except Team.DoesNotExist:
            return Response({"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND)


class TeamPokemonDetail(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def update_is_complete_pkm(self, team):
        if team.pokemons.count() >= 6:
            team.is_complete = True
        else:
            team.is_complete = False
        team.save()

    def delete(self, request, team_id, slot):
        try:
            team_pokemon = TeamPokemon.objects.get(team_id=team_id, slot=slot)
            team_pokemon.delete()
            self.update_is_complete_pkm(team_pokemon.team)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TeamPokemon.DoesNotExist:
            return Response({"error": "TeamPokemon not found."}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, team_id, slot):
        try:
            team_pokemon = TeamPokemon.objects.get(team_id=team_id, slot=slot)
            pokemon = team_pokemon.pokemon
            moves = team_pokemon.moves.all()

            pokemon_serializer = PokemonSerializer(pokemon)
            moves_serializer = MoveSerializer(moves, many=True)

            return Response({
                "pokemon": pokemon_serializer.data,
                "moves": moves_serializer.data
            }, status=status.HTTP_200_OK)
        except TeamPokemon.DoesNotExist:
            return Response({"error": "TeamPokemon not found."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, team_id, slot):
        try:
            team_pokemon = TeamPokemon.objects.get(team_id=team_id, slot=slot)
            data = {'moves': request.data.get('moves')}
            serializer = TeamPokemonSerializer(team_pokemon, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TeamPokemon.DoesNotExist:
            return Response({"error": "TeamPokemon not found."}, status=status.HTTP_404_NOT_FOUND)


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


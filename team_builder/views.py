from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Team, TeamPokemon, Move
from .serializers import TeamSerializer, TeamPokemonShortListSerializer, TeamDetailSerializer, TeamPokemonSerializer, \
    PokemonSerializer, MoveSerializer
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication


class TeamCreate(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        request.data['user'] = request.user.id
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        teams = Team.objects.filter(user=request.user)
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeamDetail(APIView):
    permission_classes = [AllowAny]

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
    def delete(self, request, team_id, slot):
        try:
            team_pokemon = TeamPokemon.objects.get(team_id=team_id, slot=slot)
            team_pokemon.delete()
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
            data = {'moves': request.data.get('moves')}  # Tylko pola moves można zmieniać
            serializer = TeamPokemonSerializer(team_pokemon, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TeamPokemon.DoesNotExist:
            return Response({"error": "TeamPokemon not found."}, status=status.HTTP_404_NOT_FOUND)


# Needs reviewing
class UserTeamListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        teams = Team.objects.filter(user=user)

        sort_by = request.query_params.get('sort_by')
        if sort_by == 'name':
            teams = teams.order_by('name')
        elif sort_by == 'id':
            teams = teams.order_by('-id')

        serialized_teams = []
        for team in teams:
            serialized_pokemons = TeamPokemonShortListSerializer(team.pokemons.all(), many=True).data
            serialized_team = {
                'name': team.name,
                'pokemons': serialized_pokemons
            }
            serialized_teams.append(serialized_team)

        return Response(serialized_teams)


class MoveList(APIView):
    def get(self, request):
        moves = Move.objects.all()
        name = request.query_params.get('name')
        if name:
            moves = moves.filter(name__icontains=name)

        type = request.query_params.get('type')
        if type:
            moves = moves.filter(type__name__icontains=type)

        category = request.query_params.get('category')
        if category:
            moves = moves.filter(category__icontains=category)

        sort_by = request.query_params.get('sort_by', 'id')
        moves = moves.order_by(sort_by)

        serializer = MoveSerializer(moves, many=True)

        return Response(serializer.data)

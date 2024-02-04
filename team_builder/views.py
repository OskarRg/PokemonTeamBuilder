from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Team, TeamPokemon
from .serializers import TeamSerializer, TeamPokemonCreateSerializer, TeamPokemonShortListSerializer, TeamDetailSerializer
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication


class TeamListCreateAPIView(APIView):
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


class TeamDetailAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, team_id):
        try:
            team = Team.objects.get(pk=team_id)
            if team.user == request.user:
                serializer = TeamDetailSerializer(team)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "You don't have permission to access this team."},
                                status=status.HTTP_403_FORBIDDEN)
        except Team.DoesNotExist:
            return Response({"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, team_id):
        try:
            team = Team.objects.get(pk=team_id)
            if team.user == request.user:
                serializer = TeamDetailSerializer(team, data=request.data)
                if serializer.is_valid():
                    serializer.save()
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


class TeamPokemonCreateAPIView(APIView):
    def post(self, request, team_id):
        try:
            team = Team.objects.get(pk=team_id)
            if team.user == request.user:
                serializer = TeamPokemonCreateSerializer(data=request.data, context={'team_id': team_id})
                if serializer.is_valid():
                    slot = serializer.validated_data.get('slot')
                    if TeamPokemon.objects.filter(team=team, slot=slot).exists():
                        return Response({"error": "A Pokemon with this slot already exists in this team."},
                                        status=status.HTTP_400_BAD_REQUEST)
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "You don't have permission to add a Pokemon to this team."},
                                status=status.HTTP_403_FORBIDDEN)
        except Team.DoesNotExist:
            return Response({"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND)


class TeamPokemonDeleteAPIView(APIView):
    def delete(self, request, team_id, slot):
        try:
            team_pokemon = TeamPokemon.objects.get(team_id=team_id, slot=slot)
            if team_pokemon.team.user == request.user:
                team_pokemon.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"error": "You don't have permission to delete this Pokemon from the team."},
                                status=status.HTTP_403_FORBIDDEN)
        except TeamPokemon.DoesNotExist:
            return Response({"error": "Team Pokemon not found."},
                            status=status.HTTP_404_NOT_FOUND)


class TeamPokemonUpdateAPIView(APIView):
    def patch(self, request, team_id, slot):
        try:
            team = Team.objects.get(pk=team_id)
            if team.user == request.user:
                try:
                    pokemon = TeamPokemon.objects.get(team=team, slot=slot)
                except TeamPokemon.DoesNotExist:
                    return Response({"error": "No Pokemon found with this slot in this team."},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer = TeamPokemonCreateSerializer(pokemon, data=request.data, context={'team_id': team_id},
                                                         partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "You don't have permission to update Pokemon in this team."},
                                status=status.HTTP_403_FORBIDDEN)
        except Team.DoesNotExist:
            return Response({"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND)


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

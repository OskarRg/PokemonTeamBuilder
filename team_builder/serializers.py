from rest_framework import serializers
from .models import Team, Move, Pokemon, TeamPokemon


class TeamPokemonShortListSerializer(serializers.ModelSerializer):
    pokemon_name = serializers.CharField(source='pokemon.name')

    class Meta:
        model = TeamPokemon
        fields = ['pokemon_id', 'pokemon_name', 'slot']


class TeamSerializer(serializers.ModelSerializer):
    pokemons = TeamPokemonShortListSerializer(read_only=True, many=True, source='pokemons.all')
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Team
        fields = '__all__'

    def create(self, validated_data):
        team = Team.objects.create(**validated_data)
        return team


class TeamPokemonSerializer(serializers.ModelSerializer):
    slot = serializers.IntegerField(min_value=1, max_value=6)
    moves = serializers.PrimaryKeyRelatedField(queryset=Move.objects.all(), many=True)

    class Meta:
        model = TeamPokemon
        exclude = ['team']
        read_only_fields = ('id',)

    def validate_moves(self, value):
        if len(value) > 4:
            raise serializers.ValidationError("A Pokemon can have at most 4 moves.")
        return value

    def create(self, validated_data):
        team_id = self.context.get('team_id')
        moves_data = validated_data.pop('moves', [])

        team_pokemon = TeamPokemon.objects.create(team_id=team_id, **validated_data)

        team_pokemon.moves.add(*moves_data)

        return team_pokemon

    def update(self, instance, validated_data):
        moves = validated_data.pop('moves', None)
        slot = validated_data.pop('slot', None)
        pokemon = validated_data.pop('pokemon', None)

        if moves is not None:
            instance.moves.set(moves)
        if slot is not None:
            instance.slot = slot
        if pokemon is not None:
            instance.pokemon = pokemon

        instance.save()
        return instance


class TeamDetailSerializer(serializers.ModelSerializer):
    pokemons = TeamPokemonSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'user', 'is_complete', 'is_private', 'pokemons']
        read_only_fields = ('id', 'user', 'name', 'is_complete')


class MoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Move
        fields = '__all__'


class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = '__all__'

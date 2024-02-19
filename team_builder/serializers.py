from rest_framework import serializers
from .models import Team, Move, Pokemon, TeamPokemon


class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = '__all__'


class MoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Move
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        read_only_fields = ['user', 'is_complete']


class TeamPokemonListSerializer(serializers.ModelSerializer):
    moves = serializers.PrimaryKeyRelatedField(queryset=Move.objects.all(), required=False, many=True)
    slot = serializers.IntegerField(min_value=1, max_value=6, required=False)

    class Meta:
        model = TeamPokemon
        fields = '__all__'
        read_only_fields = ['team']

    def validate_slot(self, value):
        team_id = self.context.get('team_id')
        if team_id:
            team = Team.objects.get(pk=team_id)
            if TeamPokemon.objects.filter(team=team, slot=value).exists():
                raise serializers.ValidationError("Slot is already occupied.")

        return value

    def validate_moves(self, value):
        if len(set(value)) != len(value):
            raise serializers.ValidationError("Each move must be different.")
        if len(value) > 4:
            raise serializers.ValidationError("A Pokemon cannot have more than 4 moves.")
        return value

    def create(self, validated_data):
        team_id = self.context.get('team_id')
        team = Team.objects.get(pk=team_id)
        validated_data['team'] = team
        return super().create(validated_data)


class TeamPokemonDetailSerializer(serializers.ModelSerializer):
    moves = serializers.PrimaryKeyRelatedField(queryset=Move.objects.all(), required=False, many=True)
    slot = serializers.IntegerField(min_value=1, max_value=6, required=False)

    class Meta:
        model = TeamPokemon
        fields = '__all__'
        read_only_fields = ['team']

    def validate_slot(self, value):
        instance = self.instance
        team_id = instance.team_id

        team = Team.objects.get(pk=team_id)
        if instance and instance.slot == value:
            return value
        if TeamPokemon.objects.filter(team=team, slot=value).exists():
            raise serializers.ValidationError("Slot is already occupied.")
        return value

    def validate_moves(self, value):
        if len(set(value)) != len(value):
            raise serializers.ValidationError("Each move must be different.")
        if len(value) > 4:
            raise serializers.ValidationError("A Pokemon cannot have more than 4 moves.")
        return value

from rest_framework import serializers
from .models import TeamComment, PokemonComment, Vote


class TeamCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamComment
        fields = '__all__'
        read_only_fields = ['user', 'team']


class PokemonCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonComment
        fields = '__all__'
        read_only_fields = ['user', 'pokemon']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['user', 'content_type', 'object_id', 'is_upvote']
        read_only_fields = ['user', 'content_type', 'object_id']

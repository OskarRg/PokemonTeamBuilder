from rest_framework import serializers
from .models import TeamComment, PokemonComment, Upvote, Downvote


class TeamCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamComment
        fields = '__all__'
        read_only_fields = ['user', 'team']


class TeamCommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamComment
        fields = ['id', 'content', 'created_at', 'user', 'team']
        read_only_fields = ['user', 'team']


class PokemonCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonComment
        fields = '__all__'
        read_only_fields = ['user', 'pokemon']


class PokemonCommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonComment
        fields = ['id', 'content', 'created_at', 'user', 'pokemon']
        read_only_fields = ['user', 'pokemon']


class UpvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upvote
        fields = '__all__'
        read_only_fields = ['team_comment', 'pokemon_comment']


class DownvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Downvote
        fields = '__all__'
        read_only_fields = ['team_comment', 'pokemon_comment']

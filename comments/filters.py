import django_filters
from .models import TeamComment, PokemonComment


class TeamCommentFilter(django_filters.FilterSet):
    class Meta:
        model = TeamComment
        fields = {
            'content': ['iexact', 'icontains'],
            'user': ['exact'],
            'created_at': ['exact', 'gt', 'lt', 'gte', 'lte'],
        }


class PokemonCommentFilter(django_filters.FilterSet):
    class Meta:
        model = PokemonComment
        fields = {
            'content': ['iexact', 'icontains'],
            'user': ['exact'],
            'created_at': ['exact', 'gt', 'lt', 'gte', 'lte'],
        }

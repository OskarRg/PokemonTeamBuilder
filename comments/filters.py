import django_filters
from .models import TeamComment, PokemonComment


class AbstractCommentFilter(django_filters.FilterSet):
    class Meta:
        abstract = True
        model = None
        fields = {
            'content': ['iexact', 'icontains'],
            'user': ['exact'],
            'created_at': ['exact', 'gt', 'lt', 'gte', 'lte'],
        }


class TeamCommentFilter(AbstractCommentFilter):
    class Meta(AbstractCommentFilter.Meta):
        model = TeamComment


class PokemonCommentFilter(AbstractCommentFilter):
    class Meta(AbstractCommentFilter.Meta):
        model = PokemonComment

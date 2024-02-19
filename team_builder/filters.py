import django_filters
from team_builder.models import Pokemon, Move, Team, TeamPokemon

class PokemonFilter(django_filters.FilterSet):
    class Meta:
        model = Pokemon
        fields = {
            'name': ['iexact', 'icontains'],
            'primary_type__name': ['iexact', 'icontains'],
            'secondary_type__name': ['iexact', 'icontains'],
            'hp': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'attack': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'defense': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'sp_attack': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'sp_defense': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'speed': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'is_legendary': ['exact'],
            'is_mythical': ['exact'],
        }


class MoveFilter(django_filters.FilterSet):
    class Meta:
        model = Move
        fields = {
            'name': ['iexact', 'icontains'],
            'type__name': ['iexact', 'icontains'],
            'category': ['iexact', 'icontains'],
            'power': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'accuracy': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'pp': ['exact', 'gt', 'lt', 'gte', 'lte'],
        }


class TeamFilter(django_filters.FilterSet):
    class Meta:
        model = Team
        fields = {
            'name': ['iexact', 'icontains'],
            'is_complete': ['exact'],
            'is_private': ['exact'],
        }


class TeamPokemonFilter(django_filters.FilterSet):
    slot = django_filters.NumberFilter(field_name='slot', lookup_expr='exact')
    pokemon__name = django_filters.CharFilter(field_name='pokemon__name', lookup_expr='icontains')

    class Meta:
        model = TeamPokemon
        fields = ['slot', 'pokemon__name']

    def filter_by_team_id(self, queryset, value):
        return queryset.filter(team_id=value)
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from team_builder.models import Team, Pokemon


class AbstractComment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    votes = GenericRelation('Vote')

    class Meta:
        abstract = True


class TeamComment(AbstractComment):
    team = models.ForeignKey(Team, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.content}'


class PokemonComment(AbstractComment):
    pokemon = models.ForeignKey(Pokemon, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.content}'


class Vote(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='votes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': ['teamcomment', 'pokemoncomment']})
    object_id = models.PositiveIntegerField()
    comment = GenericForeignKey('content_type', 'object_id')
    is_upvote = models.BooleanField()

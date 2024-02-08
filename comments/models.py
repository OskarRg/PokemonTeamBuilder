from django.contrib.auth import get_user_model
from django.db import models

from team_builder.models import Team, Pokemon


class TeamComment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), related_name='team_comments', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.content}'


class PokemonComment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), related_name='pokemon_comments', on_delete=models.CASCADE)
    pokemon = models.ForeignKey(Pokemon, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.content}'


class Upvote(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='upvotes', on_delete=models.CASCADE)
    team_comment = models.ForeignKey(TeamComment, related_name='upvotes', on_delete=models.CASCADE, null=True,
                                     blank=True)
    pokemon_comment = models.ForeignKey(PokemonComment, related_name='upvotes', on_delete=models.CASCADE, null=True,
                                        blank=True)


class Downvote(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='downvotes', on_delete=models.CASCADE)
    team_comment = models.ForeignKey(TeamComment, related_name='downvotes', on_delete=models.CASCADE, null=True,
                                     blank=True)
    pokemon_comment = models.ForeignKey(PokemonComment, related_name='downvotes', on_delete=models.CASCADE, null=True,
                                        blank=True)

from django.db import models
from django.contrib.auth.models import User
from django.db.models import ForeignKey


class Type(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Pokemon(models.Model):
    name = models.CharField(max_length=50)
    type = ForeignKey(Type, on_delete=models.CASCADE)
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    sp_attack = models.IntegerField()
    sp_defense = models.IntegerField()
    speed = models.IntegerField()

    def __str__(self):
        return self.name


class Move(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    power = models.IntegerField(null=True)
    accuracy = models.IntegerField(null=True)
    pp = models.IntegerField(null=True)

    def __str__(self):
        # Might use these
        # power_str = str(self.power) if self.power is not None else '---'
        # accuracy_str = str(self.accuracy) if self.accuracy is not None else '---'
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, related_name='teams', on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class TeamPokemon(models.Model):
    team = models.ForeignKey(Team, related_name='pokemons', on_delete=models.CASCADE)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    moves = models.ManyToManyField(Move, related_name='team_pokemons')
    slot = models.IntegerField()

    def __str__(self):
        return f'{self.team.name} - {self.pokemon.name} (slot {self.slot})'


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.content}'


class BuiltInTeam(models.Model):
    name = models.CharField(max_length=50)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class BuiltInTeamPokemon(models.Model):
    team = models.ForeignKey(BuiltInTeam, related_name='pokemons', on_delete=models.CASCADE)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    move = models.ManyToManyField(Move, related_name='builtin_team_pokemons')
    slot = models.IntegerField()

    def __str__(self):
        return f'{self.team.name} - {self.pokemon.name}'

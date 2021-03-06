from django.db import models


class Game(models.Model):

    name = models.CharField(max_length=50)
    min_players = models.IntegerField()
    max_players = models.IntegerField()
    difficulty = models.CharField(max_length=50)
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE)
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)

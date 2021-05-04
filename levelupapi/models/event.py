from django.db import models
from .game import Game
from .gamer import Gamer


class Event(models.Model):

    name = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    content = models.TextField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    host = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(
        "Gamer", through="GamerEvent", related_name="Attending")

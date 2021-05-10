from django.db import models
from .game import Game
from .gamer import Gamer


class Event(models.Model):

    name = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    content = models.TextField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    host = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(
        "Gamer", through="GamerEvent", related_name="Attending")

    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value
from django.db import models


class GameType(models.Model):

    type_name = models.CharField(max_length=50)

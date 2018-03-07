from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

# purchasing a game creates one of transaction objects, used to validate users right to play a game
class Transaction(models.Model):
	trID = models.CharField(max_length=40,unique=True)
	customer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='game_purchases', null=True, default=None)
	developer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='game_sales', null=True, default=None)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	price = models.DecimalField(decimal_places=2, max_digits=4, validators=[MinValueValidator(0, message='Price cannot be negative')])
	datetime = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10)
	bankreference = models.CharField(max_length=7, blank=True, null=True)

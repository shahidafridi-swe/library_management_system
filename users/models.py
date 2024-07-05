from django.db import models
from django.contrib.auth.models import User


class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    account_number = models.IntegerField(unique=True)
    balance = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return f"{self.user.username} - {self.account_number}"
    
    
from django.db import models
from django.contrib.auth.models import User


class user(models.Model):
    username = models.OneToOneField(User,on_delete=models.CASCADE)

    Type1 = (
        ('user', 'user'),
        ('seller', 'seller'),
    )
    type = models.CharField(max_length=8, choices=Type1, default='user')

    def __str__(self):
        return self.username.__str__()


class Item(models.Model):
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    seller = models.ForeignKey(user, on_delete=models.CASCADE, limit_choices_to={'type': 'seller',})


class orderlog(models.Model):
    user=models.CharField(max_length=150)
    seller=models.CharField(max_length=150)
    order=models.CharField(max_length=10000)
    qty=models.CharField(max_length=10000,default='0' )
    total=models.IntegerField()



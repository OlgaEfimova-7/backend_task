from django.db import models


class User(models.Model):
    img = models.CharField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=30)
    available = models.BooleanField()
    friends = models.ManyToManyField('self', through='FriendList')


class FriendList(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='initial_user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='friend_user')

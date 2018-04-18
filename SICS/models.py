from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    sender_username = models.CharField(max_length=30)
    sender_first_name = models.CharField(max_length=30)
    sender_last_name = models.CharField(max_length=30)
    recipient = models.CharField(max_length=1000)
    data = models.CharField(max_length=1000)
    time = models.DateTimeField()

    def __str__(self):
        return self.sender_username + " " + self.recipient + " " + str(self.time)


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.CharField(max_length=30)
    recipient = models.CharField(max_length=1000)
    data = models.CharField(max_length=1000)
    time = models.DateTimeField()
    status = models.IntegerField()

    def __str__(self):
        return self.sender + " " + self.recipient + " " + str(self.time)


class Friend(models.Model):
    id = models.AutoField(primary_key=True)
    userA = models.CharField(max_length=30)
    userB = models.CharField(max_length=30)

    def __str__(self):
        return self.userA + " " + self.userB

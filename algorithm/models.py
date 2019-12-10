from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    uname = models.CharField(max_length=50)
    upwd = models.CharField(max_length=100)
    # active inactive
    status = models.CharField(max_length=10)


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    # deleted alive
    status = models.CharField(max_length=10)

class A(models.Model):
    id = models.AutoField(primary_key=True)
    a0 = models.FloatField()
    a1 = models.FloatField()
    a2 = models.FloatField()
   
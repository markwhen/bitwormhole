# -*- coding: utf-8 -*-
from django.db import models

#bitwormhole models
class BUser(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    def __unicode__(self):
        return self.username
    class Meta:
        ordering = ['username']
class BName(models.Model):
    name = models.CharField(max_length=30)
    datetime = models.DateTimeField()
    wormholeclass = models.CharField(max_length=1)
    volumnlimit = models.IntegerField()
    founder = models.ForeignKey(BUser)

    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']
class BFile(models.Model):
    filename = models.CharField(max_length=100)
    bname = models.ForeignKey(BName)
    datetime = models.DateTimeField()
    key = models.CharField(max_length=20)
    add = models.CharField(max_length=140)
    like = models.IntegerField()
    def __unicode__(self):
        return self.filename
    class Meta:
        ordering = ['filename']

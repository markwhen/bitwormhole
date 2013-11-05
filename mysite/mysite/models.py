#from django.db import models

#class userlist(models.Model):
#    email = models.CharField(max_length=20)
#    password = models.CharField(max_length=20)
#    username = models.CharField(max_length=20)
#    info = models.CharField(max_length=100)
#    def __unicode__(self):
#        return self.email
#class grouplist(models.Model):
#    groupname = models.CharField(max_length=20)
#    groupclass = models.CharField(max_length=1)
#    password = models.CharField(max_length=20)
#    def __unicode__(self):
#        return self.groupname
#class groupadmin(models.Model):
#    groupid = models.IntegerField()
#    admin1id = models.IntegerField()
#    admin2id = models.IntegerField()
#    admin3id = models.IntegerField()
#    def __unicode__(self):
#        return u'%s %s' % (self.groupid, self.admin1id)
#class groupuser(models.Model):
#    groupid = models.IntegerField()
#    userid = models.IntegerField()
#    def __unicode__(self):
#        return u'%s %s' % (self.groupid, self.userid)

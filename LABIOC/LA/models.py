from django.db import models

# Create your models here.

class SHHost(models.Model):
    host_name = models.CharField(max_length=200)
    ip = models.GenericIPAddressField(null=True)
    owner = models.CharField(max_length=200)
    os = models.CharField(max_length=200,null=True)
    lastcu = models.CharField(max_length=200,null=True)
    compliant = models.BooleanField(default=False,null=True)
    lastscantime = models.DateTimeField(null=True)
    def __str__(self):
        return self.host_name

class Patch(models.Model):
    title = models.CharField(max_length=200)
    kbnumber = models.CharField(max_length=200)

class VirtualMachine(models.Model):
    vm_name = models.CharField(max_length=200)
    ip = models.GenericIPAddressField(null=True)
    owner = models.CharField(max_length=200)
    os = models.CharField(max_length=200,null=True)
    lastcu = models.CharField(max_length=200,null=True)
    compliant = models.BooleanField(default=True)
    lastscantime = models.DateTimeField(null=True)
    loc_host = models.ForeignKey(SHHost,on_delete=models.CASCADE,db_column='host_name')
    def __str__(self):
        return self.vm_name

class Vulnerability(models.Model):
    vulid = models.IntegerField(default=0)
    vulname = models.CharField(max_length=200)
    vuldescription = models.CharField(max_length=600)
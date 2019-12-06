from django.db import models
import uuid
# Create your models here.


class SHHost(models.Model):
    machine_name = models.CharField(max_length=200, unique=True)
    ip = models.GenericIPAddressField(null=True,blank=True)
    owner = models.CharField(max_length=200,null=True)
    obsolete = models.BooleanField(default=False)
    os = models.CharField(max_length=200,null=True,blank=True)
    osversion = models.CharField(max_length=200,null=True,blank=True)
    oslang = models.CharField(max_length=200,null=True,blank=True)
    installedupdate = models.TextField(null=True,blank=True)
    lastcu = models.CharField(max_length=200,null=True,blank=True)
    compliant = models.BooleanField(default=False,null=True,blank=True)
    lastscantime = models.DateTimeField(null=True,blank=True)
    rebootrequired = models.BooleanField(default=False,null=True,blank=True)
    vms = models.TextField(null=True,blank=True)
    status = models.IntegerField(null=True,blank=True)
    msg = models.CharField(max_length=200,null=True,blank=True)
    sqlversion = models.CharField(max_length=200,null=True,blank=True)
    vsinstalled = models.CharField(max_length=200,null=True,blank=True)
    def __str__(self):
        return self.machine_name


class Patch(models.Model):
    title = models.CharField(max_length=200)
    kbnumber = models.CharField(max_length=200)

class SHVirtualMachine(models.Model):
    machine_name = models.CharField(max_length=200)
    vmid = models.UUIDField(default=uuid.uuid4())
    fullyqualifieddomainname = models.CharField(max_length=200,null=True,blank=True)
    domainname = models.CharField(max_length=200,null=True,blank=True)
    ip = models.GenericIPAddressField(null=True,blank=True)
    owner = models.CharField(max_length=200,null=True,blank=True)
    os = models.CharField(max_length=200,null=True,blank=True)
    osversion = models.CharField(max_length=200,null=True,blank=True)
    oslang = models.CharField(max_length=200,null=True,blank=True)
    installedupdate = models.TextField(null=True,blank=True)
    lastcu = models.CharField(max_length=200,null=True,blank=True)
    compliant = models.BooleanField(default=False,blank=True)
    lastscantime = models.DateTimeField(null=True,blank=True)
    rebootrequired = models.BooleanField(default=False,null=True,blank=True)
    loc_host = models.ForeignKey(SHHost,on_delete=models.CASCADE,db_column='host_name')
    status = models.IntegerField(null=True,blank=True)
    msg = models.CharField(max_length=200,null=True,blank=True)
    sqlversion = models.CharField(max_length=200,null=True,blank=True)
    vsinstalled = models.CharField(max_length=200,null=True,blank=True)
    def __str__(self):
        return self.machine_name

class Vulnerability(models.Model):
    vulid = models.IntegerField(default=0)
    vulname = models.CharField(max_length=200)
    vuldescription = models.CharField(max_length=600)

class REDHost(models.Model):
    machine_name = models.CharField(max_length=200, unique=True)
    ip = models.GenericIPAddressField(null=True,blank=True)
    owner = models.CharField(max_length=200,null=True,blank=True)
    obsolete = models.BooleanField(default=False)
    os = models.CharField(max_length=200,null=True,blank=True)
    osversion = models.CharField(max_length=200,null=True,blank=True)
    oslang = models.CharField(max_length=200,null=True,blank=True)
    installedupdate = models.TextField(null=True,blank=True)
    lastcu = models.CharField(max_length=200,null=True,blank=True)
    compliant = models.BooleanField(default=False,null=True)
    lastscantime = models.DateTimeField(null=True,blank=True)
    rebootrequired = models.BooleanField(default=False,null=True,blank=True)
    vms = models.TextField(null=True,blank=True)
    status = models.IntegerField(null=True,blank=True)
    msg = models.CharField(max_length=200,null=True,blank=True)
    sqlversion = models.CharField(max_length=200,null=True,blank=True)
    vsinstalled = models.CharField(max_length=200,null=True,blank=True)
    def __str__(self):
        return self.machine_name
    
class REDVirtualMachine(models.Model):
    machine_name = models.CharField(max_length=200)
    vmid = models.UUIDField(default=uuid.uuid4())
    fullyqualifieddomainname = models.CharField(max_length=200,null=True,blank=True)
    domainname = models.CharField(max_length=200,null=True,blank=True)
    ip = models.GenericIPAddressField(null=True)
    owner = models.CharField(max_length=200,null=True,blank=True)
    os = models.CharField(max_length=200,null=True)
    osversion = models.CharField(max_length=200,null=True,blank=True)
    oslang = models.CharField(max_length=200,null=True,blank=True)
    installedupdate = models.TextField(null=True)
    lastcu = models.CharField(max_length=200,null=True)
    compliant = models.BooleanField(default=False)
    lastscantime = models.DateTimeField(null=True)
    rebootrequired = models.BooleanField(default=False,null=True,blank=True)
    loc_host = models.ForeignKey(REDHost,on_delete=models.CASCADE,db_column='host_name')
    status = models.IntegerField(null=True,blank=True)
    msg = models.CharField(max_length=200,null=True,blank=True)
    sqlversion = models.CharField(max_length=200,null=True,blank=True)
    vsinstalled = models.CharField(max_length=200,null=True,blank=True)
    def __str__(self):
        return self.machine_name

        
class AzureVirtualMachine(models.Model):
    machine_name = models.CharField(max_length=200)
    fullyqualifieddomainname = models.CharField(max_length=200,null=True,blank=True)
    domainname = models.CharField(max_length=200,null=True,blank=True)
    ip = models.GenericIPAddressField(null=True)
    os = models.CharField(max_length=200,null=True)
    osversion = models.CharField(max_length=200,null=True,blank=True)
    oslang = models.CharField(max_length=200,null=True,blank=True)
    installedupdate = models.TextField(null=True)
    lastcu = models.CharField(max_length=200,null=True)
    compliant = models.BooleanField(default=False)
    lastscantime = models.DateTimeField(null=True)
    rebootrequired = models.BooleanField(default=False,null=True,blank=True)
    status = models.IntegerField(null=True,blank=True)
    msg = models.CharField(max_length=200,null=True,blank=True)
    resourceid = models.CharField(max_length=500,null=True,blank=True)
    location = models.CharField(max_length=200,null=True,blank=True)
    resourcename = models.CharField(max_length=200,null=True,blank=True)
    resourcegroupname = models.CharField(max_length=200,null=True,blank=True)
    role = models.CharField(max_length=200,null=True,blank=True)
    owner = models.CharField(max_length=200,null=True,blank=True)
    def __str__(self):
        return self.machine_name

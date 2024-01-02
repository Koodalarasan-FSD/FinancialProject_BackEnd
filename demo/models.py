from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin



# Create your models here.
class Member(models.Model):
    
    # fields here
    memberid=models.CharField(max_length=100,null=True,blank=True)
    membername=models.CharField(max_length=100)
    address=models.TextField()
    photo=models.ImageField(upload_to='',null=True,blank=True)
    description=models.TextField()
    contactnumber=models.BigIntegerField()
    contactnumber2=models.BigIntegerField()
    city=models.CharField(max_length=100)
    joiningdate=models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        db_table='membersprofile'   # Specify your table name here


class Base_class(models.Model):
    
    #fields here
    memberidwithname=models.CharField(max_length=100,null=True,blank=True)
    paymentid=models.CharField(max_length=100)
    amount=models.IntegerField()
    basisamounttopay=models.IntegerField()
    basisamounttopayable=models.IntegerField()
    balanceamounttopay=models.IntegerField()
    description=models.TextField()
    transactiondate=models.CharField(max_length=100,null=True,blank=True)
    currentperiod=models.IntegerField()
    

    class Meta:
        abstract=True # This makes it an abstract base model


class transactions(Base_class):
    
    
    
    noofperiods=models.IntegerField()
    paymentdurationtype=models.CharField(max_length=100)
    status=models.CharField(max_length=52)
    
    class Meta:
        db_table='transactionstable'  # Specify your table name here
        

class payments(Base_class):
    
    #fields here
    

    class Meta:
        db_table='paymentstable'



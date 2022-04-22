from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save, post_delete
from .models import *
import json 
from django.core import serializers


# automatic profile
@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            upload=instance,
            id=instance.id,isIdType=instance.isIdType,
            fullname=instance.fullname,)
        ProfileCart.objects.create(id=instance.id,
            upload=instance, )
        ProfileWishList.objects.create(id=instance.id,
            upload=instance, )
        # if instance.isSeller==True:
        #     SellerProfile.objects.create(
        #     upload=instance,
        #     id=instance.id,isSeller=True,
        #     fullname=instance.fullname,)



@receiver(post_save, sender=CartProduct)
def save_CartProfile(sender, instance, created, **kwargs):
    
        prodList = CartProduct.objects.filter(upload=instance.upload)
        
        
        ammountList=[]
        ammountData=0
        for p in prodList:
          ammountList.append(p.discountPrice)

        for ele in range(0, len(ammountList)):
            ammountData = ammountData + ammountList[ele]

        if ammountData >499:
            ProfileCart.objects.update_or_create(
            upload=instance.upload, defaults= {'ammount':ammountData, 'shipPrice':0, 'totalAmmount':ammountData })
        
        else:
            ProfileCart.objects.update_or_create(
            upload=instance.upload, defaults= {'ammount':ammountData,'shipPrice':70, 'totalAmmount':ammountData+70 })
        


        
        # ProfileCart.objects.update_or_create(
        #     upload=instance.upload, defaults= {'cartUpload':tmpObj })

@receiver(post_save, sender=WishListProduct)
def save_WishListProfile(sender, instance, created, **kwargs):
    
        prodList = WishListProduct.objects.filter(upload=instance.upload)
       
        ammountList=[]
        ammountData=0
        for p in prodList:
          ammountList.append(p.discountPrice)

        for ele in range(0, len(ammountList)):
            ammountData = ammountData + ammountList[ele]

        if ammountData >499:
            ProfileWishList.objects.update_or_create(
            upload=instance.upload, defaults= {'ammount':ammountData, 'shipPrice':0, 'totalAmmount':ammountData })
        
        else:
            ProfileWishList.objects.update_or_create(
            upload=instance.upload, defaults= {'ammount':ammountData,'shipPrice':70, 'totalAmmount':ammountData+70 })
        

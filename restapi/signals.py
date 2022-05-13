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

        offPriceList=[]
        offPriceData=0 
        for p in prodList:
          ammountList.append(p.discountPrice)
          offPriceList.append(p.offPrice)

        for ele in range(0, len(ammountList)):
            ammountData = ammountData + ammountList[ele]
        
        for e in range(0, len(offPriceList)):
            offPriceData = offPriceData + offPriceList[e]
        
        
        

        if ammountData >499:
            ProfileCart.objects.update_or_create(
            upload=instance.upload, defaults= {'ammount':ammountData, 'shipPrice':0, 'totalAmmount':ammountData, 'offPrice':offPriceData,'seller':instance.product.upload })
        
        else:
            ProfileCart.objects.update_or_create(
            upload=instance.upload, defaults= {'ammount':ammountData,'shipPrice':70, 'totalAmmount':ammountData+70,'offPrice':offPriceData ,'seller':instance.product.upload})
        


        
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


# automatic profile
@receiver(post_save, sender=Order)
def save_order(sender, instance, created, **kwargs):
    # print(created)
    if created:
        cartList =CartProduct.objects.filter(upload=instance.upload) 
        # orderList =OrderItem.objects.filter(upload=self.upload) 
       
        for i in cartList:
            OrderItem.objects.create(product=i.product, upload=instance.upload ,order_id=instance.id,seller=i.product.upload, address=instance.address ,cartUpload=i.cartProfile, ammount=i.discountPrice,)



@receiver(post_save, sender=OrderItem)
def save_OrderPrice(sender, instance, created, **kwargs):
    
        orderList = OrderItem.objects.filter(order_id=instance.order_id)
        print(orderList)
        ammountList=[]
        ammountData=0
        for p in orderList:
          ammountList.append(p.ammount)

        print(ammountList)

        for ele in range(0, len(ammountList)):
            ammountData = ammountData + ammountList[ele]

        if ammountData >499:
            Order.objects.update_or_create(
            id=instance.order_id, defaults= {'ammount':ammountData, 'shipPrice':0, 'totalAmmount':ammountData })
        
        else:
            Order.objects.update_or_create(
            upload=instance.order_id, defaults= {'ammount':ammountData,'shipPrice':70, 'totalAmmount':ammountData+70 })
from datetime import date, datetime
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
import uuid
from django.urls import reverse
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
from django.conf import settings

 



# MY CUSTOMUSER
class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    phone = models.CharField(
        unique=True, max_length=15, validators=[RegexValidator("^[789]\d{9}$")]
    )
    fullname = models.CharField(
        _("full name"),
        max_length=130, null=True,blank=True,
    )
    email = models.EmailField(_("emailaddress"), unique=True,null=True,blank=True)
    
    is_phone_verfied=models.BooleanField(default=False)

    is_staff = models.BooleanField(_("is_staff"), default=False)
    is_active = models.BooleanField(_("is_active"), default=True)
    date_joined = models.DateField(_("date_joined"), default=date.today)
    change_pw = models.BooleanField(default=True)
    # isCustomer = models.BooleanField(default=False,null=True,
    #     blank=True,)
    # isSeller = models.BooleanField(default=False,null=True,
    #     blank=True,)
    
    # ! isIdType==False  => Customer  ,,, True => Seller 
    isIdType=  models.BooleanField(default=False,null=True,
        blank=True,)
    

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ("id",)
        verbose_name = _("Accounts")
        verbose_name_plural = _("Acconts")

    def get_short_name(self):
        """
        Returns the display name.
        If full name is present then return full name as display name
        else return username.
        """
        if self.fullname != "":
            return self.fullname
        else:
            return str(self.phone) 


class MobileOtp(models.Model):
    phone = models.CharField(unique=True,
         max_length=15, validators=[RegexValidator("^[789]\d{9}$")]
    )

    otp=models.CharField(max_length=6)
    is_phone_verfied=models.BooleanField(default=False)



class Profile(models.Model):
    id = models.UUIDField(
        primary_key=True,
    )
    # isCustomer = models.BooleanField(default=True)
    isIdType=  models.BooleanField(default=False,null=True,
        blank=True)
    fullname = models.CharField(max_length=100, null=True,blank=True)
    email = models.EmailField(_("emailaddress"), unique=True, null=True, blank=True)
    upload = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=200,
        null=True,
        blank=True,
    )
    pic = models.ImageField(upload_to="CustomerImg", blank=True, null=True)

    businesspic = models.ImageField(upload_to="SellerImg", blank=True, null=True)
    businessname=models.CharField(max_length=100, null=True,
        blank=True,)

    # @permalink
    def get_absolute_url(self):
        return reverse("", kwargs={"pk": self.pk})

    def __str__(self):
        return str(self.upload.id)


# ! Seller Profile 
class ProfileSeller(models.Model):
    id = models.UUIDField(
        primary_key=True,
    )
    isSeller = models.BooleanField(default=False)
    fullname = models.CharField(max_length=100, null=True,blank=True)
    email = models.EmailField(_("emailaddress"), unique=True, null=True, blank=True)
    upload = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=200,
        null=True,
        blank=True,
    )
    businesspic = models.ImageField(upload_to="SellerImg", blank=True, null=True)
    businessname=models.CharField(max_length=100, null=True,
        blank=True,)
    pic = models.ImageField(upload_to="SellerImg", blank=True, null=True)

    # @permalink
    def get_absolute_url(self):
        return reverse("", kwargs={"pk": self.pk})

    def __str__(self):
        return str(self.upload.id)



class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    upload = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="addressuser"
    )
    fullname = models.CharField(
        _("full name"),
        max_length=130,
    )
    phone = models.CharField(max_length=15, validators=[RegexValidator("^[789]\d{9}$")])
    email = models.EmailField(_("emailaddress"), null=True, blank=True)
    house = models.CharField(max_length=300, null=True, blank=True)
    trade = models.CharField(max_length=200, null=True, blank=True)
    area = models.CharField(max_length=200,  null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    pinCode = models.CharField(
        max_length=100,
        validators=[RegexValidator("^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$")],
    )
    delTime = models.CharField(max_length=100,  default="AnyTime")
    state = models.CharField(max_length=200)
    

    def __str__(self):
        return str(self.upload)



# ! Category 
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

# ! Product Model
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    salesPrice = models.FloatField()
    discountPrice = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    stock = models.PositiveIntegerField()
    pic=models.FileField(upload_to='ProdcutImg',blank=True,null=True)
    pic1=models.FileField(upload_to='ProdcutImg',blank=True,null=True)
    pic2=models.FileField(upload_to='ProdcutImg',blank=True,null=True)
    pic3=models.FileField(upload_to='ProdcutImg',blank=True,null=True)
    
    offers = models.IntegerField(default=1, null=True, blank=True)
    
    upload = models.ForeignKey(
        to=CustomUser,
        # to=ProfileSeller,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,null=True,blank=True
    )
    quantity = models.PositiveIntegerField(default=1)
    ammount = models.PositiveIntegerField(default=0)
    cartItem =models.BooleanField(default=False)

    # ! this method add ammount value is
    def save(self, *args, **kwargs):
        if not self.pk:  # Check for create
            self.ammount = self.discountPrice * self.quantity
        else:

            self.ammount = self.discountPrice * self.quantity
        return super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse("product", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title




# !  Cart In Product
class CartProduct(models.Model):
    class Meta:
        unique_together = (("upload"), ("product"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    upload = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
   
    salesPrice = models.FloatField(default=0)
    discountPrice = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def user_id(self):
     return self.id.__str__()

    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.salesPrice =self.product.salesPrice * self.quantity
            self.discountPrice=self.product.discountPrice * self.quantity
        else:
            self.salesPrice =self.product.salesPrice * self.quantity
            self.discountPrice=self.product.discountPrice * self.quantity

        return super().save(*args, **kwargs)


    def __str__(self):
        return str(self.id) 

  

# !Cart Profile
class ProfileCart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    upload=models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    cartUpload=models.ForeignKey(CartProduct, on_delete=models.CASCADE, blank=True, null=True)
    ammount =  models.FloatField(default=0)
    shipPrice =  models.FloatField(default=50)
    totalAmmount =  models.FloatField(default=0)
    
    def __str__(self):
        return f"cartID ={self.id}user={self.upload}"
    
    def get_cartList(self):
        usr=self.upload
        prodList = CartProduct.objects.filter(upload=self.upload) 
        ammountList=[]
        total=0
        for p in prodList:
            a= p.discountPrice * p.quantity 
            ammountList.append(a)

        for ele in range(0, len(ammountList)):
          total = total + ammountList[ele]
        return f' {list(prodList).__len__() }   {total} {list(prodList)}'
       



# ! Wishlist Product 
class WishListProduct(models.Model):
    class Meta:
        unique_together = (("upload"), ("product"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    upload = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
   
    salesPrice = models.FloatField(default=0)
    discountPrice = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def user_id(self):
     return self.id.__str__()

    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.salesPrice =self.product.salesPrice * self.quantity
            self.discountPrice=self.product.discountPrice * self.quantity
        else:
            self.salesPrice =self.product.salesPrice * self.quantity
            self.discountPrice=self.product.discountPrice * self.quantity

        return super().save(*args, **kwargs)


    def __str__(self):
        return str(self.id) 

  

# !Cart Profile
class ProfileWishList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    upload=models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    ammount =  models.FloatField(default=0)
    shipPrice =  models.FloatField(default=50)
    totalAmmount =  models.FloatField(default=0)
    
    def __str__(self):
        return f"wishListID ={self.id} user={self.upload}"
    
    def get_wishList(self):
        usr=self.upload
        prodList = WishListProduct.objects.filter(upload=self.upload) 
        ammountList=[]
        total=0
        for p in prodList:
            a= p.discountPrice * p.quantity 
            ammountList.append(a)

        for ele in range(0, len(ammountList)):
          total = total + ammountList[ele]
        return f' {list(prodList).__len__() }   {total} {list(prodList)}'
       




# !ORDER BASE CLASS
# class BaseOrder(models.Model):
#     customer = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     product = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#     )
#     seller=models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True,
#         blank=True)
#     address = models.ForeignKey(Address, on_delete=models.CASCADE)
#     date = models.DateTimeField(auto_now_add=True)
#     quantity = models.PositiveIntegerField(default=1)
#     ammount = models.PositiveIntegerField()
#     shipPrice = models.PositiveIntegerField(default=50)
#     totalAmmount = models.PositiveIntegerField(default=0)

#     # ! this method add ammount value is
#     def save(self, *args, **kwargs):
#         if not self.pk:
#             self.ammount = self.product.discountPrice * self.quantity
#             if self.ammount > 499:
#                 self.shipPrice = 0
#                 self.totalAmmount = self.ammount + self.shipPrice
#             else:
#                 self.shipPrice = 70
#                 self.totalAmmount = self.ammount + self.shipPrice
#         else:
#             self.ammount = self.product.discountPrice * self.quantity
#             if self.ammount > 499:
#                 self.shipPrice = 0
#                 self.totalAmmount = self.ammount + self.shipPrice
#             else:
#                 self.shipPrice = 70
#                 self.totalAmmount = self.ammount + self.shipPrice

#         return super().save(*args, **kwargs)

#     def __str__(self):
#         return str(self.id)

#     class Meta:
#         abstract = True   



# # ! All Order 
# class Order(BaseOrder):
#     id = models.UUIDField(
#         primary_key=True,
#         editable=False,
#         default=uuid.uuid4,
#     )
#     # customer = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     # seller=models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True,blank=True)
#     # cartProduct=models.ForeignKey(CartProfile,on_delete=models.CASCADE,null=True, blank=True)
#     # address = models.ForeignKey(Address, on_delete=models.CASCADE)
#     # date = models.DateTimeField(auto_now_add=True)
#     # quantity = models.PositiveIntegerField(default=1)
#     # ammount = models.PositiveIntegerField()
#     # shipPrice = models.PositiveIntegerField(default=50)
#     # totalAmmount = models.PositiveIntegerField(default=0)

 
#     status = models.CharField(max_length=100, default='Pendiing')
#     selOrderStatus = models.CharField(
#         max_length=100,
#         null=True,
#         blank=True,
#     )

# # ! CURRENT ORDER
# class OrderCurrent(models.Model):
#     id = models.UUIDField(
#         primary_key=True,
#     )
#     orderSeller = models.ForeignKey(Order, on_delete=models.CASCADE)
#     orderStatus = models.CharField(
#         max_length=100,
        
#         default="OrderConfirm",
#         null=True,
#         blank=True,
#     )


# #! Success ORDER
# class OrderSuccess(models.Model):
#     id = models.UUIDField(
#         primary_key=True,
#     )
#     orderSeller = models.ForeignKey(Order, on_delete=models.CASCADE)


# # !CANCEL ORDER
# class OrderCancel(models.Model):
#     id = models.UUIDField(
#         primary_key=True,
#     )
#     upload = models.ForeignKey(
#         Order, on_delete=models.CASCADE, null=True, blank=True
#     )
#     cancelby = models.CharField(max_length=50,null=True, blank=True)
   

class Order(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    upload= models.ForeignKey('CustomUser',  on_delete=models.CASCADE)
    cartUpload = models.ForeignKey('ProfileCart', on_delete=models.CASCADE)

    status = models.CharField(max_length=100, default='Pendiing')
    selOrderStatus = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    address = models.ForeignKey(Address, on_delete=models.CASCADE,null=True,blank=True)


    ammount =  models.FloatField(default=0)
    shipPrice =  models.FloatField(default=50)
    totalAmmount =  models.FloatField(default=0)

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    
    transcationId=models.CharField(max_length=30, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    
    def __str__(self):
        return f"cartID ={self.id}user={self.upload}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.ammount =self.cartUpload.ammount
            if self.ammount<499:
                self.shipPrice=70
                self.totalAmmount=self.ammount + self.shipPrice
            else:
                self.shipPrice=0
                self.totalAmmount=self.ammount 

        else:
            self.ammount =self.cartUpload.ammount
            if self.ammount<499:
                self.shipPrice=70
                self.totalAmmount=self.ammount + self.shipPrice
            else:
                self.shipPrice=0
                self.totalAmmount=self.ammount 

        return super().save(*args, **kwargs)



# ! NOTIFICATION MODEl
class Notification(models.Model):
    id = models.UUIDField( primary_key=True, editable=False,default=uuid.uuid4)
    sender=models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True,null=True, related_name="customer")
    recevier = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True,null=True, related_name="seller")
    checked=models.BooleanField(default=False)
    title = models.CharField(max_length=100,blank=True,null=True)
    msg = models.TextField()




class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"





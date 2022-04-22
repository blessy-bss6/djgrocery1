from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import *


# Custom Accounts
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "id",
        "phone",
        "email",
        "fullname",
        "is_staff",
        "password",
    )
    list_filter = (
        "phone",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("phone", "password", "fullname")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone",
                    "fullname",
                     "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("phone",)
    ordering = ("id",)


admin.site.register(CustomUser, CustomUserAdmin)

# ! Mobile Otp Admin
@admin.register(MobileOtp)
class MobileAdmin(admin.ModelAdmin):
    list_display = ("id", "phone", "otp","is_phone_verfied")

# CUSTOMER PROFILE
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "upload", "gender",  "pic", "fullname")

# CUSTOMER PROFILE
@admin.register(ProfileSeller)
class ProfileSellerAdmin(admin.ModelAdmin):
    list_display = ("id", "upload", "businessname","gender",  "pic", "fullname")

# ADDRESS 
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "upload", "phone", "house", "pinCode", "state")


# Product ADMIN
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "upload",  "pic", "pic1" ,"pic2","pic3" ,"title", "description", "salesPrice", "stock", "quantity", "discountPrice")



# Category ADMIN
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","title")



# Cart Product ADMIN
@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ("id", "upload","product", "quantity","salesPrice","discountPrice")

# Cart Profile ADMIN
@admin.register(ProfileCart)
class CartProfileAdmin(admin.ModelAdmin):
      list_display = ("id", "upload",  "ammount","totalAmmount" ,'get_cartList' )





# ! ALL ORDER 
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id","seller","customer",
        "status",
        "product",
        "address",
        "ammount",
        "quantity",
        
    )


# !CURRENT ORDER
@admin.register(OrderCurrent)
class OrderCurrentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "orderStatus",
      
        # "upload",
    )


# ! SUCCESS ORDERKEY
@admin.register(OrderSuccess)
class OrderSuccessAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "orderSeller",
    
        # "upload",
    )


# Cancel Order
@admin.register(OrderCancel)
class OrderCancelAdmin(admin.ModelAdmin):
    list_display = ("id", "cancelby")  



@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "recevier", "checked","msg")  
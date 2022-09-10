from rest_framework import serializers
from .models import *


class CusSer(serializers.ModelSerializer):
    class Meta:
      model=CustomUser
      fields="__all__"


# make accounts in
class RegisterSer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["phone", "password","email","fullname","isIdType"]

        def create(self, validated_data):
            user = CustomUser.objects.create_user(**validated_data)
            return user


class LoginSer(serializers.ModelSerializer):
 
  class Meta:
    model = CustomUser
    fields = [ 'phone', 'password']

# ---------------------------------------------------------------------------- #
#                    orc ProfilePage GET AND POST SERILIZER                    #
# ---------------------------------------------------------------------------- #

# ! PROFILE POST METHOD
class ProfileSer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "fullname",
            "pic",
            "gender",
        ]

class ProfileSellerSer(serializers.ModelSerializer):
    class Meta:
        model = ProfileSeller
        fields = [
            "fullname",
            "pic",
            "gender","isSeller"
        ]

# ALL PRODUCT SHOW DATA
class ProductSer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        depth = 1


class AddProductSer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "salesPrice",
            "discountPrice",
            "stock",
            "pic","pic1","pic2","pic3",
            "upload",
            "category","offers"
        ]

# ALL PRODUCT SHOW DATA
class CategorySer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        depth = 1
# ---------------------------------------------------------------------------- #
#                       ! ADDRESS METHOD POST AND GET SERILIZER                                         #
# ---------------------------------------------------------------------------- #
class AddressSer(serializers.ModelSerializer):
    class Meta:
        model =  Address
        fields = "__all__"
        depth = 2


class AddAddressSer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "fullname",
            "phone",
            "email",
            "house",
            "trade",
            "area",
            "city",
            "pinCode",
            "delTime",
            "state",
            "upload",
        ]






# CART FOR DATA
class ProfileCartSer(serializers.ModelSerializer):
    class Meta:
        model = ProfileCart
        fields = "__all__"
        depth = 1
class CartSer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = "__all__"
        depth = 3

class AddCartSer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ["product", "quantity", "upload"]

class UpdateCartSer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = [ "quantity",]


# ===================================================== Wishlist ======================================
class ProfileWishListSer(serializers.ModelSerializer):
    class Meta:
        model = ProfileWishList
        fields = "__all__"
        depth = 1
class WishListSer(serializers.ModelSerializer):
    class Meta:
        model = WishListProduct
        fields = "__all__"
        depth = 3

class AddWishListSer(serializers.ModelSerializer):
    class Meta:
        model = WishListProduct
        fields = ["product", "quantity", "upload"]

class UpdateWishListSer(serializers.ModelSerializer):
    class Meta:
        model = WishListProduct
        fields = [ "quantity",]
# ! ==========================================End Wishlist===========================================

# ! ORDER PAGE METHOD
class AddOrderSer(serializers.ModelSerializer):
    class Meta:
        model = Order
        # fields = ['quantity','product']
        fields = [ "address",
            "transcationId",
            "upload",
            "cartUpload"]
        # depth = 2



# ! Seller Order Update
class SelOrderUpdateSer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status','selOrderStatus']


class OrderSer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        depth = 3

class OrderItemSer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"
        depth=3
    

class NotificationSer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        depth = 1



class AddNotificationSer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["sender","recevier","msg","title"]
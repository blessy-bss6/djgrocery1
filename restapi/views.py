from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate,login,logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, permissions
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from .serializers import *  
from .models import * 
from .renders import *
from .helpers import send_otp_to_phone 
from django.db.models import Q


# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


class ProductView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSer

# @api_view(["GET"])
# def cartItemInProduct():

#     prod=


#      return Response(
#                 {   'success':1,  
                   
#                      'msg':'Registration Successful' }, status=status.HTTP_201_CREATED
#                 )


# class ProductView(APIView):
#     def get(self, request):
#         prod = Product.objects.all()
#         usrCart = CartProduct.objects.filter(upload=request.user.id) 
#         # serializer = ProductSer(prod, many=True)
#         #     alldata =  {"data":serializer.data,  'success':1, }
      
#         # print(usrCart)
#         # if request.user.is_authenticated:
#         #     for i in usrCart:
#         #        print(i)
        
        
#         try:
#             ser = ProductSer(prod, many=True)
#             alldata =  {"data":ser.data,  'success':1, }
            

#         except:
           
#             alldata = {"data": ser.errors, 'success': 0, }
#         return Response(alldata)
    

class CusView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CusSer

class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySer


# ! Register View 
class RegisterView(APIView):
    def post(self, request, format=None):
        data = request.data
        if CustomUser.objects.filter(phone__exact=data.get('phone')).exists():
            return Response({"stateCode": 201,"success":0 , "msg": "User Exits"}, 201)
        
        if not MobileOtp.objects.filter(phone__exact=data.get('phone')).exists(): 
          return Response({"stateCode": 400, "success":0, "msg": "Phone Number Already Exists"}, 201)
      
        isIdType =bool(data.get("isIdType"))
        if MobileOtp.objects.get(phone__exact=data.get('phone')).is_phone_verfied ==True:
          new_user = {
            "fullname": data.get("fullname"),
            "phone": data.get("phone"),
            "email":data.get("email"),
            "password": make_password(data.get("password")),
            "is_phone_verfied":True,
            "isIdType" :isIdType
            
          }
    
        #   print(new_user)

          serializer = RegisterSer(data=new_user)
          if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.save()
            username = data.get("phone")
            raw_password = data.get("password")

            cur_user = authenticate(username=username, password=raw_password)

            #   token, _ = Token.objects.get_or_create(user=cur_user)
           

            token = get_tokens_for_user(cur_user)
            # idType= CustomUser.objects.get(id=request.user.id) 
            return Response(
                {   'success':1,  
                    'token':token,
                     'msg':'Registration Successful' ,"isIdType":isIdType}, status=status.HTTP_201_CREATED
                )
          return Response(
                { 'success':0,
                   'msg':'Verify Mobile First'},
                )
        return Response(
                { 'success':0,
                   'msg':'Verify Mobile First'},
                )
        
        
       
        

        
       

# =============================== LOGIN   =====================================
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def loginView(request):
    data=request.data
    username = data.get("phone")
    password = data.get("password")
    isIdType=bool(data.get("isIdType"))
   
    
    if not CustomUser.objects.filter(phone__exact=data.get('phone')).exists(): 
          return Response({"stateCode": 400, "success":0 ,"msg": "User is Not Existes"}, 201)
    # print(request.user.is_authenticated)
    
    if not MobileOtp.objects.filter(phone__exact=data.get('phone')).exists(): 
          return Response({"stateCode": 400,"success":0 , "msg": "Phone Verify First"}, 201)
    
    if MobileOtp.objects.get(phone__exact=data.get('phone')).is_phone_verfied ==True:
        if isIdType==True:
           
        #    " print('profile type',mat)
        #     mat.isIdType=True 
        #     mat.save() "
            user = CustomUser.objects.get(phone=username)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            mat=Profile.objects.get(id=request.user.id)
            mat.isIdType=True 
            mat.save()
        
        else:
           user = CustomUser.objects.get(phone=username)
           user.backend = 'django.contrib.auth.backends.ModelBackend'
           login(request, user)
           mat=Profile.objects.get(id=request.user.id)
           mat.isIdType= False 
           mat.save()
    else:
      user = authenticate(username=username, password=password)

   
    if not user:
        return Response({   'success':0,"error": "Invalid Credentials"},)
   
    if user is not None:
      token = get_tokens_for_user(user)
      idType= Profile.objects.get(id=request.user.id) 
      return Response({   'success':1, 'token':token, 'msg':'Login Success', 'isIdType':idType.isIdType}, status=status.HTTP_200_OK)
    else:
      return Response({   'success':0 ,'msg':'Email or Password is not Valid'}, status=status.HTTP_404_NOT_FOUND)
    

# ! Profile 
class ProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    # print(request.user.seller)
    # cat=ProfileSeller.objects.get(pk=request.user.id).exists()
    # print(cat)
   
    profile = Profile.objects.filter(upload=request.user)
    try:
            serializer = ProfileSer(profile, many=True)
            alldata =  {"data":serializer.data,  'success':1, }

    except:
           
            alldata = {"data": ser.errors,  'success':0}
    return Response( alldata ,status=status.HTTP_200_OK)
    

  def post(self,request,format=None):
        
        serializer=ProfileSer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fullname = serializer.data.get('fullname')
        gender = serializer.data.get('gender')
        
        pic=request.data.get('pic')
   
        # print(pic)
        # if pic is not None:
            
        #     mat = Profile.objects.update_or_create(id=request.user.id,upload= request.user, defaults={'fullname':fullname,'gender':gender,'pic':pic})
       
        # else:
        #     cus=Profile.objects.get(upload=request.user)
         
        #     mat = Profile.objects.update_or_create(id=request.user.id,upload=request.user, defaults={'fullname':fullname,'gender':gender,'pic':cus.pic})
        Profile.objects.update_or_create(id=request.user.id,upload=request.user, defaults={'fullname':fullname,'gender':gender,'pic':cus.pic if pic==None else pic })
        
        profile = Profile.objects.filter(upload=request.user)
        ser = ProfileSer(profile, many=True)

        return Response( {"data":ser.data,  'success':1, }, status=status.HTTP_200_OK)



# ! ADDRESS View 
# ---------------------------------------------------------------------------- #
#                   ! ADDRESS POST & GET  METHOD                                     #
# ---------------------------------------------------------------------------- #
class AddressView(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    # todo  GET METHOD
    def get(self, request):
        usr = request.user.id
        addres = Address.objects.filter(upload=usr)
        

        try:

            ser = AddressSer(addres, many=True)
            alldata =  {"data":ser.data,  'success':1, }

        except:
            alldata = {"data": ser.errors ,'success': 0,}

        return Response(alldata)

    # orc Address POST METHOD

    def post(self, request, pk=None):
        data = request.data
        usr = str(request.user.id)
        # usr =data.get("uplod")
       

        new_addres = {
            "fullname": data.get("fullname"),
            "phone": data.get("phone"),
            "email": data.get("email"),
            "house": data.get("house"),
            "trade": data.get("trade"),
            "area": data.get("area"),
            "city": data.get("city"),
            "pinCode": data.get("pinCode"),
            "delTime": data.get("delTime"),
            "state": data.get("state"),
            "upload": usr,
        }

        # print(new_addres)
        serializer = AddAddressSer(data=new_addres)

        # print(serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.save()
            return Response(
                {  'success':1,
                    "stateCode": 200,
                    "msg": "enter data",
                }
            )
        return Response({"data": serializer.errors, 'success': 0,}, status=HTTP_400_BAD_REQUEST)

    # orc Update Adress
    def put(self, request, pk=None):
        data = request.data
        idt =data.get("id")
        usr=request.user.id
        print(idt) 

        if idt ==None:
            return Response(
                {   'success':0,
                    "stateCode": 404,
                    "msg": "Address Id Not Found",
                }
            )

        
        cus = Address.objects.get(pk=idt)
        new_address = {
            "fullname": data.get("fullname"),
            "phone": data.get("phone"),
            "email": data.get("email"),
            "house": data.get("house"),
            "trade": data.get("trade"),
            "area": data.get("area"),
            "city": data.get("city"),
            "pinCode": data.get("pinCode"),
            "delTime": data.get("delTime"),
            "state": data.get("state"),
            "upload": usr
            
        }

        # print(new_profile)
        serializer = AddAddressSer(cus, data=new_address)

        # print(serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.save()
            return Response(
                {   'success':1,
                    "stateCode": 200,
                    "msg": "enter data",
                }
            )
        return Response({ "data": serializer.errors,'success': 0, }, status=HTTP_400_BAD_REQUEST)
    
    # ! Delete 
    def delete(self, request,pk=None):
        idt = request.data.get("id")

        try:
            if Address.objects.filter(pk=idt).exists():
                adr = Address.objects.filter(pk=idt)
              
                adr.delete()
                res = {'success':1   ,"msg": "data delete"}
            else:
                res = {'success': 0,"msg": " not have any data"}

        except:
            res = {'success': 0,}
        return Response(res)





    
# ---------------------------------------------------------------------------- #
#                                 ! CART METHOD                                 #
# ---------------------------------------------------------------------------- #
class CartView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    # ! get cart data 
 
    def get(self, request):
        data = request.data
        # usr = request.user
        
        
        usrCart = CartProduct.objects.filter(upload=request.user.id)
        cartProf= ProfileCart.objects.filter(upload=request.user.id)
      
        # print(usrCart)
        try:
            ser = CartSer(usrCart,many=True)
            profSer= ProfileCartSer(cartProf, many=True)
            # print(profSer)d
            alldata =  {"data":ser.data, "priceData":profSer.data , 'success':1, }
            

        except:
           
            alldata = {"data": ser.errors, 'success': 0, }
        return Response(alldata)
    
    
    # orc PROFILE POST METHOD

    def post(self, request):
        data = request.data

        # usr= data.get("customerCart")
       
        newCart = {
            # "quantity": data.get("quantity"),
            "quantity":1,
            "product": data.get("product"),
            "upload": str(request.user.id),
            
        }
    

        if CartProduct.objects.filter(
            Q(upload__exact=request.user.id)
            & Q(product__exact=data.get("product"))
        ):
            return Response({  'success':0  ,"stateCode": 201, "msg": "Product Allready Exits"}, 201)
        
        serializer = AddCartSer(data=newCart)
        
      
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.save()
            # ! show the data in Post 
            usrCart = CartProduct.objects.filter(upload=request.user.id)
            cartProf= ProfileCart.objects.filter(upload=request.user.id)
            ser = CartSer(usrCart,many=True)
            profSer= ProfileCartSer(cartProf, many=True)
            return Response(
                {   'success':1,
                    "stateCode": 200,
                    "msg": "Add Product in Cart",
                    "data":ser.data, "priceData":profSer.data ,
                }
            )
        return Response( { "data": serializer.errors, 'success': 0, } ,status=HTTP_400_BAD_REQUEST)

    # orc QUANTITY UPDATE 
    def put(self, request, pk=None):
        data = request.data
        idt = request.data.get("id")
        cus = CartProduct.objects.get(pk=idt)

        usrCart = CartProduct.objects.filter(upload=request.user.id)
        cartProf= ProfileCart.objects.filter(upload=request.user.id)
        
        new_cartu = {
            "quantity": data.get("quantity"),
        }
        serializer = UpdateCartSer(cus, data=new_cartu)

      

      
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.save()
            ser = CartSer(usrCart,many=True)
            profSer= ProfileCartSer(cartProf, many=True)
            return Response(
                {   'success':1, 
                    "stateCode": 200,
                    "msg": "Add Product in Cart", "data":ser.data, "priceData":profSer.data ,
                }
            )
        return Response( {"data": serializer.errors,'success': 0, } ,status=HTTP_400_BAD_REQUEST)
    


    def delete(self, request,pk=None):
        idt= request.data.get("id") 
        cus = CartProduct.objects.get(pk=idt)
        print(cus)
        if CartProduct.objects.filter(pk=idt).exists():
                card = CartProduct.objects.get(pk=idt)
                
                card.delete()
                usrCart = CartProduct.objects.filter(upload=request.user.id)
                cartProf= ProfileCart.objects.filter(upload=request.user.id)
                ser = CartSer(usrCart,many=True)
                profSer= ProfileCartSer(cartProf, many=True)
                return Response(
                  {   'success':1,
                    "stateCode": 200,
                    "msg": "Cart Item Delete",
                    "data":ser.data, "priceData":profSer.data ,
                  }
                )
                # res = {  'success':1, "msg": "data delete"}
                # return Response(res)
        
        else:
            res = {'success': 0, "msg": " not have any data"}
        return Response(res)



# !======================================================== WISHLIST =====================================================
class WishListView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    # ! get cart data 
 
    def get(self, request):
        data = request.data
        # usr = request.user
        
        
        usrCart = WishListProduct.objects.filter(upload=request.user.id)
        cartProf= ProfileWishList.objects.filter(upload=request.user.id)
      
        # print(usrCart)
        try:
            ser = WishListSer(usrCart,many=True)
            profSer= ProfileWishListSer(cartProf, many=True)
            # print(profSer)d
            alldata =  {"data":ser.data, "priceData":profSer.data , 'success':1, }
            

        except:
           
            alldata = {"data": ser.errors, 'success': 0, }
        return Response(alldata)
    
    
    # orc PROFILE POST METHOD

    def post(self, request):
        data = request.data
        # usr = str(request.user.id) 
        # usr= data.get("customerCart")
       
        newdata = {
            "quantity":1,
            "product": data.get("product"),
            "upload": str(request.user.id),
            
        }
    

        if WishListProduct.objects.filter(
            Q(upload__exact=request.user.id)
            & Q(product__exact=data.get("product"))
        ):
            return Response({  'success':0  ,"stateCode": 201, "msg": "Product Already Exits"}, 201)
        
        serializer = AddWishListSer(data=newdata)
        
      
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.save()
            return Response(
                {   'success':1,
                    "stateCode": 200,
                    "msg": "Add Product in WishList",
                }
            )
        # return Response( { "data": serializer.errors, 'success': 0, } ,status=HTTP_400_BAD_REQUEST)
        return Response( { "data": serializer.errors, 'success': 0, } ,401)

    # orc QUANTITY UPDATE 
    def put(self, request, pk=None):
        # data = request.data
        # idt = request.data.get("id")
        # cus = WishListProduct.objects.get(pk=idt)
        
        # new_cartu = {
        #     "quantity": data.get("quantity"),
        # }
        # serializer = UpdateWishListSer(cus, data=new_cartu)
        if CartProduct.objects.filter(
            Q(upload__exact=request.user)
            & Q(product__exact=data.get("product"))
        ):
            return Response({  'success':0  ,"stateCode": 201, "msg": "Product Allready Exits"}, 201)
      
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.save()
            return Response(
                {   'success':1, 
                    "stateCode": 200,
                    "msg": "enter data",
                }
            )
        return Response( {"data": serializer.errors,'success': 0, } ,status=HTTP_400_BAD_REQUEST)
    


    def delete(self, request,pk=None):
        idt= request.data.get("id") 
        cus = WishListProduct.objects.get(pk=idt)
        # print(cus)
        if CartProduct.objects.filter(Q(upload__exact=request.user) & Q(product__exact=cus.product.id )):
                usrCart = WishListProduct.objects.filter(upload=request.user.id)
                ser = WishListSer(usrCart,many=True)
                return Response({ "data":ser.data, 'success':1,"stateCode": 200, "msg": "Product Already Exits"},201)
        if WishListProduct.objects.filter(pk=idt).exists():
                card = WishListProduct.objects.get(pk=idt)
                card.delete()

                usrCart = WishListProduct.objects.filter(upload=request.user.id)
                ser = WishListSer(usrCart,many=True)
                res = { "data":ser.data, 'success':1, "msg": "data delete"}
                return Response(res)
        
        else:
            res = {'success': 0, "msg": " not have any data"}
        return Response(res)





# ---------------------------------------------------------------------------- #
#                                 ! ORDER PAGE                                 #
# ---------------------------------------------------------------------------- #
class OrderView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    # !  ORDER REQUEST DATA
    def post(self, request):
        data = request.data
        cart=CartProduct.objects.filter(upload=request.user.id)
        cartProf =ProfileCart.objects.filter(upload= request.user.id)
        print(cart)

        # while True:
        #     new_order = {
        #         "product": i.product.id,
        #         "address": data.get("address"),
        #         "quantity": i.quantity,
        #         "customer": request.user.id,
        #         "seller": i.product.upload.id  }

        
        # for i in cart:
            # new_order = {
            #     "product": i.product.id,
            #     "address": data.get("address"),
            #     "quantity": i.quantity,
            #     "customer": request.user.id,
            #     "seller": i.product.upload.id  }
            
            # print(new_order)
            
        print(cartProf)
        # print(cartProf)
        print(cart.length)
            # serializer = AddOrderSer(data=new_order)
            
            # if serializer.is_valid(raise_exception=True):
            #     serializer.save()
            #     user = serializer.save()
            #     return Response(
            #         { 'success':1, 
            #         "stateCode": 200,
            #         "msg": "enter data",
            #         }
            #     )
        return Response( {   'success': 0,"data" :serializer.errors, } )

        # return Response('Order Wrong', )

    # ! CURRENT ORDER data
    def get(self, request):
        usr = request.user
      

        order =Order.objects.filter(customer=usr.id)
        # print(order)

        try:
            ser = OrderSer(order, many=True)
            alldata = {"data":ser.data,  'success':1, }
            # print(alldata)

        except:
            alldata = ser.errors

        return Response(alldata)
    

    def delete(self, request,pk=None):
        idt= request.data.get("id") 
        cus = Order.objects.get(pk=idt)
        print(cus)
        if Order.objects.filter(pk=idt).exists():
                card = Order.objects.get(pk=idt)
                OrderCancel.objects.create()
                card.delete()
                res = {  'success':1, "msg": " data delete"}
                return Response(res)
        
        else:
            res = {'success': 0, "msg": " not have any data"}
        return Response(res) 





class NotificationView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usr=request.user
     
        noti=Notification.objects.filter(recevier=usr)
        
       

        try:
            ser = NotificationSer(noti, many=True)
            alldata = {"data":ser.data,  'success':1, }
            # print(alldata)

        except:
            alldata = {"data": ser.errors ,'success': 0,}

        return Response(alldata)
    
    def post(self, request, pk=None):
        data = request.data
       
       

        noti_data = {
            "sender": request.user.id,
            "recevier": data.get("recevier"),
            "msg":data.get("msg"),
            "title":data.get("title")
        }

      
        serializer = AddNotificationSer(data=noti_data)

        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.save()
            return Response(
                {  'success':1, 
                    "stateCode": 200,
                    "msg": "enter data",
                }
            )
        return Response({ "data" : serializer.errors, 'success': 0,} ,status=HTTP_400_BAD_REQUEST)


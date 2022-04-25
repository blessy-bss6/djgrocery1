from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
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

from django.db.models import Q




# Product Seller
class SelProductView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    # todo  GET METHOD
    def get(self, request):
    
        prod = Product.objects.filter(upload=request.user)
        

        try:

            ser = ProductSer(prod, many=True)
            alldata = {"data":ser.data,  'success':1, }

        except:
            alldata = { "data" : ser.errors , 'success': 0}

        return Response(alldata)

    # orc Address POST METHOD

    def post(self, request, pk=None):
        data = request.data
        usr = str(request.user.id)
        # usr =data.get("uplod")
       

        new_prod = {
            "title": data.get("title"),
            "description": data.get("description"),
            "salesPrice": data.get("salesPrice"),
            "discountPrice": data.get("discountPrice"),
            "stock": data.get("stock"),
            "pic": data.get("pic"),
            "pic1": data.get("pic1"),
            "pic2": data.get("pic2"),
            "pic3": data.get("pic3"),
            "category": data.get("category"),
            "offers": data.get("offers"),
            "upload": usr,
        }

        # print(new_addres)
        serializer = AddProductSer(data=new_prod)

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
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    # orc Update Adress
    def put(self, request, pk=None):
        data = request.data
        idt =data.get("id")
        usr=request.user.id

        # pic= None
        # pic1 =None
        # pic2= None
        # pic3= None
        
        pic= data.get("pic")
        pic1 = data.get("pic1")
        pic2= data.get("pic2")
        pic3= data.get("pic3")

        # pic1 = request.FILES['pic1']

                
        print(pic)
        print(pic1)
        print(pic2)
        print(pic3)
        
        cus = Product.objects.get(pk=idt)
        new_prod = {
            "title": data.get("title"),
            "description": data.get("description"),
            "salesPrice": data.get("salesPrice"),
            "discountPrice": data.get("discountPrice"),
            "stock": data.get("stock"),
            "category": data.get("category"),
            "offers": data.get("offers"),
            "upload": usr,
        }


        serializer = AddProductSer(cus, data=new_prod) 
        serializer.is_valid(raise_exception=True)

        print('idt')
        Product.objects.update_or_create(id=idt,upload=usr, defaults= {
            "title": data.get("title"),
            "description": data.get("description"),
            "salesPrice": data.get("salesPrice"),
            "discountPrice": data.get("discountPrice"),
            "stock": data.get("stock"),
            "category": data.get("category"),
            "offers": data.get("offers"), 
            "pic":cus.pic if pic ==None else pic ,"pic1":cus.pic1  if pic1 ==None else pic1,"pic2":cus.pic2 if pic2 ==None else pic2  ,"pic3":cus.pic3 if pic3 ==None else pic3 
            })  
       
        
        # prod = Product.objects.filter(upload=request.user)
        # ser = ProductSer(prod, many=True)
        return Response(
                {   'success':1,
                    "stateCode": 200,
                    "msg": "Enter  data",
                    #  "data":ser.data
                }
            )
        
       
    # ! Delete 
    def delete(self, request,pk=None):
        idt = request.data.get("id")

        try:
            if Product.objects.filter(pk=idt).exists():
                prd = Product.objects.filter(pk=idt)
              
                prd.delete()
                prod2 = Product.objects.filter(upload=request.user)
                ser = ProductSer(prod2, many=True)
                res = {   'success':1 , "msg": " product delete" ,   "data":ser.data}
            else:
                res = {'success': 0, "msg": " not have any data"}

        except:
            res = {"error": True ,'success':0, }
        return Response(res)



#  Order View 
class SelOrderView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    
    # ! CURRENT ORDER data
    def get(self, request):
        usr = request.user
        order =Order.objects.filter(seller=request.user.id)
        try:
           ser = OrderSer(order, many=True)
           alldata = ser.data
            # print(alldata)
        except:
            alldata = ser.errors

        return Response(alldata)

    
    def put(self, request,pk=None):
        data = request.data
        idt = data.get("id")
        cus = Order.objects.get(pk=idt)
       
        usr=request.user
        new_order = {
            "status":"Accept",
            "selOrderStatus":data.get("selOrderStatus")
        }
     
        if data.get("status")=="Decline":
            OrderCancel.objects.create(id=cus.id,cancelby="seller")
            Notification.objects.create(sender=cus.seller.upload, recevier=cus.customer.upload,msg="Order Cancel By User")
            cus.delete()
            res = {'success':1, "msg": " data delete"}
            return Response(res)
            
        else: 
            serializer = SelOrderUpdateSer(cus,data=new_order)
            
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                user = serializer.save()
                Notification.objects.create(sender=cus.seller.upload, recevier=cus.customer.upload,msg=data.get("selOrderStatus"))
                return Response(
                    { 'success':1, 
                    "stateCode": 200,
                    "msg": "enter data",
                    }
                )
        return Response( {"data":serializer.errors,  'success':0, })
    

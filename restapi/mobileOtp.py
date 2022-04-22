from .helpers import send_otp_to_phone 
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from .models import CustomUser,MobileOtp
import re

@api_view(['POST'])
def send_otp(request):
    data =request.data 
    if data.get('phone') is None and data.get('password') is None:
        return Response({
            'status':400,
            'msg':'Field required',"success":0,
        })
    regex= "^[7-9][0-9]{9}$"
    # Compile the ReGex
    p = re.compile(regex)

    
    if re.fullmatch(p,data.get('phone')) : 
       otp=send_otp_to_phone(data.get('phone'))
       MobileOtp.objects.update_or_create(phone=str(data.get('phone')), 
       defaults={'otp':str(otp) ,'is_phone_verfied':False}) 
       return Response({
        'status':200,'msg':'Otp Sent In Mobile Number', "success":1,
        'Otp':otp
        })
    else:
       return Response({
        'status':400,'msg':'Please valid Indian Mobile Number', "success":0,
        
       })


    

    
#  Verfiy Otp   
   
     
@api_view(['POST'])
def verfiy_otp(request):
    data=request.data
    regex= "^[7-9][0-9]{9}$"
    # Compile the ReGex
    p = re.compile(regex)
    if data.get('phone') is None and re.fullmatch(p,data.get('phone')) :
        return Response({"success":0,
            'status':400,
            'msg':'Field required'
        }) 
    
    if data.get('otp') is None:
        return Response({"success":0,
            'status':400,
            'msg':'Otp Invalid'
        })
    try: 
      user= MobileOtp.objects.get(phone=data.get('phone'))
    #   print(user)
    #   print(user.otp)
    
    except Exception as e:
        return Response({
            'status':400,"success":0,
            'msg':'Phone is Not exitsts',
            'otpvalid':False
        })
    
    if user.otp == data.get('otp'):
        user.is_phone_verfied =True 
        user.save()
        return Response({
            'status':200,"success":1,
            'msg':'Otp Successful',
            'otpvalid':user.is_phone_verfied

        })
    return Response({
            'status':400,"success":0,
            'msg':'Invalid Otp'
        })
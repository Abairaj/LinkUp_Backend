from rest_framework import status
from rest_framework.generics import GenericAPIView,ListAPIView,CreateAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .serializers import UserRegisterSerializer,UserLoginSerializer
from django.contrib.auth import authenticate,login,logout
from .models import user



class UserRegistrationAPIView(CreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = UserRegisterSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            User = serializer.save()
            if User:
                message = {'message':"User registered successfully"}
                return Response(message,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginAPIView(TokenObtainPairView):

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response =  super(UserLoginAPIView,self).post(request, *args, **kwargs)
        token = response.data.get("access")
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            User = authenticate(email=request.data['email'],password=request.data["password"])
            if User is not None:
                login(request,User)
                return Response({'token':token,'id':User.pk},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
     
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


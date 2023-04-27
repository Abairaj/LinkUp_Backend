from rest_framework import status
from django.http import Http404
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserProfileSerializer
from django.contrib.auth import authenticate, login, logout
from .models import user


class UserRegistrationAPIView(CreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            User = serializer.save()
            if User:
                message = {'message': "User registered successfully"}
                return Response(message, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(TokenObtainPairView):

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super(UserLoginAPIView, self).post(request, *args, **kwargs)
        token = response.data.get("access")

        email = request.data['email']
        password = request.data['password']
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            if user.objects.filter(email=email).first():
                User = authenticate(
                    email=request.data['email'], password=request.data["password"])
            else:
                return Response({"message": "Email is already registerd"}, status=status.HTTP_400_BAD_REQUEST)
            if User is not None:
                login(request, User)
                return Response({'token': token, 'id': User.pk}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': ['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return user.objects.get(pk=pk)
        except user.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        User = self.get_object(pk)
        if User:
            serializer = UserProfileSerializer(User)
            return Response({"user": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        User = self.get_object(pk)
        if User:
            serializer = UserProfileSerializer(data=request.data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': "User details updated successfully"}, status=status.HTTP_200_OK)
            else:
                print(serializer.errors)

                return Response({'message': 'User update Failed'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

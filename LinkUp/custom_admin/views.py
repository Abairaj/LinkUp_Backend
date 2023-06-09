from django.shortcuts import render
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import AdminLoginSerializer, UserListSerializer
from django.contrib.auth import authenticate, login, logout
from users.models import user
from .helper import IsAdmin

class AdminLoginAPIView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super(AdminLoginAPIView, self).post(
            request, *args, **kwargs)
        token = response.data.get("access")

        email = request.data['email']
        password = request.data['password']
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            User = authenticate(email=email, password=password)
            if User is not None and User.is_superuser:
                login(request, User)
                return Response({'token': token, 'id': User.pk}, status=status.HTTP_200_OK)
            else:
                return Response({'error': "password or email not valid"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminUsersAPIView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        try:
            User = user.objects.all().filter(is_superuser=False)
            serializer = UserListSerializer(User, many=True)
        except user.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, user_id):
        try:
            User = user.objects.get(id=user_id)
            print(request.data['is_banned'])

        except user.DoesNotExist:
            return Response({"error":"user does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if User:
            serializer = UserListSerializer(instance=User,data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                if User.is_banned == True:
                    return Response({'message':"user banned successfully"})
                elif User.is_banned == False:
                    return Response({'message':"user unbanned successfully"})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

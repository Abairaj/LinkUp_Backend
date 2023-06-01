from rest_framework import status
from django.http import Http404
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserUnfollowSerializer,
    UserFollowSerializer
)
from django.contrib.auth import authenticate, login, logout
from .models import user
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope


class AuthCheckAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            User = user.objects.get(pk=id)
            print("authentication checked")
        except user.DoesnotExist:
            print('user does not exist')

        if User:
            serializer = UserProfileSerializer(User)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        email = request.data['email']
        username = request.data['username']
        full_name = request.data['full_name']
        print(full_name)

        if user.objects.filter(email=email).exists():
            return Response({"message": "Email already exist"}, status=status.HTTP_403_FORBIDDEN)
        elif user.objects.filter(username=username).exists():
            return Response({"message": "Username already exist"}, status=status.HTTP_403_FORBIDDEN)

        if serializer.is_valid():
            User = serializer.save()
            if User:
                message = {'message': "User registered successfully"}
                return Response(message, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
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
            User = authenticate(
                email=email, password=password)

            if User.is_banned:
                return Response({'message': "USER BANNED BY ADMIN"}, status=status.HTTP_403_FORBIDDEN)
            if User is not None and User.is_banned == False:
                login(request, User)
                user = UserProfileSerializer(User)
                return Response({'token': token, 'id': User.pk, 'user': user.data}, status=status.HTTP_200_OK)
            else:
                return Response({'error': "password or email not valid"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return user.objects.get(pk=pk)
        except user.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        User = self.get_object(pk)
        if User:
            serializer = UserProfileSerializer(User)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        User = self.get_object(pk)
        if User:
            serializer = UserProfileSerializer(
                instance=User, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            else:
                print(serializer.errors)
        else:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)


class UserFollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        print(user_id,'lllllllllllll')
        print(request.data.get("user_id"),'ddddddddddddddd')
        serializer = UserFollowSerializer(data=request.data)
        if serializer.is_valid():
            user_to_follow = serializer.validated_data['user_id']
            try:
                authenticated_user = user.objects.get(id=user_id)
            except user.DoesNotExist:
                return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)


            if authenticated_user in user_to_follow.followers.all():
                user_to_follow.followers.remove(user_id)
                authenticated_user.following.remove(user_to_follow)
                return Response({"message": "User unfollowed successfully"}, status=status.HTTP_201_CREATED)
            else:
                user_to_follow.followers.add(user_id)
                authenticated_user.following.add(user_to_follow)
                serializer = UserProfileSerializer(user_to_follow, many=True)
                return Response({"message": "User followed successfully"}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)




class UserSearchView(APIView):
    # permission_classes=[IsAuthenticated]
    def get(self, request):
        key = request.GET.get("key")
        if key:
            print(key, '///////////////')
            try:
                usr = user.objects.filter(username__startswith=key)
                print(key)
                print(usr, '////////////////////')
                serializer = UserProfileSerializer(instance=usr, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                print('no user')
                return Response({"message": "data not found"}, status=status.HTTP_404_NOT_FOUND)


class UserSuggestionView(APIView):
    def get(self, request):
        try:
            usr = user.objects.filter(is_superuser=False).all()
        except:
            print("no users")

        if usr:
            serializer = UserProfileSerializer(instance=usr, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "no userdata available"}, status=status.HTTP_404_NOT_FOUND)


class LogoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': "successfully logged out."}, status=status.HTTP_200_OK)

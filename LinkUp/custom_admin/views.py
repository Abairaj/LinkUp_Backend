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
from post.models import Post
from .helper import IsAdmin
from datetime import datetime, timedelta
from django.db.models import Count
from django.db.models.functions import TruncDay


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
    # permission_classes = [IsAdmin]

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





class AdminDashboardData(APIView):
    def get(self, request):
        today = datetime.now().date()
        start_date = today - timedelta(days=30)  # Retrieve data for the last 30 days

        user_count = user.objects.exclude(is_superuser=True).count()

        user_per_day = user.objects.annotate(day=TruncDay('created_at')).filter(created_at__date__gte=start_date).values('day').annotate(registrations=Count('id')).values('day', 'registrations').order_by('day')

        post_count = Post.objects.all().count()

        delete_post_count = Post.objects.filter(deleted=True).count()

        user_per_day_data = []
        for item in user_per_day:
            day = item['day'].strftime('%Y-%m-%d')
            registrations = item['registrations']
            user_per_day_data.append({'day': day, 'registrations': registrations})

        return Response(data={"user_count": user_count, "user_per_day": user_per_day_data,'post_count':post_count,'deleted_post_count':delete_post_count})
    

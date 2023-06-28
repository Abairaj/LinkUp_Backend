from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReportSerializer, CreateReportSerializer
from .models import Report
from post.models import Post
from datetime import datetime
from django.core.mail import send_mail
from django.core.paginator import Paginator
from .task import send_email
from django.db.models import Q


class ReportAPIView(APIView):
    def get(self, request):
        search_key = request.GET.get('key')
        page = int(request.GET.get('page', 1))
        per_page = 3

        # Apply search filter if search_key is provided
        if search_key:
            print('search key is there..........')
            reports = Report.objects.filter(
                reason__icontains=search_key
            ).exclude(resolved=True)
        else:
            reports = Report.objects.exclude(resolved=True)

        paginator = Paginator(reports, per_page)

        paginated_reports = paginator.get_page(page)

        serializer = ReportSerializer(paginated_reports, many=True)


        response_data = {
            'results': serializer.data,
            'total_pages': paginator.num_pages
        }

        return Response(response_data, status=status.HTTP_200_OK)


class DeletePost_Action(APIView):
    def patch(self, request, post_id):
        try:
            post = Post.objects.get(post_id=post_id)
        except Post.DoesNotExist:
            return Response({"message": "post does not exist"}, status=status.HTTP_404_NOT_FOUND)
        post.deleted = True
        post.save()
        subject = 'LinkUp Post Deleted Due to Policy Violations'
        message = f'Dear user your post with postid {post_id} has been removed by the Admin due to the violation of the polices'
        sender_mail = 'arkclickscm@gmail.com'
        reciever_mail = post.user.email
        send_email.delay(subject, message, sender_mail, reciever_mail)
        return Response(status=status.HTTP_304_NOT_MODIFIED)

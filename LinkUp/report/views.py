from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReportSerializer, CreateReportSerializer
from .models import Report
from post.models import Post
from datetime import datetime
from django.core.mail import send_mail
from .task import send_email


class ReportAPIVIEW(APIView):
    def get(self, request):
        search_key = request.GET.get('key')
        page = int(request.GET.get('page', 1))
        per_page = 10

        # Apply search filter if search_key is provided
        if search_key:
            report = Report.objects.filter(
                Q(reporting_user__username__icontains=search_key) |
                Q(reported_user__username__icontains=search_key)
            ).exclude(resolved=True)
        else:
            report = Report.objects.exclude(resolved=True)

        total_reports = report.count()
        offset = (page - 1) * per_page
        limit = page * per_page

        report = report.select_related(
            'reporting_user', 'reported_user').all()[offset:limit]
        serializer = ReportSerializer(report, many=True)

        response_data = {
            'results': serializer.data,
            'total_pages': (total_reports + per_page - 1) // per_page
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


class SearchReportApiView(APIView):
    def get(self, request):
        key = request.GET.get('key')
        print(key, 'kkkkkkkkkkkkk')
        reports = Report.objects.filter(reason__startswith=key)
        serializer = CreateReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

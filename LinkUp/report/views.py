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
        report = Report.objects.exclude(resolved=True).select_related(
            'reporting_user').select_related('reported_user').all()
        serializer = ReportSerializer(report, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data)
        serializer = CreateReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Report created"}, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        report_id = request.data.get('report_id')
        try:
            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            return Response({'message': "report does not exist"}, status=status.HTTP_404_NOT_FOUND)
        report.resolved = True
        report.save()
        return Response({'message': 'report resolved successfully'}, status=status.HTTP_200_OK)


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
    def get(self,request):
        key = request.GET.get('key')
        print(key,'kkkkkkkkkkkkk')
        reports = Report.objects.filter(reason__startswith=key)
        serializer = CreateReportSerializer(reports,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    
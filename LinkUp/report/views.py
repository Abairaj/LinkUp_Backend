from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReportSerializer,CreateReportSerializer
from .models import Report



class ReportAPIVIEW(APIView):

    def get(self, request):
        report = Report.objects.select_related('reporting_user').select_related('reported_user').all()
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
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def put(self,request):
        pass
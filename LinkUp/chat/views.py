from django.shortcuts import render
from .models import Message
from rest_framework.views import APIView
from .serializer import MessageSerializer
from rest_framework.response import Response
from rest_framework import status
from users.models import user
from django.db.models import Q

# Create your views here.


class MessageAccessView(APIView):
    def get(self, request, rec_id, sen_id):
        try:
            print('[[[[[[[[[[[[[[]]]]]]]]]]]]]]')
            message = Message.objects.filter(
                (Q(sender=sen_id) & Q(recipient=rec_id)) | (
                    Q(sender=rec_id) & Q(recipient=sen_id))
            ).order_by('created_at')
            print(message, 'lllllllllllllllllll')
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MessageSerializer(message, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, rec_id, sen_id):
        sender = user.objects.get(id=sen_id)
        recipient = user.objects.get(id=rec_id)
        content = 'Hi'
        Message.objects.create(
            sender=sender, recipient=recipient, content=content)
        return Response(status=status.HTTP_200_OK)

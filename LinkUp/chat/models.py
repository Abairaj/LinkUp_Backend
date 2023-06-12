from django.db import models
from users.models import user
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
# Create your models here.


class Notifications(models.Model):
    sender = models.ForeignKey(
        user, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        user, related_name='receiver', on_delete=models.CASCADE)
    notification = models.CharField(max_length=550, null=True, blank=True)
    is_seen = models.BooleanField(default=False)
    type = models.CharField(max_length=280, null=True, blank=True)

    def save(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        notification_objs = Notifications.objects.filter(is_seen=False).count()
        data = {'count': notification_objs,
                'current_notification': self.notification}
        async_to_sync(channel_layer.group_send)(
            'notification_group',
            {"type": "send_notification",
             "value": json.dumps(data)
             }
        )
        super(Notifications, self).save(*args, **kwargs)

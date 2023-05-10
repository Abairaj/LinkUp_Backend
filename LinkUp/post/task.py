from celery import shared_task
from celery import Celery
from time import sleep
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from post.models import Post

from pathlib import Path


app = Celery('task', backend='rpc://', broker='pyamqp://')


@shared_task
def process_Post(user_id, path, file_name):
    print('processing........')
    sleep(10)
    storage = FileSystemStorage()
    path_object = Path(path)

    with path_object.open(mode='rb') as file:
        pic = File(file, name=path_object.name)
        instance = Post(user=user_id, image_url=pic)
        instance.save()

    storage.delete(file_name)
    print('uploaded..........')

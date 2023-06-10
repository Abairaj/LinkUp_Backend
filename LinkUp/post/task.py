from celery import shared_task
from .helper import json_to_image,compressing_image

@shared_task
def Post_Save(media_file):
    image = json_to_image(media_file)
    compressing_image(image)
    print('image compressed .............')

from celery import shared_task
from time import sleep
from django.core.files import File
import os
from django.core.files.storage import default_storage
from .helper import compressing_image

from PIL import Image
import io
import base64


@shared_task
def Post_Save(image_data):
    print(image_data,'.......................')
    image_bytes = base64.b64decode(image_data)
    image_stream = io.BytesIO(image_bytes)
    image = Image.open(image_stream)
    
    print(image, '>>>>>>>>>>>>>>>>>>>>>>')

    # Perform any necessary operations with the image

    print('task done')
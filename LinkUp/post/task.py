from celery import shared_task
from post.models import Post
from time import sleep
import base64
from PIL import Image
import io
from django.core.files import File
import os
from .models import user
from django.core.files.storage import default_storage
from .helper import compressing_image

@shared_task
def Post_Save(file_path):
    file = default_storage.open(file_path)
    image_name = file.name
    compressed_image = compressing_image(file, image_name)
    # instance.image = compressed_image
    # instance.save() 
    print('task done')
    
       

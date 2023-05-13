# from celery import shared_task
# from celery import Celery
# from time import sleep
# from django.core.files.storage import FileSystemStorage
# from django.core.files import File
# from post.models import Post
# from rest_framework.response import Response

# from pathlib import Path



# @shared_task
# def process_Post(user_id, path, file_name):
#     print('processing........')
#     sleep(10)
#     storage = FileSystemStorage()
#     path_object = Path(path)

#     with path_object.open(mode='rb') as file:
#         pic = File(file, name=path_object.name)
#         instance = Post(user=user_id, image_url=pic)
#         instance.save()

#     storage.delete(file_name)
#     print('uploaded..........')

from rest_framework.response import Response


import os
from io import BytesIO

from celery import shared_task
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from ffmpeg import(
    _ffmpeg,
    Error as FFmpegError
)
from PIL import Image

from .models import Post
import logging
logger = logging.getLogger(__name__)

@shared_task
def compress_media(post_id, media_url,file_name):
    logger.info('..........................................',post_id,media_url)
    try:
        post = Post.objects.get(post_id=post_id)

        # Image handling
        if post.media_type == 'Image':
            image_path = file_name
            with media_url.open(mode='rb') as f:
                image_data = BytesIO(f.read())
            image = Image.open(image_data)
            image.save(image_path, quality=50, optimize=True) 


            # saving to db 

            compressed_image_url = default_storage.url(image_path) 
            print(compressed_image_url)
            post.media_url = compressed_image_url
            post.save()
            return compressed_image_url

        # Video handling
        elif post.media_type == 'Video':
            video_path = media_url
            compressed_video_path = f'{video_path}.compressed.mp4'

            try:
                _ffmpeg.input(video_path).output(
                    compressed_video_path, crf=28, preset='slow', pix_fmt='yuv420p'
                ).run(capture_stdout=True, capture_stderr=True)

                # Delete original video and save compressed
                os.remove(video_path)
                with open(compressed_video_path, 'rb') as f:
                    compressed_video_data = BytesIO(f.read())
                post.media_url.save(
                    os.path.basename(compressed_video_path),
                    content=ContentFile(compressed_video_data.getvalue())
                )
            except FFmpegError as e:
                print(f'Error compressing video{video_path}')
            finally:
                os.remove(compressed_video_path)

    except Post.DoesNotExist:
        print(f'Post {post_id} does not exist')

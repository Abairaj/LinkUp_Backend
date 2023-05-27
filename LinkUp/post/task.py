from celery import shared_task


@shared_task
def Compress_media(media_file):
    print('media uploading ...................',media_file*500)
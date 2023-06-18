from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
from moviepy.editor import VideoFileClip


import base64
import json
import tempfile

import time
import random
import string

def generate_unique_filename():
    timestamp = str(int(time.time()))  # Get the current timestamp
    random_string = ''.join(random.choices(string.ascii_lowercase, k=6))  # Generate a random string of length 6
    filename = f"{timestamp}_{random_string}.jpg"  # Combine timestamp, random string, and file extension

    return filename
save_directory = tempfile.mkdtemp()



def image_to_json(image_file):
    try:
        with open(image_file.path, 'rb') as file:
            encoded_image = base64.b64encode(file.read()).decode('utf-8')

        json_data = json.dumps({'image': encoded_image})
        return json_data
    except Exception as e:
        print(f"Error converting image to JSON: {str(e)}")
        return None



def json_to_image(json_data):
    try:
        decoded_image = base64.b64decode(json_data['image'])

        # Generate a unique file name
        file_name = generate_unique_filename()

        # Create the image path
        image_path = os.path.join(save_directory, file_name)

        # Save the image file
        with open(image_path, 'wb') as image_file:
            image_file.write(decoded_image)

        return image_path
    except Exception as e:
        print(f"Error converting JSON to image: {str(e)}")
        return None



def compressing_image(image, image_name):
    # Open the image using Pillow
    img = Image.open(image)

    # Convert the image to RGB color mode
    img = img.convert("RGB")

    # Create a BytesIO object to store the compressed image data
    img_io = BytesIO()

    # Compress and save the image in JPEG format with quality 70
    img.save(img_io, format='JPEG', quality=70, optimize=True)

    # Move the pointer to the beginning of the BytesIO stream
    img_io.seek(0)

    # Get the original image format
    image_format = image.name.split(".")[-1]

    # Create a new InMemoryUploadedFile with the compressed image data
    new_image = InMemoryUploadedFile(
        img_io,
        None,
        image_name,
        f'image/{image_format.lower()}',
        img_io.tell(),
        None
    )

    # Print a message to indicate that the image has been compressed
    print('Image compressed')

    return new_image


def compressing_videos(video_file):
    file_path = video_file.temporary_file_path()


    # Generate the output file path
    output_file = os.path.splitext(video_file.name)[0] + "_compressed.mp4"

    # Open the input video file
    clip = VideoFileClip(file_path)

    # Calculate the target width and height for a 9:16 aspect ratio
    target_width = clip.w
    target_height = target_width * 16 // 9

    # Calculate the cropping parameters
    y1 = (clip.h - target_height) // 2
    y2 = y1 + target_height

    # Crop the video
    cropped_clip = clip.crop(y1=y1, y2=y2)

    # Resize the video to the desired height for compression
    compressed_clip = cropped_clip.resize(height=720)  # Set the desired height for compression

    # Calculate the target bitrate to limit the output video size
    target_bitrate = 9000000  # 9 Mbps

    # Compress the video by reducing the bitrate and setting the output format
    compressed_clip.write_videofile(output_file, bitrate=str(target_bitrate), codec="libx264", audio_codec="aac")

    # Close the clips
    clip.close()
    cropped_clip.close()
    compressed_clip.close()

    # Return the path of the compressed video file
    return output_file


# def compressing_videos(video_file):
#     # Generate the output file path for the compressed video
#     output_file_path = os.path.splitext(video_file.name)[0] + "_compressed.mp4"
#     absolute_path = os.path.abspath(output_file_path)

#     # Open the input video file
#     clip = VideoFileClip(output_file_path)

#     # Calculate the target width and height for a 9:16 aspect ratio
#     target_width = clip.w
#     target_height = target_width * 16 // 9

#     # Calculate the cropping parameters
#     y1 = (clip.h - target_height) // 2
#     y2 = y1 + target_height

#     # Crop the video
#     cropped_clip = clip.crop(y1=y1, y2=y2)

#     # Resize the video to the desired height for compression
#     # Set the desired height for compression
#     compressed_clip = cropped_clip.resize(height=720)

#     # Calculate the target bitrate to limit the output video size
#     target_bitrate = 9000000  # 9 Mbps

#     # Compress the video by reducing the bitrate and setting the output format
#     compressed_clip.write_videofile(output_file_path, bitrate=str(
#         target_bitrate), codec="libx264", audio_codec="aac")

#     # Close the clips
#     clip.close()
#     cropped_clip.close()
#     compressed_clip.close()

#     # Return the path of the compressed video file
#     return output_file_path

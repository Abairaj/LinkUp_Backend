from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
from moviepy.editor import VideoFileClip


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
<<<<<<< HEAD
# def compressing_videos(video_file):
#     file_path = video_file.temporary_file_path()
=======

def compressing_videos(video_file):
    file_path = video_file.temporary_file_path()
>>>>>>> Chat

#     # Generate the output file path
#     output_file = os.path.splitext(video_file.name)[0] + "_compressed.mp4"

#     # Open the input video file
#     clip = VideoFileClip(file_path)

#     # Calculate the target width and height for a 9:16 aspect ratio
#     target_width = clip.w
#     target_height = target_width * 16 // 9

#     # Calculate the cropping parameters
#     y1 = (clip.h - target_height) // 2
#     y2 = y1 + target_height

#     # Crop the video
#     cropped_clip = clip.crop(y1=y1, y2=y2)

#     # Resize the video to the desired height for compression
#     compressed_clip = cropped_clip.resize(height=720)  # Set the desired height for compression

#     # Calculate the target bitrate to limit the output video size
#     target_bitrate = 9000000  # 9 Mbps

#     # Compress the video by reducing the bitrate and setting the output format
#     compressed_clip.write_videofile(output_file, bitrate=str(target_bitrate), codec="libx264", audio_codec="aac")

#     # Close the clips
#     clip.close()
#     cropped_clip.close()
#     compressed_clip.close()

#     # Return the path of the compressed video file
#     return output_file


def compressing_videos(video_file):
    # Generate the output file path for the compressed video
    output_file_path = os.path.splitext(video_file.name)[0] + "_compressed.mp4"
    absolute_path = os.path.abspath(output_file_path)

    # Open the input video file
    clip = VideoFileClip(output_file_path)

    # Calculate the target width and height for a 9:16 aspect ratio
    target_width = clip.w
    target_height = target_width * 16 // 9

    # Calculate the cropping parameters
    y1 = (clip.h - target_height) // 2
    y2 = y1 + target_height

    # Crop the video
    cropped_clip = clip.crop(y1=y1, y2=y2)

    # Resize the video to the desired height for compression
    # Set the desired height for compression
    compressed_clip = cropped_clip.resize(height=720)

    # Calculate the target bitrate to limit the output video size
    target_bitrate = 9000000  # 9 Mbps

    # Compress the video by reducing the bitrate and setting the output format
    compressed_clip.write_videofile(output_file_path, bitrate=str(
        target_bitrate), codec="libx264", audio_codec="aac")

    # Close the clips
    clip.close()
    cropped_clip.close()
    compressed_clip.close()

    # Return the path of the compressed video file
    return output_file_path

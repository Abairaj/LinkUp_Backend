from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
from moviepy.editor import VideoFileClip







def compressing_image(image, image_name):
    img = Image.open(image)

    img_io = BytesIO()
    img.save(img_io, format='JPEG', quality=70, optimize=True)
    img_io.seek(0)

    new_image = InMemoryUploadedFile(
        img_io,
        None,
        image_name,
        'image/jpeg',
        img_io.tell(),
        None
    )
    print('compressed//////////////////////////////////////////////////////')

    return new_image
def compressing_videos(video_file):
    file_path = video_file.temporary_file_path()

    # Generate the output file path
    output_file = os.path.splitext(file_path)[0] + ".mp4"
    print(output_file,'output////////////////////////////////////////////////')
    print(video_file,'videofile///////////////////////////////////////////////////////////////')
    
    # Open the input video file
    clip = VideoFileClip(video_file.path)
    
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
    target_bitrate = 9000000  # 10 Mbps
    
    # Compress the video by reducing the bitrate and setting the output format
    compressed_clip.write_videofile(output_file, bitrate="1000k", codec="libx264", audio_codec="aac")
    
    # Close the clips
    clip.close()
    cropped_clip.close()
    compressed_clip.close()
    
    # Return the path of the compressed video file
    return output_file








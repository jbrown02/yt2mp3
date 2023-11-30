# Josh Brown & Dre Owens
# Fall, 2023 - Zak Rubin
# CNE 430

# YouTube to MP3 Converter

# Convert the audio of a YouTube video to an MP3 file using an EC2 instance
# File is temporarily hosted in an S3 bucket and deleted after 5 minutes

import subprocess
import boto3
import logging
from botocore.exceptions import ClientError
import time

# Download video
def download_video(video_url, output_path):
    command = f'sudo yt-dlp -o "{output_path}" {video_url}'
    
    try:
        subprocess.run(command, shell=True, check=True)
        print("Video downloaded successfully!")

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# Convert video
def convert_video():
    command = f'sudo ffmpeg -i /home/ubuntu/served_files/video.webm -vn -ar 44100 -ac 2 -b:a 192k /home/ubuntu/served_files/audio.mp3'
    
    try:
        subprocess.run(command, shell=True, check=True)
        print("File converted successfully!")

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# Delete video
def delete_video():
    command = f'sudo rm /home/ubuntu/served_files/video.webm'
    
    try:
        subprocess.run(command, shell=True, check=True)
        print("Video file deleted")

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# Transfer audio
def transfer_audio():
    command = f'aws s3 cp /home/ubuntu/served_files/audio.mp3 s3://josh-yt2mp3/  --region us-west-2'

    try:
        subprocess.run(command, shell=True, check=True)
        print("Audio file transferred to S3 bucket")

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# The audio file should now be securely hosted in the S3 bucket
# Next, the script will create a functioning download URL

logger = logging.getLogger(__name__)

# Generate pre-signed URL
def s3_url(s3_client, client_method, method_parameters, expires_in=30):
    """
    Generate a presigned Amazon S3 URL that can be used to perform an action.

    :param s3_client: A Boto3 Amazon S3 client.
    :param client_method: The name of the client method that the URL performs.
    :param method_parameters: The parameters of the specified client method.
    :param expires_in: The number of seconds the presigned URL is valid for.
    :return: The presigned URL.
    """
    try:
        url = s3_client.generate_presigned_url(
            ClientMethod=client_method, Params=method_parameters, ExpiresIn=expires_in
        )
        logger.info("Got presigned URL: %s", url)
    except ClientError:
        logger.exception(
            "Couldn't get a presigned URL for client method '%s'.", client_method
        )
        raise
    return url

# Delete audio file from server and S3 bucket
def delete_audio():
    command = f'sudo rm /home/ubuntu/served_files/audio.mp3'
    
    try:
        time.sleep(301)
        subprocess.run(command, shell=True, check=True)
        print("5 minutes elapsed")

        # Delete the file from S3
        s3_bucket_name = "josh-yt2mp3"
        s3_key = "audio.mp3"

        s3_client = boto3.client('s3')
        s3_client.delete_object(Bucket=s3_bucket_name, Key=s3_key)
        print("Audio files deleted successfully")

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    video_url = input("Enter video URL: ")
    output_path = "/home/ubuntu/served_files/video"
    mp3_path = "/home/ubuntu/served_files/audio.mp3"
    s3_bucket_name = "josh-yt2mp3"
    s3_key = "audio.mp3"

    download_video(video_url, output_path)
    convert_video()
    delete_video()
    transfer_audio()

    s3_client = boto3.client('s3')
    method_parameters = {'Bucket': s3_bucket_name, 'Key': s3_key}
    pre_signed_url = s3_url(s3_client, 'get_object', method_parameters, expires_in=30)

    print(f"Download URL: \033[32m{pre_signed_url}")
    
    delete_audio()
    print("Conversion complete!")

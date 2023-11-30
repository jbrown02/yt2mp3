from pytube import YouTube
import boto3

# Download YT video as MP3 and upload to S3 Bucket
def download_and_upload_to_s3(youtube_url):
    yt = YouTube(youtube_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(filename='audio.mp3')
    
    s3_bucket_name = 'dreconvbucket' 
    
    # Upload the MP3 file to S3 bucket
    s3_client = boto3.client('s3')
    s3_client.upload_file('audio.mp3', s3_bucket_name, 'audio.mp3')
  
# Accepts YT URL from triggerScript.py
if __name__ == "__main__":
    youtube_url = input("Enter the YouTube URL: ")  
    
    # Download YouTube video as MP3 and upload to S3 Bucket
    download_and_upload_to_s3(youtube_url)

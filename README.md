# Youtube to MP3 converter
## Hosted on AWS

### Prerequisites:
An up-to-date Ubuntu EC2 instance

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

pip: Install Pip in order to install other dependencies.

```bash
$ sudo apt install pip
```

yt-dlp: Install YouTube downloader library for downloading videos.

```bash
$ sudo pip install yt-dlp
```

ffmpeg: Install FFmpeg for audio conversion.

```bash
sudo apt-get install ffmpeg
```

AWS CLI: Configure AWS CLI with the necessary credentials for S3 file transfer.

```bash
aws configure
```

Boto3: Install Boto3 library for AWS S3 interaction.

```bash
sudo pip install boto3
```

### Configuration:
The terminal on your native device should have pip, Python3, and paramiko installed.

- output_path: Path where the downloaded video is saved on the server.
- mp3_path: Path where the converted MP3 file is saved on the server.
- s3_bucket_name: Name of the S3 bucket where the MP3 file is transferred.
- s3_key: Key (object name) for the MP3 file in the S3 bucket.
- expires_in: Expiration time for the pre-signed URL (default is 30 seconds).

### Usage:
Run the script based on the absolute path of its location  on  your native  device:

```bash
python3 /Users/joshuabrown/Desktop/BAS/Code/yt2mp3/trigger.py
```

You can then input your YouTube video URL. After that, you will be given a download link for the MP3 file. The server will delete all data in 5 minutes.

### Notes:
- The script uses sudo in commands, so ensure that the user running the script has appropriate privileges.
- Adjust the paths, S3 bucket details, and expiration time as needed.

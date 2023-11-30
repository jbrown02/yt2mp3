import boto3

def trigger_conversion_on_ec2(ec2_instance_id, youtube_url):
    command = f"python3 /home/ubuntu/conversionScript.py {youtube_url}"
    region = 'us-west-2'

    # AWS credentials
    boto3.setup_default_session(
        aws_access_key_id='AKIARDI66FHQUOUQWOOV',
        aws_secret_access_key='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',
        region_name=region
    )
    
    ssm_client = boto3.client('ssm', region_name=region)
    response = ssm_client.send_command(
        InstanceIds=[ec2_instance_id],
        DocumentName="AWS-RunShellScript",
        Parameters={'commands': [command]}
    )
    return response

# Function to deliver S3 link
def get_s3_link(bucket_name, file_name):
    s3_client = boto3.client('s3')
    url = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket_name, 'Key': file_name},
        ExpiresIn=3600  # Link expiration time in seconds 
    )
    return url

if __name__ == "__main__":
    ec2_instance_id = 'i-0f01429ae3babf3b0'
    bucket_name = 'dreconvbucket'

    youtube_url = input("Enter the YouTube URL: ")

    # Triggers the conversion script stored on EC2 instance
    response = trigger_conversion_on_ec2(ec2_instance_id, youtube_url)
    print("Initiating Conversion Sequence...")

    # Retrieves S3 link for the uploaded MP3 file
    file_name = 'audio.mp3'
    s3_link = get_s3_link(bucket_name, file_name)
    print(f"Your File Is Ready For Download: {s3_link}")

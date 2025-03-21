import requests
import boto3
from botocore.exceptions import NoCredentialsError
from urllib.parse import urlparse
import os

def download_image(image_path_or_url):
    parsed_url = urlparse(image_path_or_url)
    
    if parsed_url.scheme in ('http', 'https'):
        # Download image from URL
        response = requests.get(image_path_or_url)
        if response.status_code == 200:
            return response.content
        else:
            raise ValueError(f"Failed to download image from URL: {image_path_or_url}")
    
    elif parsed_url.scheme == 's3':
        # Download image from S3
        s3 = boto3.client('s3')
        bucket = parsed_url.netloc
        key = parsed_url.path.lstrip('/')
        try:
            response = s3.get_object(Bucket=bucket, Key=key)
            return response['Body'].read()
        except NoCredentialsError:
            raise ValueError("AWS credentials not found.")
        except Exception as e:
            raise ValueError(f"Failed to download image from S3: {str(e)}")
    
    else:
        # Download image from local path
        if os.path.exists(image_path_or_url):
            with open(image_path_or_url, "rb") as image_file:
                return image_file.read()
        else:
            raise ValueError(f"Local file not found: {image_path_or_url}")

if __name__ == "__main__":
    image_path = input("Enter the image path or URL: ")
    try:
        image_data = download_image(image_path)
        print("Image downloaded successfully.")
    except Exception as e:
        print(f"Error: {e}")

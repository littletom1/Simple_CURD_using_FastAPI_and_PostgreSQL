import boto3
from decouple import config
from botocore.exceptions import ClientError
import logging
import os

class S3Client:
    def __init__(self):
        self.client = boto3.client(
            's3',
            aws_access_key_id = config('AWS_ACCESS_KEY'),
            aws_secret_access_key = config('AWS_SECRET_KEY'),
            region_name = config('AWS_REGION')
        )
                
    def upload_file(self, file_name, bucket, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)
        
        # Upload the file
        try:
            response = self.client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True
    def put_object(self, Body, Bucket, Key,ContentType):
        try:
            response = self.client.put_object(Body=Body, Bucket=Bucket, Key=Key, ContentType=ContentType)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    
    
            

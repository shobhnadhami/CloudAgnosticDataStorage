import boto3
import os
import zipfile
from util_function import save_zip_file, delete_folder



class AwsUtils:
    def __init__(self, aws_access_key_id, aws_secret_key, region):
        self.aws_key_id = aws_access_key_id
        self.aws_secret_key = aws_secret_key
        self.region_name = region

    def upload_file(self, bucket_name, file, s3_object_folder):
        s3 = boto3.client("s3", region_name=self.region_name, aws_access_key_id=self.aws_key_id,
        aws_secret_access_key=self.aws_secret_key)
        try:
            # s3.upload_file('C:/Users/shobhna/Documents/machine learning shobhna.pdf', bucket_name, 'machine learning shobhna.pdf')
            response = s3.upload_fileobj(
                file,
                bucket_name,
                file.filename,
                ExtraArgs={
                    "ContentType": file.content_type  # Set appropriate content type as per the file
                })
            return True, ""
        except Exception as ex:
            return False, str(ex)

    def upload_folder(self, bucket_name, file, s3_object_folder, config):
        try:
            failed_upload = {}
            s3 = boto3.client("s3", region_name=self.region_name, aws_access_key_id=self.aws_key_id,
            aws_secret_access_key=self.aws_secret_key)
            zip_file_path = config['Path']['DataPath']
            is_file_saved, saved_folder_name = save_zip_file(file, zip_file_path)
            if not is_file_saved:
                return False, saved_folder_name
            for subdir, dirs, files in os.walk(zip_file_path):
                for file in files:
                    full_path = os.path.join(subdir, file)
                    object_name = full_path.split(saved_folder_name)[1][1:].replace('\\','/')
                    try:
                        s3.upload_file(full_path, bucket_name, object_name)
                    except Exception as ex:
                        failed_upload[object_name] = str(ex)
                        continue
            delete_folder(saved_folder_name)
                    # s3.upload_file(full_path, bucket_name, object_name)
            return True, failed_upload
        except Exception as ex:
            return False, str(ex)


    def download_file(self,bucket_name, s3_object_name, saved_file_name):
        try:
            s3 = boto3.client("s3", region_name=self.region_name, aws_access_key_id=self.aws_key_id,
            aws_secret_access_key=self.aws_secret_key)
            file = s3.get_object(
                Bucket=bucket_name, Key=s3_object_name
            )
            return True, file
        except Exception as ex:
            return False, str(ex)

    def download_file(self,bucket_name, s3_object_name, saved_file_name):
        try:
            s3 = boto3.client("s3", region_name=self.region_name, aws_access_key_id=self.aws_key_id,
            aws_secret_access_key=self.aws_secret_key)
            file = s3.get_object(
                Bucket=bucket_name, Key=s3_object_name
            )
            return True, file
        except Exception as ex:
            return False, str(ex)
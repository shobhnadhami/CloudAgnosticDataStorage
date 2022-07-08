import boto3
import os
from util_function import save_zip_file, delete_folder, zip_folder



class AwsUtils:
    def __init__(self, aws_access_key_id, aws_secret_key, region):
        self.aws_key_id = aws_access_key_id
        self.aws_secret_key = aws_secret_key
        self.region_name = region

    def upload_file(self, bucket_name, file):
        s3 = boto3.client("s3", region_name=self.region_name, aws_access_key_id=self.aws_key_id,
        aws_secret_access_key=self.aws_secret_key)
        try:
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

    def upload_folder(self, bucket_name, file, config):
        try:
            failed_upload = {}
            s3 = boto3.client("s3", region_name=self.region_name, aws_access_key_id=self.aws_key_id,
            aws_secret_access_key=self.aws_secret_key)
            zip_file_path = config['PATH']['DataPath']
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

            return True, failed_upload
        except Exception as ex:
            return False, str(ex)


    def download_file(self,bucket_name, s3_object_name,config):
        try:
            download_folder = config['PATH']['DownloadPath']
            download_filename = s3_object_name.split('/')[-1]
            download_path = os.path.join(download_folder,download_filename)
            s3 = boto3.client("s3", region_name=self.region_name, aws_access_key_id=self.aws_key_id,
            aws_secret_access_key=self.aws_secret_key)
            s3.download_file(
                bucket_name, s3_object_name,download_path
            )
            return True, download_filename
        except Exception as ex:
            return False, str(ex)
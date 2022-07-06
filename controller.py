import os
import configparser
import zipfile
from aws_utils import AwsUtils

PATH = os.getcwd()
config = configparser.ConfigParser()
config.read(os.path.join(PATH, 'config.ini'))


class Controller:
    def __init__(self, instance_name):
        self.instance_name = instance_name

    def store_file(self, request_body, file):
        try:
            instance = request_body['instance']
            if instance == 'aws':
                access_key_id = config['AWS']['AccessKey']
                secret_key_id = config['AWS']['SecretKey']
                region = config['AWS']['Region']
                # access_key_id = request_body['access_key']
                # secret_key_id = request_body["secret_key"]
                # region = request_body["region"]
                bucket_name = request_body["bucket_name"]
                # s3_object_name = request_body["object_folder_name"]
                aws_util_obj = AwsUtils(access_key_id,secret_key_id, region)
                if file.content_type == 'application/zip':
                # if zipfile.is_zipfile(file.filename):
                    response, message = aws_util_obj.upload_folder(bucket_name, file,  config)
                else:
                    response, message = aws_util_obj.upload_file(bucket_name)
                if response :
                    if len(message) == 0:
                        return {'status_Code':200, 'message':'file uploaded succussfully','Reason':''}
                    return {'status_Code':400, 'message':'','Reason':'Failed to uppload following files:' + str(message)}
                return {'status_Code':400, 'message': '','Reason': message}
            return "not implemented"
        except Exception as ex:
            return {'status_Code':400, 'message': '','Reason': str(ex)}


    def retrieve_file(self, request_body):
        try:
            instance = request_body['instance']
            if instance == 'aws':
                access_key_id = request_body['access_key']
                secret_key_id = request_body["secret_key"]
                region = request_body["region"]
                bucket_name = request_body["bucket_name"]
                s3_object_name = request_body["object_name"]
                isfolder = request_body['object_is_folder']
                saved_file_name = request_body["save_file_name"]
                aws_util_obj = AwsUtils(access_key_id, secret_key_id, region)
                if not isfolder:
                    response, file = aws_util_obj.download_file(bucket_name, s3_object_name, saved_file_name)
                else:
                    response, file = aws_util_obj.download_folder(bucket_name, s3_object_name, saved_file_name)
                if response:
                    return True,file
                return False, {'status_Code': 400, 'message': '', 'Reason': str(file)}
        except Exception as ex:
            return False, {'status_Code': 400, 'message': '', 'Reason': str(ex)}
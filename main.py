from flask import Flask, jsonify, request, send_file
import configparser
import os
import io
import json
from werkzeug.utils import secure_filename
from controller import Controller
from util_function import delete_folder

app = Flask(__name__)
PATH = os.getcwd()
config = configparser.ConfigParser()
config.read(os.path.join(PATH, 'config.ini'))
host = config['DEFAULT']['Host']
port = config['DEFAULT']['Port']


@app.route('/store_file', methods=['POST'])
def store_file():
    """
    api to store file
    :return:
    """
    data_file = request.files['file']
    if data_file.filename != "":
        data_file.filename = secure_filename(data_file.filename)
        request_body_obj = dict(request.form)
        controller_obj = Controller(request_body_obj['instance'])
        response = controller_obj.store_file(request_body_obj, data_file)
        return jsonify(response)


@app.route('/retrieve_file', methods=['POST'])
def retrieve_file():
    """
    api to download file
    :return:
    """
    download_folder = config['PATH']['DownloadPath']
    request_body_obj = request.json

    controller_obj = Controller(request_body_obj['instance'])
    response_download, file_name = controller_obj.retrieve_file(request_body_obj)
    if response_download:
        file_path = download_folder + '/' + file_name
        file_data = io.BytesIO()
        with open(file_path, 'rb') as fo:
            file_data.write(fo.read())
        file_data.seek(0)
        os.remove(file_path)
        return send_file(file_data, as_attachment=True, download_name=file_name)

    return jsonify(file_name)




if __name__ == "__main__":
    app.run(host=host, port=port)
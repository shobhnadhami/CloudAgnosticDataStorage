from flask import Flask, jsonify, request, send_from_directory
import configparser
import os
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

# @app.route('/store', methods=['POST'])
# def store_file():
#     pass


@app.route('/store', methods=['POST'])
def store_file():
    data_file = request.files['file']
    if data_file.filename != "":
        data_file.filename = secure_filename(data_file.filename)
        request_body_obj = dict(request.form)
        controller_obj = Controller(request_body_obj['instance'])
        response = controller_obj.store_file(request_body_obj, data_file)
        return jsonify(response)


@app.route('/retrieve_file', methods=['POST'])
def retrieve_file():
    download_folder = config['PATH']['DownloadPath']
    request_body_obj = request.json

    controller_obj = Controller(request_body_obj['instance'])
    response_download, file_path = controller_obj.retrieve_file(request_body_obj)
    if response_download:
        return send_from_directory(download_folder, file_path,as_attachment=True)

    return jsonify(file_path)




if __name__ == "__main__":
    app.run(host=host, port=port)
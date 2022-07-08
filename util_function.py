import zipfile
import shutil
import os

def save_zip_file(file,destination):
    try:
        destination = os.path.join(destination, file.filename.split('.zip')[0])
        with zipfile.ZipFile(file) as zf:
            zf.extractall(
                destination)
        return True, destination
    except Exception as ex:
        return False, str(ex)


def delete_folder(destination):
    try:
        shutil.rmtree(destination)
        return True, "folder deleted"
    except Exception as ex:
        return False, str(ex)

def zip_folder(folder_path):
    try:
        zip_name = folder_path + '.zip'
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
            for folder_name, subfolders, filenames in os.walk(folder_path):
                for filename in filenames:
                    file_path = os.path.join(folder_name, filename)
                    zip_ref.write(file_path, arcname=os.path.relpath(file_path, folder_path))

        zip_ref.close()
        return True, zip_name
    except Exception as ex:
        return False, str(ex)
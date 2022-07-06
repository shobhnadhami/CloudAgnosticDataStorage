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
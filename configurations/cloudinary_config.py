from werkzeug.datastructures import FileStorage
import cloudinary
from cloudinary import uploader, api

from configurations.envs_config import (
    CLOUDINARY_APIKEY,
    CLOUDINARY_APISECRET,
    CLOUDINARY_CLOUDNAME,
    CLOUDINARY_FOLDER,
)

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUDNAME,
    api_key=CLOUDINARY_APIKEY,
    api_secret=CLOUDINARY_APISECRET,
    secure=True,
)


def file_uploader(image: FileStorage):
    return uploader.upload(image, folder=CLOUDINARY_FOLDER)

def get_file(public_id):
    try:
        return api.resource(public_id)
    except Exception as e:
        raise e

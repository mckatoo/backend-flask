import cloudinary
from decouple import config

cloudinary.config(
    cloud_name=config("CLOUDINARY_CLOUDNAME"),
    api_key=config("CLOUDINARY_APIKEY"),
    api_secret=config("CLOUDINARY_APISECRET"),
    secure=True,
)
folder = config("CLOUDINARY_FOLDER")

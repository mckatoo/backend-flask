from decouple import config

DEV_ENV = config("DEV_ENV", cast=bool, default=False)
SECRET_KEY = config("PRIVATE_KEY")
IMAGE_ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
CLOUDINARY_FOLDER = config("CLOUDINARY_FOLDER", cast=str, default="")
CLOUDINARY_CLOUDNAME = config("CLOUDINARY_CLOUDNAME")
CLOUDINARY_APIKEY = config("CLOUDINARY_APIKEY")
CLOUDINARY_APISECRET = config("CLOUDINARY_APISECRET")

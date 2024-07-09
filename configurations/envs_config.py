from decouple import Csv, config

DEV_ENV = config("DEV_ENV", cast=bool, default=False)
SECRET_KEY = config("PRIVATE_KEY")
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", cast=Csv())
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

IMAGE_ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
CLOUDINARY_FOLDER = config("CLOUDINARY_FOLDER", cast=str, default="")
CLOUDINARY_CLOUDNAME = config("CLOUDINARY_CLOUDNAME")
CLOUDINARY_APIKEY = config("CLOUDINARY_APIKEY")
CLOUDINARY_APISECRET = config("CLOUDINARY_APISECRET")

SMTP_SERVER_ADDRESS = config(
    "SMTP_SERVER_ADDRESS", cast=str, default="localhost"
)
SMTP_SERVER_PORT = config("SMTP_SERVER_PORT", cast=int, default=587)
SMTP_START_TLS = config("SMTP_START_TLS", cast=bool, default=True)
SMTP_USERNAME = config("SMTP_USERNAME", cast=str)
SMTP_PASSWORD = config("SMTP_PASSWORD", cast=str)
EMAIL_SUBJECT_PREFIX = config("EMAIL_SUBJECT_PREFIX", cast=str)

AUTH0_CLIENT_ID = config("AUTH0_CLIENT_ID", cast=str)
AUTH0_CLIENT_SECRET = config("AUTH0_CLIENT_SECRET", cast=str)
AUTH0_DOMAIN = config("AUTH0_DOMAIN", cast=str)

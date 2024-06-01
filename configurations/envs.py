from decouple import config

DEV_ENV = config("DEV_ENV", cast=bool, default=False)
SECRET_KEY = config("PRIVATE_KEY")
IMAGE_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

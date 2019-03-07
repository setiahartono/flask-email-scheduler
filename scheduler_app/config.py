import os

SECRET_KEY = 'dev'

BASEDIR = os.path.dirname(os.path.abspath(__file__))

# Database Settings
database_filename = "email_post.sqlite3"
database_file = "sqlite:///{}/db/{}".format(BASEDIR, database_filename)
SQLALCHEMY_DATABASE_URI = database_file

# Celery and Broker Settings, Redis example is provided
REDIS_HOST = "0.0.0.0"
REDIS_PORT = 6379
BROKER_URL = "redis://{}:{}/0".format(REDIS_HOST, REDIS_PORT)
CELERY_RESULT_BACKEND = BROKER_URL

# SMTP Settings, modify to make it work
MAIL_SERVER = 'smtp.yourserver.com'
MAIL_PORT = 465
MAIL_USERNAME = 'youremail@yourserver.com'
MAIL_PASSWORD = 'yourpassword'
MAIL_DEFAULT_SENDER = MAIL_USERNAME
MAIL_USE_TLS = False
MAIL_USE_SSL = True

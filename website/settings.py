import os 

heroku_uri = os.environ.get('DATABASE_URL')
SQLALCHEMY_DATABASE_URI = heroku_uri[:8]+'ql'+heroku_uri[8:]
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False

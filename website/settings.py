import os 

SQLALCHEMY_DATABASE_URI = 'postgresql://wbaipmlhagglvr:dc75aed2c33a809bd118910f2170bdbaf6d21f6c9158acf4fa3ad93c79a58c37@ec2-63-32-7-190.eu-west-1.compute.amazonaws.com:5432/df6t7emeu38drt'
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False

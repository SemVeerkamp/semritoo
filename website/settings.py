import os 

SQLALCHEMY_DATABASE_URI = 'postgresql://zqcwshnuvmsssb:bb31875ede38ab52448a4ea61f393a66fa4633b1523942663d3b96b7de40003f@ec2-79-125-93-182.eu-west-1.compute.amazonaws.com:5432/d2q6l6u8irtla1'
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False

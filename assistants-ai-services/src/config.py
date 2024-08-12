import os

from os.path import join, dirname
from dotenv import load_dotenv

# load the environment variables based on FLASK_ENV
PROJECT_ROOT_PATH = os.getcwd()
environment = os.getenv("FLASK_ENV")
dotenv_path = join(PROJECT_ROOT_PATH, f'.env.{environment}')
load_dotenv(dotenv_path)

class Config(object):
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')    
    APPLICATION_ROOT = "/api"
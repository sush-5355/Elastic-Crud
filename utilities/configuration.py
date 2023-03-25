import os
from elasticsearch import Elasticsearch
import warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('ELASTIC_HOSTNAME')
port = os.getenv('ELASTIC_PORT')
username = os.getenv('ELASTIC_USERNAME')
password = os.getenv('ELASTIC_PASSWORD')

url = f'https://{host}:{port}'

es = Elasticsearch([url],
                   http_auth=(username, password),
                   verify_certs=False)
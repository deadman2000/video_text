import os
from pymongo import MongoClient

url = os.environ.get('MONGO_URL', None)
if url is None:
    url = 'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@mongodb'.format(**os.environ)

client = MongoClient(url)

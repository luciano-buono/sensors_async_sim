import json
from pymongo import MongoClient

def write_to_db(topic, jsonData):

    # class pymongo.mongo_client.MongoClient(host='localhost', port=27017, document_class=dict, tz_aware=False, connect=True, **kwargs)
    client = MongoClient()
    db = client['iot-mongo']
    posts = db[topic]
    data = json.loads(jsonData)
    posts.insert_one(data)

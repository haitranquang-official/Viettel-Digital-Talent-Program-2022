from flask_mongoengine import MongoEngine

config = {
    'db': 'student',
    'host': 'localhost',
    'port': 27017
}

def get_config():
    return config
from flask_mongoengine import MongoEngine

config = {
    'db': 'student',
    'host': 'mongodb',
    'port': 27017
}

def get_config():
    return config
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ['postgres://akldbagkltqwej:9eeffab6ddd07e05fed9df47a2c61e7aeed4e6eadd76571aff26796dfe78f241@ec2-3-209-124-113.compute-1.amazonaws.com:5432/d7o8p9tmsr6jqo']

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

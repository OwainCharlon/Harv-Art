class BaseConfig(object):
    SECRET_KEY = 'abcdef123456'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MYSQL = {
        'user': 'root',
        'pw': '',
        'db': 'harvart',
        'host': 'localhost',
        'port': '3308',
    }

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % MYSQL


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True

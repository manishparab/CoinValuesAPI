from psycopg2.extras import DictCursor
from psycopg2.pool import SimpleConnectionPool
from configparser import ConfigParser

file = 'config.ini'
config = ConfigParser()
config.read(file)

pool = SimpleConnectionPool(minconn=int(config['database']['min_conn']),
                            maxconn=int(config['database']['max_conn']),
                            database=config['database']['database'],
                            user=config['database']['user'],
                            password=config['database']['password'],
                            host=config['database']['host'], cursor_factory=DictCursor)



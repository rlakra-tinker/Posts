import os

from multiprocessing import cpu_count
from dotenv import load_dotenv

load_dotenv()
# gunicorn -c webapp/gunicorn.conf.py webapp:app
default_pool_size = int(os.getenv('DEFAULT_POOL_SIZE', 1))
rds_pool_size = int(os.getenv('RDS_POOL_SIZE', 1))
rds_pool_size += default_pool_size
# validate the pool size
if (rds_pool_size - default_pool_size) < 1:
    raise Exception('Threads has to be higher that 0.')

bind = os.getenv('HOST', '127.0.0.1') + ':' + os.getenv('PORT', '8080')
workers = cpu_count() * 2 + 1
threads = rds_pool_size - default_pool_size
worker_class = 'gthread'
timeout = 60
accesslog = '-'
errorlog = '-'
loglevel = 'debug'
capture_output = True

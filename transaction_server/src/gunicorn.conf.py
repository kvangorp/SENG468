bind = '0.0.0.0:8000'
backlog = 2048
workers = 4
threads = 100
worker_class = 'gthread'
worker_connections = 6000
timeout = 30
keepalive = 2
spew = False
errorlog = '-'
loglevel = 'debug'
accesslog = '-'
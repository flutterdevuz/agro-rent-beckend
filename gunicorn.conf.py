# Gunicorn Configuration for AgroTerra Production
# File: gunicorn.conf.py

import multiprocessing

# Server socket
bind = "0.0.0.0:5050"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
loglevel = "info"
accesslog = "/root/agroterra/logs/access.log"
errorlog = "/root/agroterra/logs/error.log"

# Process naming
proc_name = "agroterra"

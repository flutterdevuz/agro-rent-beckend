# Gunicorn Configuration for AgroRent (agrorent.uz)
# systemd: agrorent.service

# nginx bilan unix socket orqali ulanadi (port band qilmaydi)
bind = "unix:/run/agrorent/gunicorn.sock"
umask = 0o007  # socket'ga www-data (nginx) guruhi kira olishi uchun

# Server boshqa loyihalar bilan umumiy, shuning uchun workerlar soni cheklangan
workers = 3
worker_class = "sync"
timeout = 60
keepalive = 2

# Loglar journald'ga yoziladi: journalctl -u agrorent
loglevel = "info"
accesslog = "-"
errorlog = "-"

proc_name = "agrorent"

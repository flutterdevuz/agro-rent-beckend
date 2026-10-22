#!/bin/bash
# =============================================
# AgroRent (agrorent.uz) deploy skripti
# Serverda root sifatida ishga tushiring:  bash /opt/agrorent/app/deploy.sh
# =============================================

set -euo pipefail

APP_DIR=/opt/agrorent/app
VENV=/opt/agrorent/venv
DATA_DIR=/opt/agrorent/data
BACKUP_DIR=/opt/agrorent/backups
as_app() { sudo -u agrorent -H "$@"; }
# agrorent foydalanuvchisi o'qiy oladigan papkadan ishlaymiz (masalan /root emas)
cd /opt/agrorent

echo "🌿 AgroRent deploy boshlandi..."

# --- 1. Bazaning zaxira nusxasi ---
if [ -f "$DATA_DIR/db.sqlite3" ]; then
    echo "💾 Baza zaxiralanmoqda..."
    as_app mkdir -p "$BACKUP_DIR"
    as_app "$VENV/bin/python" -c "import sqlite3, sys; sqlite3.connect(sys.argv[1]).backup(sqlite3.connect(sys.argv[2]))"         "$DATA_DIR/db.sqlite3" "$BACKUP_DIR/db-$(date +%Y%m%d-%H%M%S).sqlite3"
    # Oxirgi 30 ta zaxira saqlanadi
    ls -1t "$BACKUP_DIR"/db-*.sqlite3 | tail -n +31 | xargs -r rm --
fi

# --- 2. Yangi kod ---
as_app mkdir -p /opt/agrorent/cache
echo "📦 Kod yangilanmoqda..."
as_app git -C "$APP_DIR" pull --ff-only origin main

# --- 3. Kutubxonalar ---
echo "📥 Kutubxonalar o'rnatilmoqda..."
as_app /opt/agrorent/bin/uv pip install --python "$VENV/bin/python" -q -r "$APP_DIR/requirements.txt"

# --- 4. Migratsiya va static fayllar ---
cd "$APP_DIR/agroRent"
echo "🗄️  Migratsiyalar..."
as_app "$VENV/bin/python" manage.py migrate --no-input
echo "📁 Static fayllar..."
as_app "$VENV/bin/python" manage.py collectstatic --no-input -v 0

# --- 5. Qayta ishga tushirish ---
echo "🔄 Xizmat qayta ishga tushirilmoqda..."
cp "$APP_DIR/agrorent.service" /etc/systemd/system/agrorent.service
systemctl daemon-reload
systemctl restart agrorent
sleep 2
systemctl is-active --quiet agrorent || { journalctl -u agrorent -n 30 --no-pager; exit 1; }

echo ""
echo "✅ AgroRent ishga tushdi: https://agrorent.uz"
echo "🔐 Admin: https://agrorent.uz/admin/?access=<ADMIN_ACCESS_KEY>"

#!/bin/bash
# =============================================
# AgroTerra Production Deploy Script
# Root user, port 5050
# =============================================

set -e

echo "🌿 AgroTerra Deployment Starting..."

# --- 1. Pull latest code ---
echo "📦 Pulling latest code..."
cd /root/agroterra
git pull origin main

# --- 2. Activate virtual environment ---
echo "🐍 Activating virtual environment..."
source /root/agroterra/venv/bin/activate

# --- 3. Install/update dependencies ---
echo "📥 Installing dependencies..."
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# --- 4. Run migrations ---
echo "🗄️  Running migrations..."
cd /root/agroterra/agroRent
python manage.py migrate --no-input

# --- 5. Collect static files ---
echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

# --- 6. Create log directory ---
mkdir -p /root/agroterra/logs

# --- 7. Restart Gunicorn via systemd ---
echo "🔄 Restarting Gunicorn..."
systemctl daemon-reload
systemctl restart agroterra

# --- 8. Reload Nginx ---
echo "🌐 Reloading Nginx..."
nginx -t && systemctl reload nginx

echo ""
echo "✅ AgroTerra is LIVE on port 5050!"
echo "🔗 Site:   https://yourdomain.com"
echo "🔐 Admin:  https://yourdomain.com/admin/?access=agroterra_premium_2026"
echo "📖 Docs:   https://yourdomain.com/api/docs/?access=agroterra_premium_2026"

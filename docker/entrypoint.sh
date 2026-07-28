#!/bin/bash
set -e

cd /home/frappe/frappe-bench

SITE_NAME=${SITE_NAME:-x-electronics.local}

if [ ! -d "sites/$SITE_NAME" ]; then
  echo "Site $SITE_NAME not found — creating it now..."

  bench new-site "$SITE_NAME" \
    --db-type postgres \
    --db-host "$DB_HOST" \
    --db-port "$DB_PORT" \
    --db-root-username "$DB_USER" \
    --db-root-password "$DB_PASSWORD" \
    --admin-password "$ADMIN_PASSWORD"

  echo "Configuring Redis (Upstash)..."
  bench --site "$SITE_NAME" set-config redis_cache "$REDIS_CACHE_URL"
  bench --site "$SITE_NAME" set-config redis_queue "$REDIS_QUEUE_URL"

  echo "Installing warehouse_management app..."
  bench --site "$SITE_NAME" install-app warehouse_management

  echo "Site $SITE_NAME created and app installed."
else
  echo "Site $SITE_NAME already exists — skipping creation."
fi

bench use "$SITE_NAME"

echo "Starting Frappe web server on 0.0.0.0:8000"
bench serve --port 8000

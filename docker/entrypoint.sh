#!/bin/bash
set -e

cd /home/frappe/frappe-bench

SITE_NAME=${SITE_NAME:-x-electronics.local}
PORT=${PORT:-8000}


if [ ! -d "sites/$SITE_NAME" ]; then
    echo "Creating site: $SITE_NAME"

    bench new-site "$SITE_NAME" \
        --db-type postgres \
        --db-host "$DB_HOST" \
        --db-port "$DB_PORT" \
        --db-name "$DB_NAME" \
        --db-root-username "$DB_USER" \
        --db-root-password "$DB_PASSWORD" \
        --admin-password "$ADMIN_PASSWORD" \
        --force

    echo "Setting current site..."
    bench use "$SITE_NAME"

    echo "Configuring Redis..."
    bench --site "$SITE_NAME" set-config redis_cache "$REDIS_CACHE_URL"
    bench --site "$SITE_NAME" set-config redis_queue "$REDIS_QUEUE_URL"

    # Optional if using Upstash for Socket.IO
    if [ -n "$REDIS_SOCKETIO_URL" ]; then
        bench --site "$SITE_NAME" set-config redis_socketio "$REDIS_SOCKETIO_URL"
    fi

    echo "Installing warehouse_management..."
    bench --site "$SITE_NAME" install-app warehouse_management

    echo "Enabling scheduler..."
    bench --site "$SITE_NAME" enable-scheduler

    echo "Site created successfully."
else
    echo "Site already exists."

    bench use "$SITE_NAME"
fi

echo "Starting Frappe..."
exec bench serve --host 0.0.0.0 --port "$PORT"

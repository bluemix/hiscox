set -e

if [ "$1" = "odoo" ]; then
    echo "Starting Odoo..."
    exec odoo --addons-path=/mnt/extra-addons/hiscox -c /etc/odoo/odoo.conf
fi

exec "$@"

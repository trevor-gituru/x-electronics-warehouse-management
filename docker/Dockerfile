FROM frappe/bench:latest

WORKDIR /home/frappe

USER frappe

RUN bench init frappe-bench --frappe-branch version-15 --skip-redis-config-generation --no-backups

WORKDIR /home/frappe/frappe-bench

# Pull your app straight from GitHub — replace with your actual repo URL
RUN bench get-app https://github.com/trevor-gituru/x-electronics-warehouse-management.git

COPY --chown=frappe:frappe docker/entrypoint.sh /home/frappe/entrypoint.sh
USER root
RUN chmod +x /home/frappe/entrypoint.sh
USER frappe

EXPOSE 8000

ENTRYPOINT ["/home/frappe/entrypoint.sh"]

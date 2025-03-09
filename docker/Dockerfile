FROM odoo:17.0

USER root

COPY ./ /mnt/extra-addons/hiscox
RUN chown -R odoo:odoo /mnt/extra-addons/hiscox

USER odoo
CMD ["/entrypoint.sh"]

from odoo import models, fields, http
import requests
import base64
import qrcode
from io import BytesIO

import logging
_logger = logging.getLogger(__name__)


class HiscoxEditedCase(models.Model):
    _name = 'edited.hiscox.case'
    _description = 'Hiscox Application Case'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Customer Name', required=True)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone', required=True)

    application_status = fields.Selection([
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Application Status', default='pending')

    qr_code = fields.Binary(string='QR Code')

    def generate_qr_code(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        for record in self:
            # data = f"Name: {record.name}, Email: {record.email}, Phone: {record.phone}"
            data = f"{base_url}/api/hiscox/applications/{record.id}"
            _logger.info(f"generate_qr_code, data: {data}")
            qr = qrcode.make(data)
            buffer = BytesIO()
            qr.save(buffer, format='PNG')
            qr_image = base64.b64encode(buffer.getvalue())
            record.qr_code = qr_image

    def submit_to_hiscox(self):
        url = "https://api.hiscox.com/submit"
        headers = {'Content-Type': 'application/json'}
        payload = {
            'name': self.name,
            'email': self.email,
            'phone': self.phone
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            self.application_status = 'submitted'

            # notify user with a popup message
            self.web_message_notify(title='Success',
                                    message='Application successfully submitted',
                                    notification_type='success')

        except requests.exceptions.RequestException as e:
            self.env['ir.logging'].create({
                'name': 'Hiscox API Error',
                'type': 'server',
                'message': str(e),
                'path': "edited.hiscox.case(%s)" % self.id,
                'func': '',
                'line': ''
            })
            # notify user with a popup message
            self.web_message_notify(title='Failure',
                                    message=f'Error submitting application: {e}',
                                    notification_type='danger')

    def check_status_from_hiscox(self):
        url = f"https://api.hiscox.com/status/{self.id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            status = response.json().get('status')
            if status:
                self.application_status = status

                # notify user with a popup message
                self.web_message_notify(title='Info',
                                        message='Status Retrieved',
                                        notification_type='info')

        except requests.exceptions.RequestException as e:
            self.env['ir.logging'].create({
                'name': 'Hiscox API Error',
                'type': 'server',
                'message': str(e),
                'path': "edited.hiscox.case(%s)" % self.id,
                'func': '',
                'line': ''
            })
            # notify user with a popup message
            self.web_message_notify(title='Failure',
                                    message=f'Error checking status: {e}',
                                    notification_type='danger')

    # will be used to show pop-up web notifications in case the system user wants to
    def web_message_notify(self, title, message, notification_type):
        self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
            'type': notification_type,
            'title': title,
            'message': message,
            'sticky': False,
        })

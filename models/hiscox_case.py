from odoo import models, fields, api
import requests
import base64
import qrcode
from io import BytesIO

class HiscoxCase(models.Model):
    _name = 'hiscox.case'
    _description = 'Hiscox Application Case'

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
        for record in self:
            data = f"Name: {record.name}, Email: {record.email}, Phone: {record.phone}"
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
                'path': "hiscox.case(%s)" % self.id,
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
                                        message='Status Retrieved:',
                                        notification_type='info')
        except requests.exceptions.RequestException as e:
            self.env['ir.logging'].create({
                'name': 'Hiscox API Error',
                'type': 'server',
                'message': str(e),
                'path': "hiscox.case(%s)" % self.id,
                'func': '',
                'line': ''
            })
            # notify user with a popup message
            self.web_message_notify(title='Failure',
                                    message=f'Error checking status: {e}',
                                    notification_type='danger')

    def web_message_notify(self, title, message, notification_type):
        self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
            'type': notification_type,
            'title': title,
            'message': message,
            'sticky': False,
        })

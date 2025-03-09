
from odoo import http
from odoo.http import request
import base64
from io import BytesIO
import logging
_logger = logging.getLogger(__name__)

class HiscoxWebsite(http.Controller):
    # @http.route('/hiscox/apply', type='http', auth='public', website=True)
    # def hiscox_apply_form(self, **kw):
    #     return request.render('odoo_hiscox.hiscox_application_form')

    @http.route('/api/hiscox/submit', type='http', auth='public', methods=['POST'], website=True)
    def hiscox_submit_application(self, **post):
        _case = request.env['edited.hiscox.case'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'application_status': 'pending'
        })
        _logger.info(f'hiscox_submit_application, _case: {_case}')
        _case.generate_qr_code()

        qr_image = base64.b64encode(_case.qr_code).decode('utf-8')
        _logger.info(f'hiscox_submit_application, qr_image: {qr_image}')

        return request.render('hiscox.case_submitted', {'qr_code': qr_image})


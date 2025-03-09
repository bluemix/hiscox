from odoo import http
from odoo.http import request

# Define the HTTP controller for Hiscox application routes
class HiscoxWebsite(http.Controller):

    # Route to fetch application details by a given case ID
    @http.route('/api/hiscox/applications/<int:case_id>', type='http', auth='public', methods=['GET'], website=True)
    def hiscox_application_case(self, case_id):
        # check case exists before
        _case = request.env['edited.hiscox.case'].sudo().browse(case_id)

        if _case:  # If the case exists
            return request.render('hiscox.case_submitted',
                                  {'qr_code': _case.qr_code, 'status': _case.application_status})
        else:  # If the case doesn't exist
            return request.render('hiscox.case_submitted', )

    # Route to handle submission of new or existing applications
    @http.route('/api/hiscox/submit', type='http', auth='public', methods=['POST'], website=True)
    def hiscox_submit_application(self, **post):
        # Check if a case with the same phone or email already exists
        _case = request.env['edited.hiscox.case'].sudo().search([
            '|',
            ('phone', '=', post.get('phone')),
            ('email', '=', post.get('email'))
        ])

        if _case:  # exists
            return request.render('hiscox.case_submitted',
                                  {'qr_code': _case.qr_code, 'status': _case.application_status})
        else:  # not exists
            _case = request.env['edited.hiscox.case'].sudo().create({
                'name': post.get('name'),
                'email': post.get('email'),
                'phone': post.get('phone'),
                'application_status': 'pending',
            })
            # Generate a QR code for the new case (assumes this method exists on the model)
            _case.generate_qr_code()

            # Render the template with the new case's QR code
            return request.render('hiscox.case_submitted', {'qr_code': _case.qr_code})

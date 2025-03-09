from odoo.tests import HttpCase

class TestHiscoxAPIs(HttpCase):
    def test_02_submit_application_form(self):
        """Test submitting an application via the website form"""
        response = self.url_open('/api/hiscox/submit', data={
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '+123456789'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Scan the QR code for your application details', response.content)

    def test_03_track_application_page(self):
        """Test that the tracking page loads correctly"""
        case = self.env['edited.hiscox.case'].create({
            'name': 'Track User',
            'email': 'track@example.com',
            'phone': '+987654321',
            'application_status': 'pending'
        })
        response = self.url_open(f'/api/hiscox/applications/{case.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(case.name.encode(), response.content)

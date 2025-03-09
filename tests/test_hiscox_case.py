from odoo.tests.common import TransactionCase
import base64

class TestHiscoxCase(TransactionCase):
    def setUp(self):
        super(TestHiscoxCase, self).setUp()
        self.hiscox_case_model = self.env['edited.hiscox.case']

    def test_create_application_case(self):
        """Test application case creation"""
        case = self.hiscox_case_model.create({
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'phone': '+123456789',
            'application_status': 'pending'
        })
        self.assertEqual(case.name, 'John Doe')
        self.assertEqual(case.application_status, 'pending')

    def test_generate_qr_code(self):
        """Test QR code generation"""
        case = self.hiscox_case_model.create({
            'name': 'Jane Doe',
            'email': 'janedoe@example.com',
            'phone': '+987654321',
            'application_status': 'pending'
        })
        case.generate_qr_code()
        self.assertTrue(case.qr_code)
        self.assertIsInstance(base64.b64decode(case.qr_code), bytes)

    def test_submit_application(self):
        """Test submitting application to Hiscox API"""
        case = self.hiscox_case_model.create({
            'name': 'Alice Smith',
            'email': 'alice@example.com',
            'phone': '+192837465',
            'application_status': 'pending'
        })
        case.submit_to_hiscox()
        self.assertEqual(case.application_status, 'submitted')

    def test_check_status_from_hiscox(self):
        """Test fetching status from Hiscox API"""
        case = self.hiscox_case_model.create({
            'name': 'Bob Johnson',
            'email': 'bob@example.com',
            'phone': '+5647382910',
            'application_status': 'submitted'
        })
        case.check_status_from_hiscox()
        self.assertIn(case.application_status, ['approved', 'rejected', 'submitted'])

from odoo.tests import TransactionCase, tagged


@tagged('-at_install', 'post_install')  # Ensures test runs after Odoo is installed
class TestHiscoxCase(TransactionCase):

    def setUp(self):
        """ Set up test data before running tests """
        super(TestHiscoxCase, self).setUp()



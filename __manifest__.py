# -*- coding: utf-8 -*-
{
    'name': 'Hiscox',
    'version': '17.0.0.0.1',
    'category': 'Extra Tools',
    'summary': '''Hiscox digital application processing for Odoo''',
    'description': '''A simple module for customer data collection from Hiscox''',
    'author': 'Abdulmomen Bsruki',
    'maintainer': 'Abdulmomen Bsruki',
    'website': 'bluemix.me',
    'depends': ['base', 'mail', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/hiscox_case_views.xml',
        'views/application_case_template.xml',
        'views/case_submitted_template.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True
}

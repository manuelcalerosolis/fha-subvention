# -*- coding: utf-8 -*-
{
    'name': 'Subventions',
    "version": "13.0.1.0.0",
    'category': 'Tools',
    'summary': 'Centralize your subventions',
    'description': """
    This module offers the possibility of managing your subventions
""",
    'depends': [
        'base',
        'mail',
        'sale_management',
        'purchase',
        'account',
        'hr_timesheet',
    ],
    'data': [
        'security/fha_subvention_security.xml',
        'security/ir.model.access.csv',
        'views/account_analityc_account_view.xml',
        'views/account_analityc_group_view.xml',
        'views/account_analytic_line_view.xml',
        'views/fha_subvention_view.xml',
        'data/fha_subvention_data.xml',
    ],
    'application': True,
    "uninstall_hook": "uninstall_hook",
}

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from . import models

from odoo import api, SUPERUSER_ID

import logging
_logger = logging.getLogger(__name__)

def uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    accounts = env['account.analytic.account'].search([('subvention', '=', True)])
    accounts.write({'active': False})

    _logger.warning("The following subventions items have been archived following 'subventions' module uninstallation: %s" % accounts.ids)

    try:
        accounts.unlink()
    except:
        pass

    groups = env['account.analytic.group'].search([('subvention', '=', True)])

    try:
        groups.unlink()
    except:
        pass

    _logger.warning("The following subventions have been deleted following 'subventions' module uninstallation: %s" % groups.ids)

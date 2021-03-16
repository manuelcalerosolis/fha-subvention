# Copyright 2021 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models, _


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    move_name = fields.Many2one(
        related='move_id.move_id',
        string="Invoice Number",
        readonly=True,
    )

    # timesheet_invoice_id = fields.Many2one('account.move', string="Invoice", readonly=True, copy=False, help="Invoice created from the timesheet")

    # account_id = fields.Many2one('account.analytic.account', 'Analytic Account', required=True, ondelete='restrict', index=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

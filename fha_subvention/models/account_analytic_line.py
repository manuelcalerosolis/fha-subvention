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
    abs_amount = fields.Monetary(
        string="Absolute Amount",
        compute="_compute_amount",
        store=True,
    )

    @api.depends("amount")
    def _compute_amount(self):
        for record in self:
            record.abs_amount = abs(record.amount)

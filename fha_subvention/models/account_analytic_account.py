# Copyright 2020 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models, _


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    subvention = fields.Boolean(
        string="Subvention",
        default=False,
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id.id,
        required=True,
    )
    total_subvention = fields.Monetary(
        help='The total subvention concept.',
        currency_field='currency_id',
        track_visibility='always',
        default=0.0,
    )
    percentage = fields.Float(
        help='The percentage of subvention concept.',
        required=True,
        digits=(16, 2),
        track_visibility='always',
        default=0.0,
    )
    total_expense = fields.Monetary(
        string='Total expense',
        compute='_compute_total_expense',
        currency_field='currency_id',
        help='Total expense in this item',
    )
    percentage_expense = fields.Float(
        string='Percentage expense',
        compute='_compute_percentage_expense',
        help='Percentage of expense in this item',
    )

    def _compute_total_expense(self):
        for record in self:
            record.total_expense = 0

    def _compute_percentage_expense(self):
        for record in self:
            record.percentage_expense = 0

# Copyright 2020 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from datetime import date
from odoo import api, fields, models, _


class AccountAnalyticGroup(models.Model):
    _name = 'account.analytic.group'
    _inherit = ['account.analytic.group', 'mail.thread', 'mail.activity.mixin']

    is_readonly = fields.Boolean(
        string="Read Only",
        compute='_compute_readonly_subvention',
    )

    def _get_default_subvention(self):
        return self._context.get('in_subvention_app', False)

    subvention = fields.Boolean(
        string="Subvention",
        default=_get_default_subvention,
    )
    code = fields.Char(
        string="Subvention Code",
        help="Code of subvention.",
        required=True,
        index=True,
        track_visibility="always",
        default=lambda self: self.env['ir.sequence'].next_by_code('fha.subvention'),
    )
    date_init = fields.Date(
        string="Init Date",
        required=True,
        track_visibility="always",
        default=lambda d: date(date.today().year, 1, 1),
    )
    date_end = fields.Date(
        string="End Date",
        required=True,
        track_visibility="always",
        default=lambda d: date(date.today().year, 12, 31),
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Entity',
        track_visibility="always",
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id.id,
        required=True
    )
    total_subvention = fields.Monetary(
        help="The total subvention.",
        currency_field='currency_id',
        track_visibility="always",
    )
    percentage = fields.Float(
        help="The percentage of subvention.",
        digits=(16, 2),
        track_visibility="always",
    )
    annual_subvention = fields.Monetary(
        help="The annual subvention.",
        currency_field='currency_id',
        track_visibility="always",
    )
    annual_spend = fields.Monetary(
        help="The annual spend.",
        currency_field='currency_id',
        track_visibility="always",
    )
    account_analytic_account_ids = fields.One2many(
         comodel_name="account.analytic.account",
         inverse_name="group_id",
         string='Subvention items',
         track_visibility="always",
    )

    def _compute_readonly_subvention(self):
        for record in self:
            record.is_readonly = not self.env.user.has_group('fha_subvention.group_fha_administrator_subvention')

    @api.onchange('percentage')
    def on_change_percentage(self):
        self.annual_subvention = self.total_subvention * self.percentage / 100
        self.annual_spend = self.total_subvention * self.percentage / 100


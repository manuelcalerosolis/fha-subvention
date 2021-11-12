# Copyright 2021 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models, _


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    move_name = fields.Many2one(
        related='move_id.move_id',
        string='Invoice Number',
        readonly=True,
    )
    abs_amount = fields.Monetary(
        string='Absolute Amount',
        compute='_compute_amount',
        store=True,
    )
    subvention = fields.Boolean(
        string='Subvention',
        related='group_id.subvention',
    )
    account_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account',
        required=False,
        ondelete='restrict',
        index=True,
        domain="[('subvention', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )
    justified_percentage = fields.Float(
        related='account_id.percentage',
        digits=(16, 2),
        default=0.0,
    )
    justified_amount = fields.Monetary(
        string='Justified Amount',
        help='The justified amount.',
        currency_field='currency_id',
        compute='_compute_justified_amount',
    )
    is_subvention_app = fields.Boolean(
        compute='_compute_is_subvention_app',
    )

    def _timesheet_preprocess(self, vals):
        context = dict(self._context or {})
        result = super()._timesheet_preprocess(vals)
        if not context.get('is_subvention_app', False) and result.get('account_id'):
            result.pop('account_id')
        return result

    def _compute_is_subvention_app(self):
        context = dict(self._context or {})
        for record in self:
            record.is_subvention_app = context.get('is_subvention_app', False)

    @api.depends('amount')
    def _compute_amount(self):
        for record in self:
            record.abs_amount = abs(record.amount)

    @api.depends('amount', 'justified_percentage')
    def _compute_justified_amount(self):
        self.justified_amount = 0
        for record in self.filtered(lambda r: r.amount != 0):
            record.justified_amount = abs(record.amount) * record.justified_percentage / 100

    @api.model
    def create(self, vals):
        print("create account.analytic.line", self.justified_amount)
        return super().create(vals)

    def write(self, vals):
        print("write account.analytic.line", self.justified_amount)
        return super().write(vals)

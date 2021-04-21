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
    subvention = fields.Boolean(
        string='Subvention',
        related="group_id.subvention",
    )
    account_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account',
        required=False,
        ondelete='restrict',
        index=True,
        domain="[('subvention', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]"
    )

    def _timesheet_preprocess(self, vals):
        context = dict(self._context or {})
        result = super(AccountAnalyticLine, self)._timesheet_preprocess(vals)
        if not context.get('in_subvention_app', False) and result.get('account_id'):
            result.pop('account_id')
        return result

    @api.depends("amount")
    def _compute_amount(self):
        for record in self:
            record.abs_amount = abs(record.amount)

# Copyright 2020 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models, _


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    def _get_default_subvention(self):
        return self._context.get('in_subvention_app', False)

    subvention = fields.Boolean(
        string="Subvention",
        default=_get_default_subvention,
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
    account_analytic_line_ids = fields.One2many(
         comodel_name="account.analytic.line",
         inverse_name="account_id",
         string='Account Analytic Line',
         track_visibility="always",
    )

    def _compute_total_expense(self):
        for record in self:
            record.total_expense = sum(record.account_analytic_line_ids.mapped('amount'))

    def _compute_percentage_expense(self):
        for record in self:
            if record.total_subvention != 0:
                record.percentage_expense = abs(record.total_expense) / record.total_subvention * 100
            else:
                record.percentage_expense = 0

    def action_show_expenses(self):
        '''
        Open the expenses wizard
        '''
        self.ensure_one()
        # Get the view
        view = self.env.ref('fha_subvention.view_account_analytic_line')
        return {
            'name': _('Account Analytic Line'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.analytic.account',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': self.id,
            'context': dict(
                self.env.context
            ),
        }

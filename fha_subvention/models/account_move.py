# Copyright 2020 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        for rec in self:
            for line in rec.line_ids:
                if abs(
                    line.analytic_account_id.total_expense) + line.price_subtotal > line.analytic_account_id.total_subvention:
                    raise ValidationError(
                        _(
                            "You cannot validate a bill the line '%s' exceeds the limit of the item."
                        ) % line.name
                    )
        return super().action_post()

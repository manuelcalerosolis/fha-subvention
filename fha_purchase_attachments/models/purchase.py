# Copyright 2022 Xtendoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        for order in self:
            attachment_count = self.env['ir.attachment'].search_count(
                [('res_model','=','purchase.order'),('res_id','=',order.id)]
            )
            if attachment_count < 1:
                raise ValidationError(
                    "Necesita adjuntar al menos un documento"
                )
            if order.amount_untaxed > 1200 and attachment_count < 3:
                raise ValidationError(
                    "Necesita adjuntar al menos tres documentos para pedidos superiores a 1.200€"
                )
        return super().button_confirm()

# Copyright 2020 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from datetime import datetime, timedelta

from odoo import api, fields, models, _


class FhaSubventionConcept(models.Model):
    _name = "fha.subvention.concept"

    _inherit = ["mail.thread", "mail.activity.mixin"]

    _description = "Subvention Concept"

    name = fields.Char(
        string="Name",
        help="Name of subvention concept.",
        required=True,
        index=True,
        track_visibility="always",
    )
    code_id = fields.Many2one(
        "fha.subvention.code",
        store=True,
        required=True,
        string="Code",
        track_visibility="always",
    )

    def action_global(self):
        self.action_beep()
        self.action_notification()
        return

    def action_notification(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'danger',
                'title': _("Connection Test Succeeded!"),
                'message': _("Everything seems properly set up!"),
                'sticky': False,
            }
        }

    def action_beep(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'beep.action',
            'params': {}
        }


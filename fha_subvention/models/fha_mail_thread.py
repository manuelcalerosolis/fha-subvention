# Copyright 2020 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, exceptions, fields, models

class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    _description = 'Email Thread'

    message_ids = fields.One2many(
        'mail.message',
        'res_id',
        string='Messages',
        domain=lambda self: [('message_type', '!=', 'user_notification'), ('author_id', '!=', 1)],
        auto_join=True
    )

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
        domain=lambda self: self._domain_message(),
    )

    @api.model
    def _domain_message(self):
        if self.env.user.has_group('fha_subvention.specialist_group'):
            return [('message_type', '!=', 'user_notification')]
        return [('message_type', '!=', 'user_notification'), ('is_special', '=', False)]


class Message(models.Model):
    _inherit = 'mail.message'

    is_special = fields.Boolean(
        'Created by specialist',
        compute='_get_special',
        help='Created by group',
        store=True,
    )

    @api.depends('author_id')
    def _get_special(self):
        for message in self:
            message.is_special = self.env['res.users'].search(
                [('partner_id.id', '=', message.author_id[0].id)]).has_group('fha_subvention.specialist_group')

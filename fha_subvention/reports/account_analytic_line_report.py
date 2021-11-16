# Copyright 2020 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class AccountAnalyticLineView(models.TransientModel):
    _name = "account.analytic.line.view"
    _description = "Subvention View"
    _order = "date"

    date = fields.Datetime()
    name = fields.Many2one(comodel_name="product.product")


class AccountAnalyticLineReport(models.TransientModel):
    _name = "account.analytic.line.report"
    _description = "Subvention Report"

    date_from = fields.Date()
    date_to = fields.Date()

    # Data fields, used to browse report data
    results = fields.Many2many(
        comodel_name="account.analytic.line.view",
        compute="_compute_results",
        help="Use compute fields, so there is nothing store in database",
    )

    def _compute_results(self):
        self.ensure_one()
        ReportLine = self.env["account.analytic.line.view"]
        date_from = self.date_from or "0001-01-01"
        date_to = self.date_to or fields.Date.context_today(self)

        print(":"*80)
        print("date_from :", date_from)
        print("date_to :", date_to)
        print(":"*80)


        self._cr.execute(
            """
            SELECT
                line.name,
                line.date
            FROM
                account_analytic_line line
            WHERE
                CAST(line.date AS date) >= %s
                and
                CAST(line.date AS date) <= %s
            ORDER BY line.date
        """,
            (
                date_from,
                date_to,
            ),
        )
        results = self._cr.dictfetchall()

        print(":"*80)
        print("Results :", results)
        print(":"*80)

        self.results = [ReportLine.new(line).id for line in results]

    def print_report(self):
        self.ensure_one()
        action = self.env.ref("fha_subvention.action_account_analytic_line_report_pdf")
        return action.report_action(self, config=False)

    def _get_html(self):
        result = {}
        rcontext = {}
        report = self.browse(self._context.get("active_id"))
        if report:
            rcontext["o"] = report
            result["html"] = self.env.ref(
                "fha_subvention.action_account_analytic_line_report_html"
            ).render(rcontext)
        return result

    @api.model
    def get_html(self, given_context=None):
        return self.with_context(given_context)._get_html()

import logging
from base64 import b64decode
from io import StringIO

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


_logger = logging.getLogger(__name__)

try:
    from csv import reader
except (ImportError, IOError) as err:
    _logger.error(err)


class EmployeeTimesheetCostImport(models.TransientModel):
    _name = "employee.timesheet.cost.import"
    _description = "Employee Timesheet Cost Import"

    data_file = fields.Binary(
        string="File to Import",
        required=True,
        help="Get you data file.",
    )
    filename = fields.Char()

    def import_file(self):
        """ Process the file chosen in the wizard. """
        self.ensure_one()
        data_file = b64decode(self.data_file)
        if not data_file:
            return
        self._parse_file(data_file)

    def parse_row(self, csv_data):
        error_list = []
        for row in csv_data:
            print("*"*80)
            print("row", row[1])
            print("*"*80)

            if row[1] == "":
                error_list.append(
                    _("Employee is empty: %s") % (row[1])
                )
        if error_list:
            raise ValidationError(
                _("Has errors: " "\n%s") % "\n".join(error_list)
            )

    def _parse_file(self, data_file):
        try:
            data = StringIO(data_file.decode("utf-8"))
            csv_data = reader(data)
            next(csv_data)
        except Exception:
            raise UserError(_("Can not read the file"))
        self.parse_row(csv_data)
        return

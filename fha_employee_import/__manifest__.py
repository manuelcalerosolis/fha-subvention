{
    "name": "FHA Employee Import",
    "category": "Product",
    "version": "13.0.1.0",
    "depends": [
        "hr_timesheet"
    ],
    "description": """
        Wizard to Import FHA Employee.
        """,
    "data": [
        "wizard/employee_timesheet_cost_import.xml",
        "views/hr_employee_form_view.xml",],
    "installable": True,
    "auto_install": True,
}

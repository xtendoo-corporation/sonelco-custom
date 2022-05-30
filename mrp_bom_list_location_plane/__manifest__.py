# Copyright 2021 Manuel Calero - Xtendoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "MRP bom list location plane",
    "version": "13.0.0.0",
    "summary": "MRP bom list location plane",
    "author": "Dani Domínguez",
    "company": "Xtendoo",
    "website": "https://xtendoo.es",
    "category": "Extra Tools",
    "description": """
        MRP bom list location plane
    """,
    "depends": [
        "mrp",
    ],
    "data": [
        "views/mrp_bom_list_view.xml",
        "views/report_view/mrp_report_bom.xml",
    ],
    "installable": True,
    "auto_install": False,
}

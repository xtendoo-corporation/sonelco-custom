# Copyright 2021 Manuel Calero - Xtendoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "MRP bom list location plane",
    "version": "18.0.1.0",
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
        "report_xlsx",
    ],
    "data": [
        "views/report_view/mrp_report_bom_xlsx.xml",
        "views/mrp_bom_list_view.xml",
        "views/report_view/mrp_report_bom.xml",
        "views/report_view/mrp_report_bom_simplify.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "mrp_bom_list_location_plane/static/src/**/*",
        ],
    },
    "installable": True,
    "auto_install": False,
}

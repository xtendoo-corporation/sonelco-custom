# Copyright 2024 Salvador González Jiménez - Xtendoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "propage_product_cost_cron",
    "version": "13.0.0.0",
    "summary": "Automatically update BOM costs for all products",
    "author": "Salvador González Jiménez",
    "company": "Xtendoo",
    "website": "https://xtendoo.es",
    "category": "Extra Tools",
    "description": """
        Cron BOM Cost Update
    """,
    "depends": [
        "mrp",
        "stock_account",
    ],
    "data": [
        "data/ir_cron_data.xml",
    ],
    "installable": True,
    "auto_install": False,
}

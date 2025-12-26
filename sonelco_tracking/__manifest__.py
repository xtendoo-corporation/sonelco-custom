# Copyright 2021 Manuel Calero - Xtendoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sonelco tracking",
    "version": "18.0.1.0",
    "summary": "Añade tracking a varios campos",
    "author": "Dani Domínguez",
    "company": "Xtendoo",
    "website": "https://xtendoo.es",
    "category": "Extra Tools",
    "description": """
        Añade tracking a varios campos
    """,
    "depends": [
        "base",
        "sale_order_type",
        "stock",
        "mail",
        "sonelco_stock_package_numbers",
    ],
    "data": [
        "views/tracking_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}

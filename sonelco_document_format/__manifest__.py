# Copyright 2021 Manuel Calero - Xtendoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sonelco Document Format",
    "version": "13.0.0.0",
    "summary": "Formatos de impresión para Sonelco",
    "author": "Dani Domínguez",
    "company": "Xtendoo",
    "website": "https://xtendoo.es",
    "category": "Extra Tools",
    "description": """
        Formatos de impresión para Sonelco
    """,
    "depends": [
        "purchase",
        "product",
        "sonelco_stock_package_numbers",
    ],
    "data": [
        "views/package_label/package_label.xml",
        "views/purchase/purchase_order_view.xml",
        "views/sale/sale_order_view.xml",
        "views/stock_picking/stock_picking.xml",
    ],
    "installable": True,
    "auto_install": False,
}

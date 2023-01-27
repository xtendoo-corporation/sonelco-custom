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
        "stock",
        "purchase",
        "product",
        "sonelco_stock_package_numbers",
        "stock_picking_report_valued",
        "rma",
        "account_invoice_report_grouped_by_picking",
    ],
    "data": [
        "views/papper_format/papper_format_A4.xml",
        "views/layout/external_layout_clean.xml",
        "views/sale/sale_order_view.xml",
        "views/rma/rma_view.xml",
        "views/package_label/package_label_new.xml",
        "views/stock_picking/unvalued_stock_picking.xml",
        "views/stock_picking/valued_stock_picking.xml",
        "views/purchase/purchase_order_view.xml",
        "views/invoice/account_move.xml",
        "views/label/papper_format.xml",
        "views/label/product_label.xml",
        "views/label/stock_production_lot.xml",
        "views/label/stock_production_serial.xml",
    ],
    "installable": True,
    "auto_install": False,
}

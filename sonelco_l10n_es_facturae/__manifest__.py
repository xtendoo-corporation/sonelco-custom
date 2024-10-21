# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sonelco Creación de Factura-e",
    "version": "14.0.2.5.0",
    "author": "ASR-OSS, "
    "FactorLibre, "
    "Tecon, "
    "Comunitea, "
    "Tecnativa, "
    "Creu Blanca, "
    "Odoo Community Association (OCA)",
    "category": "Accounting & Finance",
    "website": "https://github.com/OCA/l10n-spain",
    "license": "AGPL-3",
    "depends": [
        "l10n_es_facturae",
    ],
    "data": [
        "views/report_facturae.xml",
    ],
    "external_dependencies": {"python": ["OpenSSL", "xmlsig"]},
    "installable": True,
    "maintainers": ["etobella"],
}

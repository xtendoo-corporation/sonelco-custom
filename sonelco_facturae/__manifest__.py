# `sonelco_facturae/__manifest__.py`
{
    'name': 'Sonelco Facturae',
    'version': '18.0.1.0.0',
    'author': 'Xtendoo',
    'category': 'Accounting',
    'depends': [
        'l10n_es_facturae',
    ],
    'data': [
        'reports/report_facturae_inherit.xml',
    ],
    'installable': True,
    'auto_install': False,
}

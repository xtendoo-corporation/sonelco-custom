from odoo import models, fields, _

class StockQuantPackage(models.Model):
    _name = "stock.quant.package"
    _inherit = ["mail.thread", "mail.activity.mixin", "stock.quant.package"]

    partner_id = fields.Many2one(
        related="delivery_id.partner_id",
        string="Delivery Partner",
        tracking=True,
    )

    name = fields.Char(
        'Package Reference', copy=False, index='trigram', required=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('stock.quant.package') or _('Unknown Pack'), tracking=True)
    quant_ids = fields.One2many('stock.quant', 'package_id', 'Bulk Content', readonly=True,
                                domain=['|', ('quantity', '!=', 0), ('reserved_quantity', '!=', 0)], tracking=True)
    package_type_id = fields.Many2one(
        'stock.package.type', 'Package Type', index=True, tracking=True,)
    location_id = fields.Many2one(
        'stock.location', 'Location', compute='_compute_package_info',
        index=True, readonly=False, store=True, tracking=True)
    company_id = fields.Many2one(
        'res.company', 'Company', compute='_compute_package_info',
        index=True, readonly=True, store=True, tracking=True)
    owner_id = fields.Many2one(
        'res.partner', 'Owner', compute='_compute_owner_id', search='_search_owner',
        readonly=True, compute_sudo=True, tracking=True)
    package_use = fields.Selection([
        ('disposable', 'Disposable Box'),
        ('reusable', 'Reusable Box'),
    ], string='Package Use', default='disposable', required=True, tracking=True,
        help="""Reusable boxes are used for batch picking and emptied afterwards to be reused. In the barcode application, scanning a reusable box will add the products in this box.
            Disposable boxes aren't reused, when scanning a disposable box in the barcode application, the contained products are added to the transfer.""")
    shipping_weight = fields.Float(string='Shipping Weight', help="Total weight of the package.", tracking=True)
    valid_sscc = fields.Boolean('Package name is valid SSCC', compute='_compute_valid_sscc', tracking=True)
    pack_date = fields.Date('Pack Date', default=fields.Date.today, tracking=True)
    property_delivery_carrier_id = fields.Many2one(
        comodel_name='delivery.carrier',
        company_dependent=True,
        string="Delivery Method",
        help="Package delivery method.",
        tracking=True,
    )



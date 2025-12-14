from odoo import models, fields

class Payment(models.Model):
    _name = 'payment.report'
    _description = 'Payment Report'

    title = fields.Char(string='Title')
    total = fields.Float(string='Total')

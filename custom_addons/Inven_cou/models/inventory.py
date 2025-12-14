from odoo import models, fields

class InventoryItem(models.Model):
    _name = 'inventory.item'
    _description = 'Inventory Item'

    name = fields.Char(string='Item Name', required=True)
    price = fields.Float(string='Price')
    stock = fields.Integer(string='Stock Quantity')
    
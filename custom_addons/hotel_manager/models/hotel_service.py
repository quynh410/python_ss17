# -*- coding: utf-8 -*-
from odoo import models, fields

class HotelService(models.Model):
    _name = 'hotel.service'
    _description = 'Hotel Service'

    name = fields.Char(string='Name', required=True)
    price = fields.Integer(string='Price')

    _sql_constraints = [
        ('positive_price', 'check(price > 0)', 'Service price must be positive!')
    ]
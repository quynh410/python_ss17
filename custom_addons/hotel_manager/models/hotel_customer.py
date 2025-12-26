# -*- coding: utf-8 -*-
from odoo import models, fields

class HotelCustomer(models.Model):
    _name = 'hotel.customer'
    _description = 'Hotel Customer'

    name = fields.Char(string='Name', required=True)
    identity_card = fields.Char(string='Identity Card')
    phone = fields.Char(string='Phone')

    _sql_constraints = [
        ('unique_identity_card', 'unique(identity_card)', 'Identity card must be unique!')
    ]
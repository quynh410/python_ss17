# -*- coding: utf-8 -*-
from odoo import models, fields

class HotelRoomType(models.Model):
    _name = 'hotel.room.type'
    _description = 'Hotel Room Type'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
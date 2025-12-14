from odoo import models, fields

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    title = fields.Char(string='Title', required=True)
    pages = fields.Integer(string='Number of Pages', default=100)
    summary = fields.Text(string='Summary', copy=False)
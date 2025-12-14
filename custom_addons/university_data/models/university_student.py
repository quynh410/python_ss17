from odoo import models, fields

class UniversityStudent(models.Model):
    _name = 'university.student'
    _description = 'University Student'

    name = fields.Char(string='Student Name')
    year = fields.Integer(string='Year')

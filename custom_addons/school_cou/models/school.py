from odoo import models, fields

class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'School Student'

    name = fields.Char(string='Student Name', required=True)
    age = fields.Integer(string='Age')
    bio = fields.Text(string='Biography')
    is_active = fields.Boolean(string='Is Active', default=True)
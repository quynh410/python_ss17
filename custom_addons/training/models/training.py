from odoo import models, fields

class TrainingCourse(models.Model):
    _name = 'training.course'
    _description = 'Training Course'

    name = fields.Char(string='Course Name', required=True)
    duration = fields.Integer(string='Duration (days)')
    active = fields.Boolean(string='Active', default=True)
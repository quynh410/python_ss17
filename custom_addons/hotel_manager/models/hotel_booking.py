# from odoo import models, fields, api
# from odoo.exceptions import ValidationError
# from datetime import timedelta

# class HotelBooking(models.Model):
#     _name = 'hotel.booking'
#     _description = 'Hotel Booking'

#     code = fields.Char(string='Booking Code', required=True, copy=False, readonly=True, default='New')
#     check_in = fields.Date(string='Check-in Date', default=fields.Date.today)
#     check_out = fields.Date(string='Check-out Date')
#     duration = fields.Integer(string='Duration (Nights)', compute='_compute_duration', store=True)
#     total_amount = fields.Integer(string='Total Amount', compute='_compute_total_amount', store=True)
#     state = fields.Selection([
#         ('draft', 'Draft'),
#         ('confirmed', 'Confirmed'),
#         ('done', 'Done'),
#         ('cancelled', 'Cancelled')
#     ], string='State', default='draft', tracking=True)
#     customer_id = fields.Many2one('hotel.customer', string='Customer', required=True)
#     room_id = fields.Many2one('hotel.room', string='Room', required=True)
#     service_ids = fields.Many2many('hotel.service', string='Additional Services')

#     @api.model
#     def create(self, vals):
#         if vals.get('code', 'New') == 'New':
#             vals['code'] = self.env['ir.sequence'].next_by_code('hotel.booking') or 'New'
#         return super(HotelBooking, self).create(vals)

#     @api.depends('check_in', 'check_out')
#     def _compute_duration(self):
#         for record in self:
#             if record.check_in and record.check_out:
#                 record.duration = (record.check_out - record.check_in).days
#             else:
#                 record.duration = 0

#     @api.depends('room_id', 'duration', 'service_ids')
#     def _compute_total_amount(self):
#         for record in self:
#             room_cost = record.room_id.price_per_night * record.duration if record.room_id else 0
#             service_cost = sum(service.price for service in record.service_ids)
#             record.total_amount = room_cost + service_cost

#     @api.onchange('room_id')
#     def _onchange_room_id(self):
#         if self.room_id and self.room_id.status == 'maintenance':
#             return {
#                 'warning': {
#                     'title': 'Warning',
#                     'message': 'This room is under maintenance, please choose another room!'
#                 }
#             }

#     @api.onchange('check_in')
#     def _onchange_check_in(self):
#         if self.check_in:
#             self.check_out = self.check_in + timedelta(days=1)

#     @api.constrains('check_in', 'check_out')
#     def _check_dates(self):
#         for record in self:
#             if record.check_in and record.check_out and record.check_out <= record.check_in:
#                 raise ValidationError('Check-out date must be after check-in date!')

#     @api.constrains('room_id')
#     def _check_room_availability(self):
#         for record in self:
#             if record.room_id and record.room_id.status == 'occupied':
#                 raise ValidationError('This room is currently occupied!')

#     def action_confirm(self):
#         """Xác nhận đặt phòng và đánh dấu phòng là đã được thuê"""
#         for record in self:
#             record.state = 'confirmed'
#             if record.room_id:
#                 record.room_id.status = 'occupied'

#     def action_check_in(self):
#         """Check-in khách"""
#         for record in self:
#             if record.state != 'confirmed':
#                 raise ValidationError('Only confirmed bookings can be checked in!')
#             record.state = 'done'

#     def action_cancel(self):
#         """Hủy đặt phòng và trả phòng về trạng thái available"""
#         for record in self:
#             record.state = 'cancelled'
#             if record.room_id:
#                 record.room_id.status = 'available'

#     def action_draft(self):
#         """Đưa về trạng thái draft"""
#         for record in self:
#             record.state = 'draft'
#             if record.room_id:
#                 record.room_id.status = 'available'

# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessError
from datetime import timedelta

class HotelBooking(models.Model):
    _name = 'hotel.booking'
    _description = 'Hotel Booking'

    code = fields.Char(string='Booking Code', required=True, copy=False, readonly=True, default='New')
    check_in = fields.Date(string='Check-in Date', default=fields.Date.today)
    check_out = fields.Date(string='Check-out Date')
    duration = fields.Integer(string='Duration (Nights)', compute='_compute_duration', store=True)
    total_amount = fields.Integer(string='Total Amount', compute='_compute_total_amount', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='State', default='draft', tracking=True)
    customer_id = fields.Many2one('hotel.customer', string='Customer', required=True)
    room_id = fields.Many2one('hotel.room', string='Room', required=True)
    service_ids = fields.Many2many('hotel.service', string='Additional Services')

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('hotel.booking') or 'New'
        return super(HotelBooking, self).create(vals)

    @api.depends('check_in', 'check_out')
    def _compute_duration(self):
        for record in self:
            if record.check_in and record.check_out:
                record.duration = (record.check_out - record.check_in).days
            else:
                record.duration = 0

    @api.depends('room_id', 'duration', 'service_ids')
    def _compute_total_amount(self):
        for record in self:
            room_cost = record.room_id.price_per_night * record.duration if record.room_id else 0
            service_cost = sum(service.price for service in record.service_ids)
            record.total_amount = room_cost + service_cost

    @api.onchange('room_id')
    def _onchange_room_id(self):
        if self.room_id and self.room_id.status == 'maintenance':
            return {
                'warning': {
                    'title': 'Warning',
                    'message': 'This room is under maintenance, please choose another room!'
                }
            }

    @api.onchange('check_in')
    def _onchange_check_in(self):
        if self.check_in:
            self.check_out = self.check_in + timedelta(days=1)

    @api.constrains('check_in', 'check_out')
    def _check_dates(self):
        for record in self:
            if record.check_in and record.check_out and record.check_out <= record.check_in:
                raise ValidationError('Check-out date must be after check-in date!')

    @api.constrains('room_id', 'check_in', 'check_out', 'state')
    def _check_room_availability(self):
        """Kiểm tra phòng có trống trong khoảng thời gian đặt không"""
        for record in self:
            if record.room_id and record.check_in and record.check_out:
                # Bỏ qua kiểm tra nếu booking đã bị hủy
                if record.state == 'cancelled':
                    continue
                
                # Kiểm tra phòng có đang bảo trì không
                if record.room_id.status == 'maintenance':
                    raise ValidationError('This room is under maintenance!')
                
                # Tìm các booking trùng thời gian
                overlapping_bookings = self.search([
                    ('room_id', '=', record.room_id.id),
                    ('id', '!=', record.id),
                    ('state', 'in', ['confirmed', 'draft']),  # Chỉ kiểm tra booking confirmed và draft
                    '|',
                        '&',
                            ('check_in', '<=', record.check_in),
                            ('check_out', '>', record.check_in),
                        '&',
                            ('check_in', '<', record.check_out),
                            ('check_out', '>=', record.check_out),
                ])
                
                if overlapping_bookings:
                    raise ValidationError(
                        f'Room {record.room_id.name} is already booked from '
                        f'{overlapping_bookings[0].check_in} to {overlapping_bookings[0].check_out}!\n'
                        f'Please choose another room or different dates.'
                    )

    def action_confirm(self):
        """Xác nhận đặt phòng"""
        self.ensure_one()
        if not self.env.user.has_group('hotel_manager.hotel_manager_group_receptionist') and \
           not self.env.user.has_group('hotel_manager.hotel_manager_group_manager'):
            raise AccessError('You do not have permission to confirm bookings!')
        
        self.state = 'confirmed'
        self._update_room_status()
        return True

    def action_check_in(self):
        """Check-in khách"""
        self.ensure_one()
        if not self.env.user.has_group('hotel_manager.hotel_manager_group_receptionist') and \
           not self.env.user.has_group('hotel_manager.hotel_manager_group_manager'):
            raise AccessError('You do not have permission to check in!')
        
        if self.state != 'confirmed':
            raise ValidationError('Only confirmed bookings can be checked in!')
        
        self.state = 'done'
        # Khi check-in xong, cập nhật trạng thái phòng
        self._update_room_status()
        return True

    def action_cancel(self):
        """Hủy đặt phòng"""
        self.ensure_one()
        if not self.env.user.has_group('hotel_manager.hotel_manager_group_receptionist') and \
           not self.env.user.has_group('hotel_manager.hotel_manager_group_manager'):
            raise AccessError('You do not have permission to cancel bookings!')
        
        self.state = 'cancelled'
        # Khi hủy, cập nhật lại trạng thái phòng
        self._update_room_status()
        return True

    def action_draft(self):
        """Đưa về trạng thái draft"""
        self.ensure_one()
        if not self.env.user.has_group('hotel_manager.hotel_manager_group_receptionist') and \
           not self.env.user.has_group('hotel_manager.hotel_manager_group_manager'):
            raise AccessError('You do not have permission to reset bookings!')
        
        self.state = 'draft'
        self._update_room_status()
        return True

    def _update_room_status(self):
        """Cập nhật trạng thái phòng dựa trên các booking hiện tại"""
        for record in self:
            if not record.room_id:
                continue
            
            # Tìm booking hiện tại đang active (confirmed) cho phòng này
            today = fields.Date.today()
            active_bookings = self.search([
                ('room_id', '=', record.room_id.id),
                ('state', '=', 'confirmed'),
                ('check_in', '<=', today),
                ('check_out', '>', today),
            ])
            
            if active_bookings:
                # Có booking đang active -> phòng occupied
                record.room_id.sudo().status = 'occupied'
            else:
                # Không có booking nào đang active -> phòng available
                # (trừ khi đang bảo trì)
                if record.room_id.status != 'maintenance':
                    record.room_id.sudo().status = 'available'

    @api.model
    def cron_update_room_status(self):
        """Cron job để tự động cập nhật trạng thái phòng hàng ngày"""
        today = fields.Date.today()
        
        # Tìm tất cả các booking đã check-out
        expired_bookings = self.search([
            ('state', '=', 'confirmed'),
            ('check_out', '<=', today),
        ])
        
        for booking in expired_bookings:
            booking.state = 'done'
            booking._update_room_status()
        
        return True
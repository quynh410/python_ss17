from odoo import models, fields, api
from odoo.exceptions import ValidationError


# 1. MODEL MÔN HỌC
class TrainingSubject(models.Model):
    _name = 'training.subject'
    _description = 'Môn học'

    name = fields.Char(string="Tên môn", required=True)
    code = fields.Char(string="Mã môn")
    description = fields.Text(string="Mô tả đề cương")
    


# 2. MODEL GIẢNG VIÊN
class TrainingTeacher(models.Model):
    _name = 'training.teacher'
    _description = 'Giảng viên'

    name = fields.Char(string="Tên giảng viên", required=True)
    phone = fields.Char(string="Số điện thoại")
    skills = fields.Text(string="Kỹ năng")


# 3. MODEL SINH VIÊN
class TrainingStudent(models.Model):
    _name = 'training.student'
    _description = 'Sinh viên'

    name = fields.Char(string="Tên sinh viên", required=True)
    email = fields.Char(string="Email")
    student_id = fields.Char(string="Mã sinh viên")

    class_ids = fields.Many2many(
        'training.class',
        'training_class_training_student_rel',
        'training_student_id',
        'training_class_id',
        string="Classes"
    )
    class_count = fields.Integer(
        string="Số lớp",
        compute="_compute_class_count",
        store=True
    )

    @api.depends('class_ids')
    def _compute_class_count(self):
        for record in self:
            record.class_count = len(record.class_ids)


# 4. MODEL LỚP HỌC
class TrainingClass(models.Model):
    _name = 'training.class'
    _description = 'Lớp học'

    name = fields.Char(string="Tên lớp")
    start_date = fields.Date(string="Ngày bắt đầu")
    end_date = fields.Date(string="Ngày kết thúc")
    duration = fields.Integer(
        string="Thời lượng (ngày)",
        compute="_compute_duration",
        store=True
    )
    description = fields.Char(string="Mô tả lớp học")

    state = fields.Selection([
        ('draft', 'Dự thảo'),
        ('open', 'Đang mở'),
        ('closed', 'Đã đóng')
    ], default='draft', string="Trạng thái")

    price_per_student = fields.Integer(
        string="Học phí mỗi sinh viên",
        default=1000000
    )

    total_revenue = fields.Integer(
        string="Tổng doanh thu",
        compute="_compute_revenue",
        store=True
    )

    # Relationships
    subject_id = fields.Many2one(
        'training.subject',
        string="Môn học",
        required=True
    )
    teacher_id = fields.Many2one(
        'training.teacher',
        string="Giảng viên"
    )
    student_ids = fields.Many2many(
        'training.student',
        string="Danh sách sinh viên"
    )
    session_ids = fields.One2many(
        'training.session',
        'class_id',
        string="Lịch học chi tiết"
    )

    _sql_constraints = [
        ('duration_constraint', 'CHECK(duration > 3)', 'Thời lượng ít nhất phải 3 buổi'),
    ]

    # ---------------- COMPUTE ----------------
    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for record in self:
            if record.start_date and record.end_date:
                record.duration = (record.end_date - record.start_date).days + 1
            else:
                record.duration = 0

    @api.depends('price_per_student', 'student_ids')
    def _compute_revenue(self):
        for record in self:
            record.total_revenue = record.price_per_student * len(record.student_ids)

    # ---------------- ONCHANGE ----------------
    @api.onchange('name', 'start_date')
    def _onchange_description(self):
        for record in self:
            if record.name and record.start_date:
                record.description = (
                    f"Lớp {record.name} bắt đầu từ ngày {record.start_date}"
                )

    @api.onchange('price_per_student')
    def _onchange_price(self):
        if self.price_per_student and self.price_per_student < 1000000:
            return {
                'warning': {
                    'title': 'Cảnh báo học phí',
                    'message': 'Học phí mỗi sinh viên nên >= 1.000.000 để đảm bảo doanh thu.'
                }
            }
    @api.constrains('name')
    def _validate_name(self):
        for record in self:
            print(record.name)
            if not record.name:
                raise ValidationError("Tên lớp không được để trống!")
        # Tên phải nằm trong khoảng 8 - 20 kí tự 
            elif len (record.name) < 8 or len(record.name) > 20:
                raise ValidationError("Tên lớp phải từ 8 đến 20 kí tự!")

# 5. MODEL BUỔI HỌC
class TrainingSession(models.Model):
    _name = 'training.session'
    _description = 'Buổi học'

    name = fields.Char(string="Nội dung buổi học", required=True)
    date = fields.Date(
        string="Ngày học",
        default=fields.Date.today
    )
    duration = fields.Integer(string="Thời lượng (phút)")

    is_past = fields.Boolean(
        string="Đã qua",
        compute="_compute_is_past"
    )

    class_id = fields.Many2one(
        'training.class',
        string="Lớp học",
        ondelete='cascade'
    )

    @api.depends('date')
    def _compute_is_past(self):
        today = fields.Date.today()
        for record in self:
            record.is_past = record.date < today if record.date else False

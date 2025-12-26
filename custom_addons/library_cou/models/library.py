from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class LibraryCategory(models.Model):
    _name = 'library.category'
    _description = 'Library Category'

    name = fields.Char(string='Name', required=True)

class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Library Author'

    name = fields.Char(string='Name', required=True)
    bio = fields.Text(string='Biography')

class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = 'Library Loan History'

    borrower_name = fields.Char(string='Borrower Name')
    borrow_date = fields.Date(string='Borrow Date', default=fields.Date.today)
    return_date = fields.Date(string='Return Date')
    is_returned = fields.Boolean(string='Is Returned')
    duration = fields.Integer(string='Duration', compute='_compute_duration')
    book_id = fields.Many2one('library.book', string='Book', ondelete='cascade')

    @api.model
    def create(self, vals):
        record = super(LibraryLoan, self).create(vals)
        if record.book_id and record.book_id.state != 'lost':
            record.book_id.state = 'borrowed'
        return record

    @api.depends('borrow_date', 'return_date')
    def _compute_duration(self):
        for record in self:
            if record.return_date and record.borrow_date:
                record.duration = (record.return_date - record.borrow_date).days
            else:
                record.duration = 0

    @api.onchange('borrow_date')
    def _onchange_borrow_date(self):
        if self.borrow_date:
            self.return_date = self.borrow_date + timedelta(days=7)

    @api.onchange('is_returned')
    def _onchange_is_returned(self):
        if self.is_returned and self.book_id:
            self.book_id.state = 'available'

    @api.constrains('return_date', 'borrow_date')
    def _check_return_date(self):
        for record in self:
            if record.return_date and record.borrow_date and record.return_date < record.borrow_date:
                raise ValidationError('Ngày trả sách không thể đứng trước ngày mượn!')

    @api.constrains('book_id')
    def _check_book_state(self):
        for record in self:
            if record.book_id and record.book_id.state == 'lost':
                raise ValidationError('Cuốn sách này đã bị báo mất, không thể cho mượn!')

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string='Book Name', required=True)
    isbn = fields.Char(string='ISBN')
    short_description = fields.Char(string='Short Description', compute='_compute_short_description', store=True)
    purchase_date = fields.Date(string='Purchase Date', default=fields.Date.today)
    days_since_purchase = fields.Integer(string='Days Since Purchase', compute='_compute_days_since_purchase')
    total_loans = fields.Integer(string='Total Loans', compute='_compute_total_loans')
    notes = fields.Text(string='Notes')
    state = fields.Selection([
        ('draft', 'Mới nhập'),
        ('available', 'Có sẵn'),
        ('borrowed', 'Đang mượn'),
        ('lost', 'Đã mất')
    ], string='State', default='draft')
    condition = fields.Selection([
        ('0', 'Kém'),
        ('1', 'TB'),
        ('2', 'Tốt'),
        ('3', 'Mới')
    ], string='Condition')
    purchase_price = fields.Integer(string='Purchase Price', groups='library_cou.group_library_librarian')
    year = fields.Integer(string='Năm xuất bản')

    # SQL Constraints
    _sql_constraints = [
        ('isbn_unique', 'unique(isbn)', 'Mã ISBN này đã tồn tại trong hệ thống!'),
        ('purchase_price_positive', 'check(purchase_price > 0)', 'Giá nhập sách phải là số dương!'),
    ]

    # Relationships
    category_id = fields.Many2one('library.category', string='Category')
    author_ids = fields.Many2many('library.author', string='Authors')
    loan_ids = fields.One2many('library.loan', 'book_id', string='Loan History')

    @api.depends('name', 'author_ids', 'isbn')
    def _compute_short_description(self):
        for record in self:
            authors = ', '.join(record.author_ids.mapped('name')) if record.author_ids else ''
            record.short_description = f"{record.name} - {authors} ({record.isbn})"

    @api.depends('purchase_date')
    def _compute_days_since_purchase(self):
        today = fields.Date.today()
        for record in self:
            if record.purchase_date:
                record.days_since_purchase = (today - record.purchase_date).days
            else:
                record.days_since_purchase = 0

    @api.depends('loan_ids')
    def _compute_total_loans(self):
        for record in self:
            record.total_loans = len(record.loan_ids)

    @api.onchange('state')
    def _onchange_state(self):
        if self.state == 'lost':
            self.condition = '0'

    @api.onchange('isbn')
    def _onchange_isbn(self):
        if self.isbn and len(self.isbn) > 13:
            return {'warning': {'title': 'Cảnh báo', 'message': 'Mã ISBN không chuẩn (thường tối đa 13 số)' }}

    @api.onchange('category_id')
    def _onchange_category_id(self):
        if self.category_id:
            self.notes = f"Sách thuộc thể loại {self.category_id.name} - Vui lòng xếp đúng kệ."

    @api.constrains('year')
    def _check_year(self):
        for record in self:
            if record.year and record.year > fields.Date.today().year:
                raise ValidationError('Năm xuất bản không thể lớn hơn năm hiện tại!')
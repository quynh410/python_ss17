{
    'name': 'Library Management',
    'version': '1.0',
    'category': 'Unknown',
    'summary': 'Ứng dụng quản lý thư viện đơn giản',
    'author': 'Qyuhn',
    'depends': ['base'],
    'data': [
        "security/library_groups.xml",
        "security/ir.model.access.csv",
     
        "views/library_book_views.xml",
        "views/menu.xml",
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
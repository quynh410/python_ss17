{
    'name': 'Hotel Manager',
    'version': '1.0',
    'category': 'Hotel Management',
    'summary': 'Module for managing hotel rooms and bookings',
    'description': 'A comprehensive hotel management system including room management, customer management, and booking system.',
    'author': 'Your Name',
    'depends': ['base'],
    'data': [
        'security/hotel_groups.xml',
        'security/ir.model.access.csv',
        'data/hotel_sequence.xml',
        'data/hotel_cron.xml',
        'views/hotel_room_type_views.xml',
        'views/hotel_service_views.xml',
        'views/hotel_customer_views.xml',
        'views/hotel_room_views.xml',
        'views/hotel_booking_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
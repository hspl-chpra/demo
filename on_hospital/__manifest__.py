{
    'name': 'Hospital Management',
    'version': '1.0.0',
    'category': 'Hospital',
    'sequence': -100,
    'summary': 'Hospital managrmrnt system',
    'description': """Hospital managrmrnt system""",
    'depends': ['mail', 'product', 'base', ],
    'data': [
        'security/ir.model.access.csv',
        'data/patient_tag.xml',
        'data/patient.tag.csv',
        'data/sequence_data.xml',
        'views/menu.xml',
        'wizard/cancel_appointment.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/appoitment_view.xml',
        'views/patient_tag.xml',
        'views/play_ground.xml',
        'views/res_config_setting_view.xml',


    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',

}


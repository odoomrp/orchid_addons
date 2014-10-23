# -*- coding: utf-8 -*-
{
    "name" : "Sale Forecast",
    "version" : "0.1",
    "author": "OrchidERP",
    "category" : "sales",
    "description": """Sale Forecast """,
    "website": "http://www.orchiderp.com",
    "depends": ['product','sale','stock','orchid_product'],
    "data" : [
            'security/ir.model.access.csv',
            'report/od_sale_target_report_view.xml',
            'od_sales_target_view.xml',
            'report_orchid_sale_target.xml',
            'view/report_od_sales_target.xml'
            ],
    'css': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}

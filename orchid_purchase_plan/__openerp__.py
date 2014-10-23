# -*- coding: utf-8 -*-
{
    "name" : "Purchase Plan",
    "version" : "0.1",
    "author": "OrchidERP",
    "category" : "purchase",
    "description": """Purchase Plan """,
    "website": "http://www.orchiderp.com",
    "depends": ['purchase','orchid_sale_target'],
    "data" : [
            'security/ir.model.access.csv',
            'report/od_purchase_plan_report_view.xml',
            'wizard/od_purchase_plan_selection_view.xml',
            'od_purchase_plan_view.xml',
            'od_sales_target_view.xml',
            ],
    'css': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}

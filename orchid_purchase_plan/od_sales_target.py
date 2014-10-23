# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import copy
import math
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import datetime
import dateutil.relativedelta
from datetime import date, timedelta
import itertools
from lxml import etree
import openerp.addons.decimal_precision as dp

class od_sales_target(models.Model):
    _inherit = 'od.sales.target'
    purchase_plan_id = fields.Many2one('od.purchase.plan',string='Purchase Plan',readonly="1")
    def create_purchase_plan(self,cr,uid,ids,selection_type,context=None):
        for obj in self.browse(cr,uid,ids,context=context):
            if not obj.product_line:
                raise osv.except_osv(_('Warning!'), _('There Is No Product In Line'))
            if not obj.is_product:
                raise osv.except_osv(_('Warning!'), _('There Is No Product In Line'))   
            purchase_plan_obj = self.pool.get('od.purchase.plan')
            purchase_plan_ids = purchase_plan_obj.search(cr,uid,[('sale_forecast_id', '=', ids[0])])
            if purchase_plan_ids:
                raise osv.except_osv(_('Warning!'), _('Purchase Plan  Already Existing'))
            name =obj.name
            selection_type = selection_type
            
            date_from = obj.date_from
            is_product =obj.is_product
            is_brand = obj.is_brand
            is_salesman = obj.is_salesman
            is_category = obj.is_category
            is_customer = obj.is_customer
            date_to = obj.date_to
            fiscalyear_id = obj.fiscalyear_id and obj.fiscalyear_id.id
            pricelist_id = obj.pricelist_id and obj.pricelist_id.id
            
            company_id = obj.company_id and obj.company_id.id
            warehouse_id = obj.warehouse_id and obj.warehouse_id.id
            data = {
                'name': name,
                'sale_forecast_id':ids[0],
                'date_from':date_from,
                'date_to':date_to,
                'fiscalyear_id':fiscalyear_id,
                'pricelist_id':1,
                'warehouse_id':warehouse_id,
                'company_id':company_id,
            }
            purchase_plan_obj.create(cr,uid,data)
            purchase_ids = purchase_plan_obj.search(cr,uid,[('sale_forecast_id', '=', ids[0])])
            purchase_plan_id = purchase_plan_obj.browse(cr,uid,purchase_ids,context=context)
            purchase_plan_id = purchase_plan_id.id
            purchase_plan_line_obj = self.pool.get('od.purchase.plan.line')
            if obj.product_line:
                for line in obj.product_line:
                    delay_time = 0
                    price = 0.0
                    dicts ={}
                    parameter_obj = self.pool.get('ir.config_parameter')
                    if selection_type == 'lead_time':
                        if line.product_id.seller_ids:
                            dicts = { supplier.delay : supplier.name.id for supplier in line.product_id.seller_ids}
                            delays =min(dicts.keys())
                            delay_time = delays
                            supplier_id = dicts[delays]
                        else:
                            parameter_ids = parameter_obj.search(cr,uid,[('key','=', 'def_supplier')],context=context)
                            
                            if parameter_ids:
                                parameter_data = parameter_obj.browse(cr,uid,parameter_ids,context=context)
                                supplier_id = parameter_data.od_model_id.id

                            else:
                                raise osv.except_osv(_('Warning!'),_('No supplier selected\nplz config it in system parameters with key def_supplier!'))  
                        purchase_plan_line_obj.create(cr,uid,{
                                'purchase_product_plan_id':purchase_plan_id,
                                'product_id':line.product_id and line.product_id.id,
                                'quantity':line.quantity,
                                'average':line.average,
                                'delay':delay_time,
                                'price':price,
                                'supplier_id':supplier_id,
                                'sale_value':line.sale_value,
                                'sale_price':line.sale_price,
                                'p1_qty':line.p1_qty,
                                'p2_qty':line.p2_qty,
                                'p3_qty':line.p3_qty,
                                'p4_qty':line.p4_qty,
                                'p5_qty':line.p5_qty,
                                'p6_qty':line.p6_qty,
                                'p7_qty':line.p7_qty,
                                'p8_qty':line.p8_qty,
                                'p9_qty':line.p9_qty,
                                'p10_qty':line.p10_qty,
                                'p11_qty':line.p11_qty,
                                'p12_qty':line.p12_qty,
                                'p1_amount':line.p1_amount,
                                'p2_amount':line.p2_amount,
                                'p3_amount':line.p3_amount,
                                'p4_amount':line.p4_amount,
                                'p5_amount':line.p5_amount,
                                'p6_amount':line.p6_amount,
                                'p7_amount':line.p7_amount,
                                'p8_amount':line.p8_amount,
                                'p9_amount':line.p9_amount,
                                'p10_amount':line.p10_amount,
                                'p11_amount':line.p11_amount,
                                'p12_amount':line.p12_amount,
                                'total_computed_quantity':line.total_computed_quantity,
                                'total_computed_amount':line.total_computed_amount
                        })
                    pricelist_obj = self.pool.get('product.pricelist')
                    if selection_type == 'price':
                        if line.product_id.seller_ids:
                            price = pricelist_obj.price_get(cr, uid, [pricelist_id], line.product_id.id, line.quantity, line.product_id.seller_ids.id, {'uom': line.product_id.uom_id.id})[pricelist_id]
                            dicts = { price : supplier.name.id for supplier in line.product_id.seller_ids}
                            
                            price =min(dicts.keys())
                            supplier_id = dicts[price]
                        else:
                            parameter_ids = parameter_obj.search(cr,uid,[('key','=', 'def_supplier')],context=context)
                            if parameter_ids:
                                parameter_data = parameter_obj.browse(cr,uid,parameter_ids,context=context)
                                supplier_id = parameter_data.od_model_id.id
                            else:
                                raise osv.except_osv(_('Warning!'),_('No supplier selected\nPlz config it in system parameters with key def_supplier!'))
                        purchase_plan_line_obj.create(cr,uid,{
                                'purchase_product_plan_id':purchase_plan_id,
                                'product_id':line.product_id and line.product_id.id,
                                'quantity':line.quantity,
                                'average':line.average,
                                'delay':delay_time,
                                'price':price,
                                'supplier_id':supplier_id,
                                'sale_value':line.sale_value,
                                'sale_price':line.sale_price,
                                'p1_qty':line.p1_qty,
                                'p2_qty':line.p2_qty,
                                'p3_qty':line.p3_qty,
                                'p4_qty':line.p4_qty,
                                'p5_qty':line.p5_qty,
                                'p6_qty':line.p6_qty,
                                'p7_qty':line.p7_qty,
                                'p8_qty':line.p8_qty,
                                'p9_qty':line.p9_qty,
                                'p10_qty':line.p10_qty,
                                'p11_qty':line.p11_qty,
                                'p12_qty':line.p12_qty,
                                'p1_amount':line.p1_amount,
                                'p2_amount':line.p2_amount,
                                'p3_amount':line.p3_amount,
                                'p4_amount':line.p4_amount,
                                'p5_amount':line.p5_amount,
                                'p6_amount':line.p6_amount,
                                'p7_amount':line.p7_amount,
                                'p8_amount':line.p8_amount,
                                'p9_amount':line.p9_amount,
                                'p10_amount':line.p10_amount,
                                'p11_amount':line.p11_amount,
                                'p12_amount':line.p12_amount,
                                'total_computed_quantity':line.total_computed_quantity,
                                'total_computed_amount':line.total_computed_amount
                        })
        return True


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
class od_purchase_plan(models.Model):
    _name = 'od.purchase.plan'
    def create_sale_forecast(self,cr,uid,ids,context=None):
        result = self._get_act_window_dict(cr, uid, ids,'orchid_sale_target.od_sales_target_action1',context=context)
        return result
    def _get_act_window_dict(self, cr, uid, ids, name, context=None):
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        result = mod_obj.xmlid_to_res_id(cr, uid, name, raise_if_not_found=True)
        result = act_obj.read(cr, uid, [result], context=context)[0]
        return result







    def compute_distributed_quantity(self, cr, uid, ids, context=None):
        total_value = 0.0
        planned_target = 0.0
        for obj in self.browse(cr, uid, ids, context=context):
            for line in obj.product_line:
                    p1_qty = line.p1_qty
                    p2_qty = line.p2_qty
                    p3_qty = line.p3_qty
                    p4_qty = line.p4_qty
                    p5_qty = line.p5_qty
                    p6_qty = line.p6_qty
                    p7_qty = line.p7_qty
                    p8_qty = line.p8_qty
                    p9_qty = line.p9_qty
                    p10_qty = line.p10_qty
                    p11_qty = line.p11_qty
                    p12_qty = line.p12_qty
                    
                    total_computed_quantity = p1_qty + p2_qty + p3_qty + p4_qty + p5_qty + p6_qty + p7_qty +p8_qty + p9_qty + p10_qty + p11_qty + p12_qty
                    self.pool.get('od.purchase.plan.line').write(cr,uid,[line.id],{'total_computed_quantity': total_computed_quantity}, context=context)
                    planned_target = planned_target + line.total_computed_quantity
                    self.pool.get('od.purchase.plan').write(cr,uid,[obj.id],{'planned_target': planned_target}, context=context)
                       
        return 0








    fiscalyear_id = fields.Many2one('account.fiscalyear', string='Fiscal Year', required=True, )
    sale_forecast_id = fields.Many2one('od.sales.target',string='Sale Forecast',readonly="1")
    name = fields.Char(string='Name',required="1")
    product_line = fields.One2many('od.purchase.plan.line', 'purchase_product_plan_id', string='Product Lines')
    date_from = fields.Date('Date From')
    state = fields.Selection([
            ('draft','Draft'),
            ('progress','Progress'),
            ('done','Done'),
        ], string='Status', index=True, readonly=True, default='draft',
        track_visibility='onchange', copy=False,
       )
    date_to = fields.Date(string='Date To', index=True,
        help="Keep empty to use the current date", copy=False)
    company_id = fields.Many2one('res.company', string='Company',required="1")
    warehouse_id = fields.Many2one('stock.warehouse', string='Branch')
    period_type = fields.Selection([
            ('monthly','Monthly'),
            ('quaterly','Quaterly'),
            ('half','Half Yearly'),
            ('yearly','Yearly'),
        ], string='Analysis',default='monthly')
    estimated_target = fields.Float(string='Estimated Target')

    planned_target = fields.Float(string='Planned',readonly="1")
    achieved = fields.Float(string='Achieved(Actual)',readonly="1")
    pricelist_id = fields.Many2one('product.pricelist',string='Pricelist', required=True)

class od_purchase_plan_line(models.Model):
    _name = 'od.purchase.plan.line'
    purchase_product_plan_id = fields.Many2one('od.purchase.plan', string='Purchase Plan Product Wise',ondelete='cascade')
    brand_id = fields.Many2one('od.product.brand', string='Brand')
    delay = fields.Integer(string='Lead')
    price = fields.Float(string='Price')
    product_id = fields.Many2one('product.product', string='Product')
    salesman_id = fields.Many2one('res.users', string='SalesMan')
    customer_id = fields.Many2one('res.partner', string='Customer')
    supplier_id = fields.Many2one('res.partner', string='Supplier')
    category_id = fields.Many2one('product.category', string='Category')
    quantity = fields.Float(string='Quantity')
    average = fields.Float(string='Avg.Price')
    amount = fields.Float(string='Amount')
    sale_price = fields.Float(string='Sale Value Not')
    sale_value = fields.Float(string='Sale Value')
    channel = fields.Many2one('crm.case.section', string='Channel')
    p1_qty = fields.Integer(string='P1  Qty')
    p2_qty = fields.Integer(string='P2  Qty')
    p3_qty = fields.Integer(string='P3  Qty')
    p4_qty = fields.Integer(string='P4  Qty')
    p5_qty = fields.Integer(string='P5  Qty')
    p6_qty = fields.Integer(string='P6  Qty')
    p7_qty = fields.Integer(string='P7  Qty')
    p8_qty = fields.Integer(string='P8  Qty')
    p9_qty = fields.Integer(string='P9  Qty')
    p10_qty = fields.Integer(string='P10 Qty')
    p11_qty = fields.Integer(string='P11 Qty')
    p12_qty = fields.Integer(string='P12 Qty')
    p1_amount = fields.Float(string='P1 Amt')
    p2_amount = fields.Float(string='P2 Amt')
    p3_amount = fields.Float(string='P3 Amt')
    p4_amount = fields.Float(string='P4 Amt')
    p5_amount = fields.Float(string='P5 Amt')
    p6_amount = fields.Float(string='P6 Amt')
    p7_amount = fields.Float(string='P7 Amt')
    p8_amount = fields.Float(string='P8 Amt')
    p9_amount = fields.Float(string='P9 Amt')
    p10_amount = fields.Float(string='P10 Amt')
    p11_amount = fields.Float(string='P11 Amt')
    p12_amount = fields.Float(string='P12 Amt')
    period_type = fields.Selection([
            ('monthly','Monthly'),
            ('quaterly','Quaterly'),
            ('half','Half Yearly'),
            ('yearly','Yearly'),
        ], string='Period Type',default='yearly')
    salesman = fields.Boolean(string='SalesMan')
    category = fields.Boolean(string='Category')
    brand = fields.Boolean(string='Brand')
    customer = fields.Boolean(string='Customer')
    total_computed_quantity = fields.Float(string='Computed Quantity',readonly=True)
    total_computed_amount = fields.Float(string='Computed Amount',readonly=True)




        

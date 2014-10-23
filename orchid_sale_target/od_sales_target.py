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
    _name = 'od.sales.target'
    def action_progress(self, cr, uid, ids, context=None):
        self.write(cr, uid,ids, {'state': 'progress'})
        return True
    def action_done(self, cr, uid, ids, context=None):
        self.write(cr, uid,ids, {'state': 'done'})
        return True
    @api.multi
    def unlink(self):
        for target in self:
            if target.state not in ('draft'):
                raise Warning(_('You cannot delete it,it is not in draft.'))
        return super(od_sales_target, self).unlink()
    @api.multi
    def onchange_fiscalyear_id(self,fiscalyear_id):
        result = {}
        if fiscalyear_id:
            fiscal_year_obj = self.env['account.fiscalyear'].browse(fiscalyear_id)
            date_start = fiscal_year_obj.date_start
            date_stop = fiscal_year_obj.date_stop
            result = {'value': {
            'date_from': date_start,
            'date_to':date_stop
        }}
        
        return result

    @api.multi
    def onchange_is_salesman(self,is_salesman):
        result = {}
        if is_salesman:
            result = {'value': {
            'is_product': False,
            'is_category':False,
            'is_customer':False,
            'is_brand':False,
            
        }}
        
        return result
    @api.multi
    def onchange_is_product(self,is_product):
        result = {}
        if is_product:
            result = {'value': {
            'is_salesman': False,
            'is_category':False,
            'is_customer':False,
            'is_brand':False,
            
        }}
        
        return result
    @api.multi
    def onchange_is_category(self,is_category):
        result = {}
        if is_category:
            result = {'value': {
            'is_salesman': False,
            'is_product':False,
            'is_customer':False,
            'is_brand':False,
            
        }}
        
        return result
    @api.multi
    def onchange_is_customer(self,is_customer):
        result = {}
        if is_customer:
            result = {'value': {
            'is_salesman': False,
            'is_product':False,
            'is_category':False,
            'is_brand':False,
            
        }}
        
        return result
    @api.multi
    def onchange_is_brand(self,is_brand):
        result = {}
        if is_brand:
            result = {'value': {
            'is_salesman': False,
            'is_product':False,
            'is_category':False,
            'is_customer':False,
            
        }}
        
        return result





    @api.multi
    def onchange_date_from(self,date_from, fiscalyear_id):
        result = {}
        if date_from and fiscalyear_id:
            date_from = date_from
            fiscal_year_obj = self.env['account.fiscalyear'].browse(fiscalyear_id)
            date_stop = fiscal_year_obj.date_stop
            date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d')
            date_stop = datetime.datetime.strptime(date_stop, "%Y-%m-%d")
            days = (date_stop-date_from).days
            
            result = {'value': {
            'days_between_two_dates': days,
        }}
        return result
    @api.multi
    def onchange_date_to(self,date_to, fiscalyear_id):
        result = {}
        if date_to and fiscalyear_id:
            date_to = date_to
            fiscal_year_obj = self.env['account.fiscalyear'].browse(fiscalyear_id)
            date_start = fiscal_year_obj.date_start
            date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d')
            date_start = datetime.datetime.strptime(date_start, "%Y-%m-%d")
            days = (date_to-date_start).days
            
            result = {'value': {
            'days_between_two_dates': days,
        }}
        return result
    fiscalyear_id = fields.Many2one('account.fiscalyear', string='Fiscal Year', required=True, )
    name = fields.Char(string='Name',required="1",)
    brand_line = fields.One2many('od.sales.target.line', 'sale_brand_target_id', string='Brand Lines')
    category_line = fields.One2many('od.sales.target.line', 'sale_category_target_id', string='Category Lines')
    product_line = fields.One2many('od.sales.target.line', 'sale_product_target_id', string='Product Lines')
    supplier_line = fields.One2many('od.sales.target.line', 'sale_supplier_target_id', string='Supplier Lines')
    customer_line = fields.One2many('od.sales.target.line', 'sale_customer_target_id', string='Customer Lines')
    saleman_line = fields.One2many('od.sales.target.line', 'sale_saleman_target_id', string='Saleman Lines')
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
    sales_history = fields.Selection([
            ('monthly','Monthly'),
            ('yearly','Yearly(Not Implemented Yet)'),
        ], string='Sales History',default='monthly')
    period_type = fields.Selection([
            ('monthly','Monthly'),
            ('quaterly','Quaterly'),
            ('half','Half Yearly'),
            ('yearly','Yearly'),
        ], string='Analysis',default='monthly')
    sales_average = fields.Selection([
            ('1','1'),
            ('2','2'),
            ('3','3'),
            ('4','4'),
            ('5','5'),
            ('6','6'),
            ('7','7'),
            ('8','8'),
            ('9','9'),
            ('10','10'),
            ('11','11'),
            ('12','12'),
        ], string='Sales Average',default='1')
    target = fields.Float(string='Target Factor',default=1.0)
    estimated_target = fields.Float(string='Estimated Target')
    planned_target = fields.Float(string='Planned Target',readonly="1",store=True,compute='_compute_total_average')
    achieved = fields.Float(string='Achieved(Actual)',readonly="1")
    is_salesman = fields.Boolean(string='SalesMan')
    is_category = fields.Boolean(string='Category')
    is_brand = fields.Boolean(string='Brand',default=False)
    is_customer = fields.Boolean(string='Customer')
    is_product = fields.Boolean(string='Product',default=True)
    days_between_two_dates = fields.Integer(string='Days')
    pricelist_id = fields.Many2one('product.pricelist',string='Pricelist', required=True)
    p1 = fields.Boolean(string='P1',default=True)
    p2 = fields.Boolean(string='P2',default=True)
    p3 = fields.Boolean(string='P3',default=True)
    p4 = fields.Boolean(string='P4',default=True)
    p5 = fields.Boolean(string='P5',default=True)
    p6 = fields.Boolean(string='P6',default=True)
    p7 = fields.Boolean(string='P7',default=True)
    p8 = fields.Boolean(string='P8',default=True)
    p9 = fields.Boolean(string='P9',default=True)
    p10 = fields.Boolean(string='P10',default=True)
    p11 = fields.Boolean(string='P11',default=True)
    p12 = fields.Boolean(string='P12',default=True)
    @api.one
    @api.depends('product_line.average')
    def _compute_total_average(self):
        self.planned_target = sum((line.average) for line in self.product_line)
    def compute_distributed_quantity(self, cr, uid, ids, context=None):
        total_value = 0.0
        

        for obj in self.browse(cr, uid, ids, context=context):
            p1 = obj.p1
            print "QQQQQQQQQQQQQQQQQQQ",p1 
            p2 = obj.p2
            p3 = obj.p3
            p4 = obj.p4
            p5 = obj.p5
            p6 = obj.p6
            p7 = obj.p7
            p8 = obj.p8
            p9 = obj.p9
            p10 = obj.p10
            p11 = obj.p11
            p12 = obj.p12
            for line in obj.product_line:
                    if p1:
                    
                        p1_qty = line.p1_qty
                        p1_amount = line.p1_amount
                    else:
                        p1_qty = 0
                        p1_amount = 0.0
                        print "DDDDDDDDDDD"
                    if p2:
                    
                        p2_qty = line.p2_qty
                        p2_amount = line.p2_amount
                    else:
                        p2_qty = 0
                        p2_amount = 0

                    if p3:
                        p3_amount = line.p3_amount
                    
                        p3_qty = line.p3_qty
                    else:
                        p3_qty = 0
                        p3_amount = 0
                    if p4:
                        p4_amount = line.p4_amount
                        p4_qty = line.p4_qty
                    else:
                        p4_qty = 0
                        p4_amount = 0
                    if p5:
                        p5_qty = line.p5_qty
                        p5_amount = line.p5_amount
                    else:
                        p5_qty = 0
                        p5_amount = 0
                    if p6:
                        p6_qty = line.p6_qty
                        p6_amount = line.p6_amount
                    else:
                        p6_qty = 0
                        p6_amount = 0
                    if p7:
                        p7_qty = line.p7_qty
                        p7_amount = line.p7_amount
                    else:
                        p7_qty = 0
                        p7_amount = 0

                    if p8:
                        p8_amount = line.p8_amount
                        p8_qty = line.p8_qty
                    else:
                        p8_qty = 0
                        p8_amount = 0

                    if p9:
                        p9_qty = line.p9_qty
                        p9_amount = line.p9_amount
                    else:
                        p9_qty = 0
                        p9_amount = 0

                    if p10:
                        p10_amount = line.p10_amount
                        p10_qty = line.p10_qty
                    else:
                        p10_qty = 0
                        p10_amount = 0

                    if p11:
                        p11_amount = line.p11_amount
                    
                        p11_qty = line.p11_qty
                    else:
                        p11_qty = 0
                        p11_amount = 0

                    if p12:
                        p12_amount = line.p12_amount
                        p12_qty = line.p12_qty
                    else:
                        p12_qty = 0
                        p12_amount = 0
                   
                    average =line.average
                    total_value = total_value + average
                    self.pool.get('od.sales.target.line').write(cr,uid,[line.id],{'p1_qty': p1_qty,'p2_qty': p2_qty,'p3_qty': p3_qty,'p4_qty': p4_qty,'p5_qty': p5_qty,'p6_qty': p6_qty,'p7_qty': p7_qty,'p8_qty': p8_qty,'p9_qty': p9_qty,'p10_qty': p10_qty,'p11_qty': p11_qty,'p12_qty': p12_qty,'p12_amount':p12_amount,'p1_amount':p1_amount,'p2_amount':p2_amount,'p3_amount':p3_amount,'p4_amount':p4_amount,'p5_amount':p5_amount,
'p6_amount':p6_amount,'p7_amount':p7_amount,'p8_amount':p8_amount,'p9_amount':p9_amount,'p10_amount':p10_amount,'p11_amount':p11_amount}, context=context)
                    
                    total_computed_quantity = p1_qty + p2_qty + p3_qty + p4_qty + p5_qty + p6_qty + p7_qty +p8_qty + p9_qty + p10_qty + p11_qty + p12_qty
                    total_computed_amount = p1_amount + p2_amount + p3_amount + p4_amount + p5_amount + p6_amount + p7_amount + p8_amount + p9_amount + p10_amount + p11_amount + p12_amount                  
                    self.pool.get('od.sales.target.line').write(cr,uid,[line.id],{'total_computed_quantity': total_computed_quantity,'total_computed_amount':total_computed_amount}, context=context)
        return 0
    def distribute(self, cr, uid, ids, context=None):
        pricelist_obj = self.pool.get('product.pricelist')
        for obj in self.browse(cr, uid, ids, context=context):
            pricelist_id = obj.pricelist_id and obj.pricelist_id.id
            period_type = obj.period_type
            period_type = str(period_type)
            if period_type == 'monthly':
                for line in obj.product_line:
                    quantity = line.quantity
                    quantity = quantity / 12
                    quantity = math.ceil(quantity)
                    amount =0.0
                    if line.product_id:
                        product_id = line.product_id and line.product_id.id
                        price =pricelist_obj.price_get(cr, uid, [pricelist_id], product_id, 1)
                        price_key = list(price.keys())[0]
                        price = price[price_key]
                        if not price:
                            raise Warning(_('Pls configure Pricelist Properly.'))    
                        amount = quantity * price
#list(dict.keys())[0]
                    else:
                        sale_value = line.sale_value
                        amount = line.sale_value / 12
                        amount = math.ceil(amount)

                    self.pool.get('od.sales.target.line').write(cr,uid,[line.id],{'p1_qty': 0,'p2_qty': 0,'p3_qty': 0,'p4_qty': 0,'p5_qty': 0,'p6_qty': 0,'p7_qty': 0,'p8_qty': 0,'p9_qty': 0,'p10_qty': 0,'p11_qty': 0,'p12_qty': 0,'p12_amount':0,'p1_amount':0,'p2_amount':0,'p3_amount':0,'p4_amount':0,'p5_amount':0,'p6_amount':0,'p7_amount':0,'p8_amount':0,'p9_amount':0,'p10_amount':0,'p11_amount':0}, context=context)
                    self.pool.get('od.sales.target.line').write(cr,uid,[line.id],{'p1_qty': quantity,'p2_qty': quantity,'p3_qty': quantity,'p4_qty': quantity,'p5_qty': quantity,'p6_qty': quantity,'p7_qty': quantity,'p8_qty': quantity,'p9_qty': quantity,'p10_qty': quantity,'p11_qty': quantity,'p12_qty': quantity,'p12_amount':amount,'p1_amount':amount,'p2_amount':amount,'p3_amount':amount,'p4_amount':amount,'p5_amount':amount,
'p6_amount':amount,'p7_amount':amount,'p8_amount':amount,'p9_amount':amount,'p10_amount':amount,'p11_amount':amount}, context=context)
            elif period_type == 'yearly':
                for line in obj.product_line:
                    quantity = line.quantity
                    quantity = quantity / 1
                    quantity = math.ceil(quantity)
                    amount =0.0
                    if line.product_id:
                        product_id = line.product_id and line.product_id.id
                        price =pricelist_obj.price_get(cr, uid, [pricelist_id], product_id, 1)
                        amount = quantity*price[1]
                    else:
                        sale_value = line.sale_value
                        amount = line.sale_value / 1
                        amount = math.ceil(amount)
                    self.pool.get('od.sales.target.line').write(cr,uid,[line.id],{'p1_qty': 0,'p2_qty': 0,'p3_qty': 0,'p4_qty': 0,'p5_qty': 0,'p6_qty': 0,'p7_qty': 0,'p8_qty': 0,'p9_qty': 0,'p10_qty': 0,'p11_qty': 0,'p12_qty': 0,'p12_amount':0,'p1_amount':0,'p2_amount':0,'p3_amount':0,'p4_amount':0,'p5_amount':0,'p6_amount':0,'p7_amount':0,'p8_amount':0,'p9_amount':0,'p10_amount':0,'p11_amount':0}, context=context)
                    self.pool.get('od.sales.target.line').write(cr,uid,[line.id],{'p12_qty': quantity,'p12_amount':amount}, context=context)
            
            elif period_type == 'quaterly':
                for line in obj.product_line:
                    quantity = line.quantity
                    quantity = quantity / 4
                    quantity = math.ceil(quantity)
                    amount = 0.0
                    if line.product_id: 
                        product_id = line.product_id and line.product_id.id
                        price =pricelist_obj.price_get(cr, uid, [pricelist_id], product_id, 1)
                        amount = quantity*price[1]
                    else:
                        sale_value = line.sale_value
                        amount = line.sale_value / 4
                        amount = math.ceil(amount)
                    self.pool.get('od.sales.target.line').write(cr,uid,[line.id],{'p1_qty': 0,'p2_qty': 0,'p3_qty': 0,'p4_qty': 0,'p5_qty': 0,'p6_qty': 0,'p7_qty': 0,'p8_qty': 0,'p9_qty': 0,'p10_qty': 0,'p11_qty': 0,'p12_qty': 0,'p12_amount':0,'p1_amount':0,'p2_amount':0,'p3_amount':0,'p4_amount':0,'p5_amount':0,'p6_amount':0,'p7_amount':0,'p8_amount':0,'p9_amount':0,'p10_amount':0,'p11_amount':0}, context=context)
                    self.pool.get('od.sales.target.line').write(cr,uid,[line.id],{'p3_qty': quantity,'p6_qty': quantity,'p9_qty': quantity,'p12_qty': quantity,'p3_amount':amount,'p6_amount':amount,'p9_amount':amount,'p12_amount':amount}, context=context)
                    
     
            elif period_type == 'half':
                for line in obj.product_line:
                    quantity = line.quantity
                    quantity = quantity / 2
                    quantity = math.ceil(quantity)
                    amount = 0.0
                    if line.product_id:
                        product_id = line.product_id and line.product_id.id
                        price =pricelist_obj.price_get(cr, uid, [pricelist_id], product_id, 1)
                        amount = quantity*price[1]
                    else:
                        sale_value = line.sale_value
                        amount = line.sale_value / 2
                        amount = math.ceil(amount)
                    self.pool.get('od.sales.target.line').write(cr,uid,[line.id],{'p1_qty': 0,'p2_qty': 0,'p3_qty': 0,'p4_qty': 0,'p5_qty': 0,'p6_qty': 0,'p7_qty': 0,'p8_qty': 0,'p9_qty': 0,'p10_qty': 0,'p11_qty': 0,'p12_qty': 0,'p12_amount':0,'p1_amount':0,'p2_amount':0,'p3_amount':0,'p4_amount':0,'p5_amount':0,'p6_amount':0,'p7_amount':0,'p8_amount':0,'p9_amount':0,'p10_amount':0,'p11_amount':0}, context=context)
                    self.pool.get('od.sales.target.line').write(cr,uid,[line.id],{'p6_qty': quantity,'p12_qty': quantity,'p6_amount':amount,'p12_amount':amount}, context=context)
        self.compute_distributed_quantity(cr, uid, ids, context=context)
        return True
    def action_generate(self, cr, uid, ids, context=None):
        od_sales_target_line_obj = self.pool.get('od.sales.target.line')
        for obj in self.browse(cr, uid, ids, context=context):
            date_from = obj.date_from
            period_type = obj.period_type
            target_factor = obj.target
            name = obj.name 
            pricelist_id = obj.pricelist_id
            pricelist_id = pricelist_id.id
            warehouse_id = obj.warehouse_id and obj.warehouse_id.id
            print "*************************",warehouse_id
            date_to = obj.date_to
            date_to_str = str(date_to)
            date_from_str =str(date_from)
            d = datetime.datetime.strptime(date_from_str, "%Y-%m-%d")
            d_to = datetime.datetime.strptime(date_to_str, "%Y-%m-%d")
            diff = (12 * d_to.year + d_to.month) - (12 * d.year + d.month) + 1
            print "##########",diff
            d2 = d - dateutil.relativedelta.relativedelta(months=1)
            sales_average = obj.sales_average
            old_product_line_ids = od_sales_target_line_obj.search(cr, uid, [('sale_product_target_id', '=', obj.id)], context=context)
            if old_product_line_ids:
                 od_sales_target_line_obj.unlink(cr, uid, old_product_line_ids, context=context)
            if sales_average:
                date_froms = d - dateutil.relativedelta.relativedelta(months=int(sales_average))
                date_to = d
                date_from = str(date_froms)
                date_to = str(date_to)
                is_category = obj.is_category
                is_customer = obj.is_customer
                is_brand = obj.is_brand
                is_salesman = obj.is_salesman
                is_product = obj.is_product
                select_query = ''
                group_by_query = ''
                where_query = ''
                where_query_tuple = (date_from,date_to,)
                if warehouse_id:
                    where_query = where_query + " and so.warehouse_id = %s"
                    where_query_tuple = (date_from,date_to,warehouse_id,)
                    
                if is_product:
                    select_query = select_query + ", line.product_id"
                    group_by_query = group_by_query + ", line.product_id"
                else:
                    select_query = select_query + ", '' as C0"

                if is_category:
                    select_query = select_query + ", pt.categ_id"
                    group_by_query = group_by_query + ", pt.categ_id"
                else:
                    select_query = select_query + ", '' as C1"
                if is_customer:
                    select_query= select_query + ", so.partner_id"
                    group_by_query = group_by_query + ", so.partner_id"
                else:
                    select_query = select_query + ", ''  as C2"
                if is_salesman:
                    select_query= select_query + ", line.salesman_id"
                    group_by_query = group_by_query + ", line.salesman_id"
                else:
                    select_query = select_query + ", '' as C3"
                if is_brand:
                    select_query= select_query + ", pt.od_pdt_brand_id"
                    group_by_query = group_by_query + ", pt.od_pdt_brand_id"
                else:
                    select_query = select_query + ", '' as C4"
                cr.execute( "SELECT SUM(line.product_uom_qty) as qty, (sum(line.product_uom_qty*line.price_unit)/sum(line.product_uom_qty)) as average, pt.list_price as list_price, sum(line.product_uom_qty*line.price_unit) as sum" + select_query + \
                                " FROM sale_order_line line \
                                INNER JOIN product_product pd ON (pd.id=line.product_id)\
                                INNER JOIN product_template pt ON (pt.id=pd.product_tmpl_id)\
                                INNER JOIN sale_order so ON (so.id=line.order_id)\
                                where so.date_order between %s and %s" + where_query + \
                                " GROUP BY pt.list_price "+ group_by_query,where_query_tuple)
                res = cr.fetchall()
                qty_line1 = []
                sale_value_array = []
                
                sales_average = float(sales_average)
                diff = float(diff)
                if diff > 0:
                    for line in res:
                        qty_line1.append(line[0])
                        sale_value_array.append(line[3])
                        qty = 0.0
                        sale_values = 0.0
                        for i in qty_line1:
                            qty = i/sales_average
                            qty = qty * diff
                            qty = qty * target_factor
                            product_id = line[4]
                        for j in sale_value_array:
                            sale_values = j*target_factor
                            

                        
                        qty = math.ceil(qty)
                            
                        od_sales_target_line_obj.create(cr, uid,{
                            'sale_product_target_id':ids[0],
                            'sale_brand_target_id':ids[0],
                            'sale_saleman_target_id':ids[0],
                            'sale_category_target_id':ids[0],
                            'sale_customer_target_id':ids[0],
                            'quantity': qty,
                            'average':line[1],
                            'sale_price':line[2],
                            'sale_value':sale_values,
                            'product_id':line[4],
                            'category_id':line[5],
                            'customer_id':line[6],
                            'salesman_id':line[7],
                            'brand_id':line[8]
                        
                            })
                             
        return True                       
    @api.multi
    @api.one
    @api.constrains('date_from','date_to','fiscalyear_id')
    def _check_month(self):
        fiscalyear_id = self.fiscalyear_id.id
        fiscal_year_obj = self.env['account.fiscalyear'].browse(fiscalyear_id)
        date_start = fiscal_year_obj.date_start
        date_stop = fiscal_year_obj.date_stop
        date_from = self.date_from
        date_to = self.date_to
        if date_start<= date_from <=date_stop and date_start<= date_to <=date_stop:
            print "date_start"    
        else:
            raise Warning(_("Date From or Date To Is Not In The Fiscal Year,Please Enter Proper Dates %s") % self.date_to,self.date_from)
        date_from =str(date_from)
        date_to = str(date_to)
        date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d')
        date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d")
        diff = (12 * date_to.year + date_to.month) - (12 * date_from.year + date_from.month)
        if diff == 0:
            raise Warning(_("If You Want To Check Current Month Target,Please Put Date To As First Day Of Next Month %s") % self.date_to)
        elif diff < 1:
            raise Warning(_("Invalid Date,Date To is Less Than Date From, %s") % self.date_to)   
    def _get_act_window_dict(self, cr, uid, ids, name, context=None):
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        result = mod_obj.xmlid_to_res_id(cr, uid, name, raise_if_not_found=True)
        result = act_obj.read(cr, uid, [result], context=context)[0]
        return result
    def back(self, cr, uid, ids, context=None):
        result = self._get_act_window_dict(cr, uid, ids,'orchid_sale_target.od_sales_target_action3',context=context)
        result['res_id'] = ids[0]
        return result
    def action_view_generate(self, cr, uid, ids, context=None):
        result = self._get_act_window_dict(cr, uid, ids,'orchid_sale_target.od_sales_target_action2',context=context)
        result['res_id'] = ids[0]
        return result





class od_sales_target_line(models.Model):
    _name = 'od.sales.target.line'
    sale_brand_target_id = fields.Many2one('od.sales.target', string='Sales Target Brand',ondelete='cascade')
    sale_category_target_id = fields.Many2one('od.sales.target', string='Sales Target Category',ondelete='cascade')
    sale_product_target_id = fields.Many2one('od.sales.target', string='Sales Target Product',ondelete='cascade')
    sale_supplier_target_id = fields.Many2one('od.sales.target', string='Sales Target Supplier',ondelete='cascade')
    sale_customer_target_id = fields.Many2one('od.sales.target', string='Sales Target Customer',ondelete='cascade')
    sale_saleman_target_id = fields.Many2one('od.sales.target', string='Sales Target Saleman',ondelete='cascade')
    brand_id = fields.Many2one('od.product.brand', string='Brand')
    product_id = fields.Many2one('product.product', string='Product')
    is_brand = fields.Boolean(related='sale_product_target_id.is_brand',string='Is Brand',store=True)
    is_customer = fields.Boolean(related='sale_product_target_id.is_customer',string='Is Customer',store=True)
    is_salesman = fields.Boolean(related='sale_product_target_id.is_salesman',string='Is Salesman',store=True)
    is_category = fields.Boolean(related='sale_product_target_id.is_category',string='Is Category',store=True)
    is_product = fields.Boolean(related='sale_product_target_id.is_product',string='Is Product',store=True)
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

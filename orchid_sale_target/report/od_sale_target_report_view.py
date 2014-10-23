# -*- coding: utf-8 -*-
from openerp import tools
from openerp.osv import fields, osv
class od_sale_target_report_view(osv.osv):
    _name = "od.sale.target.report.view"
    _description = "od.sale.target.report.view"
    _auto = False
    _rec_name = 'target_id'
    _columns = {
       

        'target_id':fields.many2one('od.sales.target','Sale Target'),
        'target_line_id':fields.many2one('od.sales.target.line','Target Line'),
        'fiscalyear_id':fields.many2one('account.fiscalyear','Fiscal Year'),
        'product_id':fields.many2one('product.product','Product'),
        'brand_id':fields.many2one('od.product.brand','Brand'),
        'category_id':fields.many2one('product.category','Category'),
        'customer_id':fields.many2one('res.partner','Customer'),
        'salesman_id':fields.many2one('res.users','SalesMan'),
        'p1_qty':fields.integer('P1  Qty'),
        'p2_qty':fields.integer('P2  Qty'),
        'p3_qty':fields.integer('P3  Qty'),
        'p4_qty':fields.integer('P4  Qty'),
        'p5_qty':fields.integer('P5  Qty'),
        'p6_qty':fields.integer('P6  Qty'),
        'p7_qty':fields.integer('P7  Qty'),
        'p8_qty':fields.integer('P8  Qty'),
        'p9_qty':fields.integer('P9  Qty'),
        'p10_qty':fields.integer('P10  Qty'),
        'p11_qty':fields.integer('P11  Qty'),
        'p12_qty':fields.integer('P12  Qty'),

        'p1_amount':fields.float('P1 Amt'),
        'p2_amount':fields.float('P2 Amt'),
        'p3_amount':fields.float('P3 Amt'),
        'p4_amount':fields.float('P4 Amt'),
        'p5_amount':fields.float('P5 Amt'),
        'p6_amount':fields.float('P6 Amt'),
        'p7_amount':fields.float('P7 Amt'),
        'p8_amount':fields.float('P8 Amt'),
        'p9_amount':fields.float('P9 Amt'),
        'p10_amount':fields.float('P10 Amt'),
        'p11_amount':fields.float('P11 Amt'),
        'p12_amount':fields.float('P12 Amt'),
        'company_id':fields.many2one('res.company','Company'),
        'warehouse_id':fields.many2one('stock.warehouse','Branch'),
        'total_computed_quantity':fields.float('Computed Quantity'),
        'total_computed_amount':fields.float('Computed Amount'),
    }



    def _select(self):
        select_str = """
             SELECT ROW_NUMBER () OVER (ORDER BY od_sales_target.id ) AS id,
              od_sales_target.id as target_id,
              od_sales_target.company_id as company_id,
              od_sales_target.warehouse_id as warehouse_id,
              od_sales_target_line.id as target_line_id,
              account_fiscalyear.id as fiscalyear_id,
              od_sales_target_line.product_id as product_id,
              od_sales_target_line.brand_id as brand_id,
              od_sales_target_line.category_id as category_id,
              od_sales_target_line.customer_id as customer_id,
              od_sales_target_line.salesman_id as salesman_id,
              od_sales_target_line.p1_qty as p1_qty,
              od_sales_target_line.p1_amount as p1_amount,
              od_sales_target_line.p2_qty as p2_qty,
              od_sales_target_line.p2_amount as p2_amount,
              od_sales_target_line.p3_qty as p3_qty,
              od_sales_target_line.p3_amount as p3_amount,
              od_sales_target_line.p4_qty as p4_qty,
              od_sales_target_line.p4_amount as p4_amount,
              od_sales_target_line.p5_qty as p5_qty,
              od_sales_target_line.p5_amount as p5_amount,
              od_sales_target_line.p6_qty as p6_qty,
              od_sales_target_line.p6_amount as p6_amount,
              od_sales_target_line.p7_qty as p7_qty,
              od_sales_target_line.p7_amount as p7_amount,
              od_sales_target_line.p8_qty as p8_qty,
              od_sales_target_line.p8_amount as p8_amount,
              od_sales_target_line.p9_qty as p9_qty,
              od_sales_target_line.p9_amount as p9_amount,
              od_sales_target_line.p10_qty as p10_qty,
              od_sales_target_line.p10_amount as p10_amount,
              od_sales_target_line.p11_qty as p11_qty,
              od_sales_target_line.p11_amount as p11_amount,
              od_sales_target_line.p12_qty as p12_qty,
              od_sales_target_line.p12_amount as p12_amount,
              od_sales_target_line.total_computed_quantity as total_computed_quantity,
              od_sales_target_line.total_computed_amount as total_computed_amount
        """
        return select_str

    def _from(self):
        from_str = """
                od_sales_target_line
        """
        return from_str
    def _group_by(self):
        group_by_str = """
            GROUP BY account_fiscalyear.id,
                od_sales_target_line.brand_id,
                od_sales_target_line.category_id,
                od_sales_target_line.customer_id,
                od_sales_target_line.salesman_id,
                od_sales_target_line.p1_qty,
                od_sales_target_line.p1_amount,
                od_sales_target_line.p2_qty,
                od_sales_target_line.p2_amount,
                od_sales_target_line.p3_qty,
                od_sales_target_line.p3_amount,
                od_sales_target_line.p4_qty,
                od_sales_target_line.p4_amount,
                od_sales_target_line.p5_qty,
                od_sales_target_line.p5_amount,
                od_sales_target_line.p6_qty,
                od_sales_target_line.p6_amount,
                od_sales_target_line.p7_qty,
                od_sales_target_line.p7_amount,
                od_sales_target_line.p8_qty,
                od_sales_target_line.p8_amount,
                od_sales_target_line.p9_qty,
                od_sales_target_line.p9_amount,
                od_sales_target_line.p10_qty,
                od_sales_target_line.p10_amount,
                od_sales_target_line.p11_qty,
                od_sales_target_line.p11_amount,
                od_sales_target_line.p12_qty,
                od_sales_target_line.p12_amount,
                od_sales_target_line.total_computed_quantity,
                od_sales_target_line.total_computed_amount
                
                   
        """
        return group_by_str        






    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM  %s 
     INNER JOIN od_sales_target ON od_sales_target_line.sale_customer_target_id = od_sales_target.id
   OR od_sales_target_line.sale_saleman_target_id = od_sales_target.id
   OR od_sales_target_line.sale_product_target_id = od_sales_target.id
   OR od_sales_target_line.sale_supplier_target_id = od_sales_target.id
   OR od_sales_target_line.sale_brand_target_id = od_sales_target.id
   OR od_sales_target_line.sale_category_target_id = od_sales_target.id
   INNER JOIN account_fiscalyear ON od_sales_target.fiscalyear_id = account_fiscalyear.id
            )""" % (self._table, self._select(), self._from()))



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:



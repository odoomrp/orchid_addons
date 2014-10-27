# -*- coding: utf-8 -*-
from openerp import tools
from openerp.osv import fields, osv
class sale_report(osv.osv):
    _inherit = "sale.report"
    _columns = {
        'od_pdt_group_id': fields.many2one('od.product.group','Group'),
        'od_pdt_sub_group_id': fields.many2one('od.product.sub.group','Sub Group'),
        'od_pdt_type_id': fields.many2one('od.product.type','Type'),
        'od_pdt_sub_type_id': fields.many2one('od.product.sub.type','Sub Type'),
        'od_pdt_classification_id': fields.many2one('od.product.classification','Classification'),
        'od_pdt_hscode_id': fields.many2one('od.product.hscode','HS Code'),    
    }
    def _select(self):
        result = super(sale_report, self)._select()
        select_str = result + """,t.od_pdt_group_id as od_pdt_group_id,
                                  t.od_pdt_sub_group_id as od_pdt_sub_group_id,
                                  t.od_pdt_type_id as od_pdt_type_id,
                                  t.od_pdt_sub_type_id as od_pdt_sub_type_id,
                                  t.od_pdt_classification_id as od_pdt_classification_id,
                                  t.od_pdt_hscode_id as od_pdt_hscode_id
                              """
        return select_str

    def _group_by(self):
        result = super(sale_report,self)._group_by()
        group_by_str = result + """,t.od_pdt_group_id,
                                  t.od_pdt_sub_group_id,
                                  t.od_pdt_type_id,
                                  t.od_pdt_sub_type_id,
                                  t.od_pdt_classification_id,
                                  t.od_pdt_hscode_id
                                """
        return group_by_str
            

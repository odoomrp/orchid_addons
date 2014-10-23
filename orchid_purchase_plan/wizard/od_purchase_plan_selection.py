# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
class od_purchase_plan_selection(osv.osv_memory):
    _name = "od.purchase.plan.selection"
    _description = "Purchase Plan Selection"
    def create_purchase_plan(self, cr, uid, ids, context=None):
        for wizard in self.browse(cr, uid, ids, context=context):
            selection_type = wizard.selection_type
            sale_target_ids = [context['active_id']]
            self.pool.get('od.sales.target').create_purchase_plan(cr, uid, sale_target_ids, selection_type, context=context)
        return True
    selection_type = fields.Selection([
            ('lead_time','Lead Time'),
            ('price','Price'),
        ], string='Select',default='lead_time',required="1")
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

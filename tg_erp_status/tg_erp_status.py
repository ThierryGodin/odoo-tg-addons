# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 - Thierry Godin. All Rights Reserved
#    @author Thierry Godin <thierry@lapinmoutardepommedauphine.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm, fields, osv
import logging
from openerp import SUPERUSER_ID

_logger = logging.getLogger(__name__)

class tg_erp_status_config(osv.Model):
	_name = 'tg.erp.status.config'
	_order = 'create_date desc'

	_columns = {
		'create_date': fields.date('Creation date', readonly=True),
		'state': fields.selection([
            ('open','Opened'),
            ('maintenance','Maintenance')
            ], 'State', required=True),
		'message_id': fields.many2one('tg.erp.status.message', 'Message', help='Select message to be displayed during maintenance', required=False),
		'is_cur_config': fields.boolean('Current ERP Status')
	}

	def init(self, cr):
		conf_ids = self.search(cr, SUPERUSER_ID, [('state', 'in', ['open'])])
		if not conf_ids:
			self.create(cr, SUPERUSER_ID, {'state': 'open', 'is_cur_config': True})

	def create(self, cr, uid, values, context=None):
		context = context or {}

		if values.get('is_cur_config'):
			is_cur_config = values.get('is_cur_config')

			if is_cur_config == True:
				conf_ids = self.search(cr, SUPERUSER_ID, [('is_cur_config', '=', True)])
				if conf_ids :
					self.write(cr, SUPERUSER_ID, conf_ids, {'is_cur_config':False})

		return super(tg_erp_status_config, self).create(cr, SUPERUSER_ID, values, context)


	def write(self, cr, uid, ids, values, context=None):
		context = context or {}

		if values.get('is_cur_config'):
			is_cur_config = values.get('is_cur_config')

			if is_cur_config == True:
				conf_ids = self.search(cr, SUPERUSER_ID, [('is_cur_config', '=', True)])
				if conf_ids :
					self.write(cr, SUPERUSER_ID, conf_ids, {'is_cur_config':False})

		return super(tg_erp_status_config, self).write(cr, SUPERUSER_ID, ids, values, context)


	def get_erp_status(self, cr, uid, context=None):
		res = {
			'state' : 'open',
			'message_title': '',
			'message_text': '',
		}

		conf_ids = self.search(cr, SUPERUSER_ID, [('is_cur_config', '=', True)])
		if conf_ids :
			conf = self.browse(cr, SUPERUSER_ID, conf_ids[0])

			res['state'] = conf.state

			if conf.state == 'maintenance' :
				res['message_text'] = conf.message_id.message

		return res



class tg_erp_status_message(osv.Model):
	_name = 'tg.erp.status.message'

	_columns = {
		'create_date': fields.date('Creation date', readonly=True),
		'name': fields.char('Title', size=128, required=True),
		'message': fields.text('Message', required=True),
	}

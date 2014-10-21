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

import logging
from openerp import tools
from openerp import netsvc
from openerp.osv import osv, fields

_logger = logging.getLogger(__name__)

class tip(osv.Model):
	_name = 'tip'


	_columns = {
		'create_date': fields.date('Creation date', readonly=True),
		'write_date': fields.datetime("Modification Date", select=True, readonly=True),
		'name': fields.char('Title', size=64, required=True, translate=True),
		'model_ids': fields.many2many('ir.model',
			                          'tip_model_rel',
			                          'tip_id',
			                          'model_id',
			                          'Model'),
		'texte': fields.char('Text', size=160, required=True, translate=True),
		'active': fields.boolean('Active'),
	}

	_defaults ={
		'active' : True,
	}

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

{
    'name': 'TG ERP Status',
    'version': '1.1.0',
    'category': 'Tools',
    'sequence': 1,
    'author': 'Thierry Godin',
    'summary': 'ERP Status',
    'description': "Set OpenERP in maintenance or open mode",
    'depends': [
    	"base", 
    ],
    'data': [
        'security/ir.model.access.csv',
        'tg_erp_status_view.xml',
    ],
    'js': [
        'static/src/js/erp_status.js',
        ],
    'qweb': [
        'static/src/xml/erp_status.xml',
        ], 
    'css':[
        'static/src/css/erp_status.css',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
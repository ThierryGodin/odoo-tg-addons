# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
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
    'name': 'Tips ',
    'version': '1.0.0',
    'category': 'Tips',
    'sequence': 1,
    'author': 'Thierry Godin',
    'summary': 'Displays tips',
    'description': """
Tips :
======

    - Displays tips under title of main frame (oe_view_manager_header).
    - Tips can be applied to models or entire ERP
    - Displays Next button in case of multiple tips in a model
    
    """,
    'depends': [
    	"base", 
        "web",
    ],
    'data': [
        'security/tips.xml',
        'security/ir.model.access.csv',
        'tips_view.xml',
        'tips_data.xml',
    ],
    'js': [
        'static/src/js/tips.js',
    ],
    'qweb': [
        'static/src/xml/tips.xml',
    ], 
    'css':[
        'static/src/css/tips.css',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
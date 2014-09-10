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
    'name': 'TG Box',
    'version': '1.1.0',
    'category': 'Box',
    'sequence': 1,
    'author': 'Thierry Godin',
    'summary': 'Shared box',
    'description': """
TG Box :
===============

    - Allows to share documents as a gallery
    - Uploaded files are displayed in Kanban view (thumbnail) + download link
    - Multiple file extensions supported : pdf, txt, rtf, images (jpg, gif, png), xls, csv, doc, etc
    - Create categories + subcategories
    - Allows to post URLs (websites or download links)
    - Only authorized users can access documents


    """,
    'depends': ["base","web"],
    'data': [
        'security/tg_box_security.xml',
        'security/ir.model.access.csv',
        'tg_box_view.xml',
    ],
    'qweb': [
        'static/src/xml/tg_box.xml',
        ],
    'js': [
        'static/src/js/tg_box.js',
        ],
    'css':[
        'static/src/css/tg_box.css',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
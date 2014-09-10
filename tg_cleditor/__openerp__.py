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
    'name': 'TG Cleditor',
    'version': '1.0.0',
    'category': '',
    'sequence': 1,
    'author': 'Thierry Godin',
    'summary': 'Cleditor enhanced',
    'description': """
Cleditor enhanced :
==================

Allows to pass parameters to cleditor as examples below :
    
    * **editor_width** *(string)* : "500" or "30%%"
    * **editor_height** *(string)* : "500" or "30%%"
    * **editor_controls** *(string)* : "bold italic underline strikethrough subscript superscript | font size style | color highlight removeformat | bullets numbering | outdent indent | alignleft center alignright justify | undo redo | rule image link unlink | cut copy paste pastetext | print source"
    * **editor_colors** *(string)* : short Css colors space separated :  "FFF FCC FC9 FF9 FFC 9F9 9FF CFF CCF FCF " ...
    * **editor_fonts** *(string)* : font name comma separated : "Arial,Arial Black,Comic Sans MS,Courier New,Narrow,Garamond" ...
    * **editor_sizes** *(string)* : font size comma separated : "1,2,3,4,5,6,7"
    * **editor_docType** *(string)* : '&lt;!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"&gt;'
    * **editor_styles** *(string pairs as array name/tag)* : "Paragraph,&lt;p&gt;;Header 1,&lt;h1&gt;"
    * editor_useCSS (string but not managed to make it work)
    * editor_docCSSFile (string but not managed to make it work)
    * **editor_bodyStyle** *(string)* : "margin:4px; color:#4c4c4c; font-size:13px; "
    
Example:
=========

<field name="content"
    
    placeholder="e.g. Once upon a time..."
    
    widget="html"
    
    class="oe_edit_only"
    
    options='{"safe": True}'
    
    editor_width="100%%"
    
    editor_height="500"
    
    editor_controls="bold italic underline strikethrough subscript superscript | font size style | color highlight removeformat | bullets numbering | outdent indent | alignleft center alignright justify | undo redo | rule image link unlink | cut copy paste pastetext | print source"
    
    editor_styles="Paragraph,&lt;p&gt;;Header 1,&lt;h1&gt;"
    
    />
    
    


    """,
    'depends': ["web"],
    'data': [],
    'js': [
        'static/src/js/tg_cleditor.js'
    ],
    'qweb': [], 
    'css':[],
    'installable': True,
    'application': False,
    'auto_install': False,
}
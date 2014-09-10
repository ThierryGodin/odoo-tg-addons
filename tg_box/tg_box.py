# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 - Thierry Godin. All Rights Reserved
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

import hashlib
import itertools
import logging
import os
import re
import openerp
from openerp import tools, addons, modules
from openerp.osv import fields,osv
from openerp import SUPERUSER_ID
from os import path

_logger = logging.getLogger(__name__)

class tg_box_category(osv.Model):
    _name = 'tg.box.category'

    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1]+' / '+name
            res.append((record['id'], name))
        return res

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)
    
    def create(self, cr, uid, values, context=None):
        if context is None:
            context = {}
        
        category_name = values['name']  
        
        if values['parent_id'] != None:     
            cat_ids = self.search(cr, SUPERUSER_ID, [('id', '=', values['parent_id'])])
            
            if cat_ids:
                parent_cat = self.browse(cr, SUPERUSER_ID, cat_ids[0], context)
                parent_menu_id = parent_cat.menu_id
            else:
                parent_menu_id = None
                
        if parent_menu_id == None:
            obj_m_data = self.pool.get('ir.model.data')
            m_data_ids = obj_m_data.search(cr, SUPERUSER_ID, [('name', '=', 'menu_box_menu')])
            
            if m_data_ids:
                m_data = obj_m_data.browse(cr, SUPERUSER_ID, m_data_ids[0])
                parent_menu_id = m_data.res_id
            
     
        category_id = super(tg_box_category, self).create(cr, SUPERUSER_ID, values, context=context) 
        
        if category_id:
            menu_id = self.galery_category_menu_create(cr, SUPERUSER_ID, category_id, category_name, values['restricted'], parent_menu_id, context) 
            x = self.write(cr, SUPERUSER_ID, [category_id], {'menu_id':menu_id}, context=context) 

        ir_model_data = self.pool.get('ir.model.data')
        data_ids = ir_model_data.search(cr, SUPERUSER_ID, [('name', '=', 'tgbox_menu_top')])

        if data_ids:
            top_menu_id = ir_model_data.read(cr, SUPERUSER_ID, data_ids[0], ['res_id'])['res_id']         

        self.check_cat_action(cr, SUPERUSER_ID, context) 
        return category_id


    _columns = {
        'name' : fields.char('Category name', size=32, required=True),
        'complete_name': fields.function(_name_get_fnc, type="char", string='Name'),
        'menu_id': fields.integer('Menu'),
        'description' : fields.char('Category description', size=128),
        'parent_id': fields.many2one('tg.box.category', 'Parent Category', select=True, ondelete='cascade'),
        'child_ids': fields.one2many('tg.box.category', 'parent_id', 'Child Categories'),
        'parent_left': fields.integer('Left Parent', select=1),
        'parent_right': fields.integer('Right Parent', select=1),
        'restricted': fields.boolean('Restricted', help="If restricted, category is visible for managers only"),
    }

    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left, name'

    def _check_recursion(self, cr, uid, ids, context=None):
        level = 100
        while len(ids):
            cr.execute('select distinct parent_id from product_category where id IN %s',(tuple(ids),))
            ids = filter(None, map(lambda x:x[0], cr.fetchall()))
            if not level:
                return False
            level -= 1
        return True

    _constraints = [
        (_check_recursion, 'Error ! You cannot create recursive categories.', ['parent_id'])
    ]

    def child_get(self, cr, uid, ids):
        return [ids]
    
    def galery_category_menu_create(self, cr, uid,  category_id, category_name, restrict, parent_menu_id, context=None):
        if context is None:
            context = {}
            
        obj_view = self.pool.get('ir.ui.view')
        obj_menu = self.pool.get('ir.ui.menu')
        obj_action = self.pool.get('ir.actions.act_window')
        
        view_ids = obj_view.search(cr, SUPERUSER_ID, [('name', '=', 'tgbox.file.form.readonly')])
        if view_ids:
            vid = view_ids[0]
        else:
            vid = False

        value = {
            'name': category_name,
            'view_type': 'form',
            'view_mode': 'kanban,form',
            'res_model': 'tg.box',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }

        all_cat_ids = []
        cat_ids = self.search(cr, SUPERUSER_ID, [('parent_id', '=', category_id)])

        if cat_ids:
            all_cat_ids += cat_ids
            other_cat_ids1 = self.search(cr, SUPERUSER_ID, [('parent_id', 'in', cat_ids)])

            if other_cat_ids1:
                all_cat_ids += other_cat_ids1
                other_cat_ids2 = self.search(cr, SUPERUSER_ID, [('parent_id', 'in', other_cat_ids1)])

                if other_cat_ids2:
                    all_cat_ids += other_cat_ids2

        all_cat_ids.append(category_id)

        value['domain'] = "[('category_id','in', %s), '|', ('auth_user_ids', 'in', uid), ('auth_user_ids', '=', False)]" % (all_cat_ids)
        value['res_id'] = category_id
        value['context'] = "{'form_view_ref' : 'tg_box.tg_file_form_readonly'}"
        value['help'] = '<p class="oe_view_no content">There are currently no document in this box</p>'

        action_id = obj_action.create(cr, SUPERUSER_ID, value)

        create_vals ={
            'name': category_name,
            'parent_id':parent_menu_id,
            'sequence': 5,
            'icon': 'STOCK_DIALOG_QUESTION',
            'action': 'ir.actions.act_window,'+ str(action_id),
        }

        obj_data = self.pool.get('ir.model.data')
        grp_ids = obj_data.search(cr, SUPERUSER_ID, [('name','=','group_tg_box_manager'),('model','=','res.groups')])
        if grp_ids:
            grp_id = obj_data.read(cr, SUPERUSER_ID, grp_ids[0], ['res_id'])['res_id']

        if restrict == True and grp_id:
            create_vals['groups_id'] = [(6, 0, [grp_id])]

        menu_id = obj_menu.create(cr, SUPERUSER_ID, create_vals, context)
        return menu_id
        
    def write(self, cr, uid, ids, vals, context=None):
        upd = {}
        res = False

        obj_action = self.pool.get('ir.actions.act_window')
        obj_menu = self.pool.get('ir.ui.menu')
        
        if 'name' in vals or 'parent_id' in vals or 'restricted' in vals:
            data = self.browse(cr, SUPERUSER_ID, ids[0], context)
                  
            if 'name' in vals:   
                act_ids = obj_action.search(cr, SUPERUSER_ID, [('res_model', '=', 'tg.box'), ('res_id', '=', ids[0])])          
                if act_ids:
                    obj_action.write(cr, SUPERUSER_ID, act_ids[0], {'name' : vals['name']})
                    
                upd['name'] = vals['name']
                
            if 'parent_id' in vals:
                category_id = vals['parent_id']
                parent = self.browse(cr, SUPERUSER_ID, category_id, context)
                upd['parent_id'] = parent.menu_id 

            if 'restricted' in vals:
                obj_data = self.pool.get('ir.model.data')
                grp_ids = obj_data.search(cr, SUPERUSER_ID, [('name','=','group_tg_box_manager'),('model','=','res.groups')])
                if grp_ids:
                    grp_id = obj_data.read(cr, SUPERUSER_ID, grp_ids[0], ['res_id'])['res_id']

                if vals['restricted'] == True and grp_id:
                    upd['groups_id'] = [(6, 0, [grp_id])]
                else:
                    upd['groups_id'] = None

            obj_menu.write(cr, SUPERUSER_ID, data.menu_id, upd, context=context)  

        res =  super(tg_box_category, self).write(cr, SUPERUSER_ID, ids, vals, context=context)
        self.check_cat_action(cr, SUPERUSER_ID, context)  
        self.reorder_menu(cr, SUPERUSER_ID, context)  

        return res

    def check_cat_action(self, cr, uid, context=None):
        context = context or {}
        obj_action = self.pool.get('ir.actions.act_window')

        act_ids = obj_action.search(cr, SUPERUSER_ID, [('res_model', '=', 'tg.box'), ('res_id', '!=', None)])  

        for act_id in act_ids:
            cat_id = obj_action.read(cr, SUPERUSER_ID, act_id, ['res_id'])['res_id']

            all_cat_ids = []
            cat_ids = self.search(cr, SUPERUSER_ID, [('parent_id', '=', cat_id)])

            if cat_ids:
                all_cat_ids += cat_ids
                other_cat_ids1 = self.search(cr, SUPERUSER_ID, [('parent_id', 'in', cat_ids)])

                if other_cat_ids1:
                    all_cat_ids += other_cat_ids1
                    other_cat_ids2 = self.search(cr, SUPERUSER_ID, [('parent_id', 'in', other_cat_ids1)])

                    if other_cat_ids2:
                        all_cat_ids += other_cat_ids2

            all_cat_ids.insert(0, cat_id)

            v = {}
            v['domain'] = "[('category_id','in', %s), '|', ('auth_user_ids', 'in', uid), ('auth_user_ids', '=', False)]" % (all_cat_ids)
            obj_action.write(cr, SUPERUSER_ID, act_id, v)


    def reorder_menu(self, cr, uid, context=None):
        context = context or {}
        obj_menu = self.pool.get('ir.ui.menu')

        main_cat_ids = self.search(cr, SUPERUSER_ID, [('parent_id', '=', None)])
        int_main = 0

        for mcid in main_cat_ids:
            m_menu = self.read(cr, SUPERUSER_ID, mcid, ['menu_id'])

            if m_menu:
                int_main += 500
                int_sec = int_main
                obj_menu.write(cr, SUPERUSER_ID, m_menu['menu_id'], {'sequence': int_main})

                sec_cat_ids = self.search(cr, SUPERUSER_ID, [('parent_id', '=', mcid)])

                for scid in sec_cat_ids:
                    s_menu = self.read(cr, SUPERUSER_ID, scid, ['menu_id'])    

                    if s_menu:
                        int_sec += 30  
                        int_ter = int_sec 
                        obj_menu.write(cr, SUPERUSER_ID, s_menu['menu_id'], {'sequence': int_sec})

                        ter_cat_ids = self.search(cr, SUPERUSER_ID, [('parent_id', '=', scid)])

                        for tcid in ter_cat_ids:
                            t_menu = self.read(cr, SUPERUSER_ID, tcid, ['menu_id'])    

                            if t_menu:
                                int_ter += 1 
                                obj_menu.write(cr, SUPERUSER_ID, t_menu['menu_id'], {'sequence': int_ter})


    def unlink(self, cr, uid, ids, context=None):
        data = self.browse(cr, uid, ids[0], context)
        menu_id = data.menu_id     

        obj_box = self.pool.get('tg.box')
        obj_menu = self.pool.get('ir.ui.menu')

        doc_ids = obj_box.search(cr, SUPERUSER_ID, [('category_id', '=', ids[0])])

        if doc_ids:
            cat_defaut_ids = self.search(cr, SUPERUSER_ID, [('parent_id', '=', None)])
            if not cat_defaut_ids:
                raise osv.except_osv(_('Warning!'), _('This category is not empty. Move or delete documents first.'))
            else:
                for doc_id in doc_ids:
                    obj_box.write(cr, SUPERUSER_ID, doc_id, {'category_id': cat_defaut_ids[0]})
      
        # delete menu
        obj_menu.unlink(cr, SUPERUSER_ID, menu_id, context=context)
        
        #finally delete category
        return super(tg_box_category, self).unlink(cr, SUPERUSER_ID, ids, context=context)


    def get_subcat_list(self, cr, uid, cat_id, context=None):
        context = context or {}
        obj_action = self.pool.get('ir.actions.act_window')

        res = []
        order = 'parent_left, name'
        cat_ids = self.search(cr, SUPERUSER_ID, [('parent_id', '=', cat_id)], order=order)

        if cat_ids:
            for cid in cat_ids:
                category = self.read(cr, SUPERUSER_ID, cid, ['name', 'menu_id'])
                act_ids = obj_action.search(cr, uid, [('res_model', '=', 'tg.box'), ('res_id', '=', cid)])  
                val = {
                    'id': cid,
                    'action_id': act_ids[0] or False,
                    'name': category['name'],
                }
                res.append(val)

        return res
        

class tg_box(osv.Model):
    _name = 'tg.box'
    _description = 'Shared documents box'

    def _full_path(self, cr, uid, location, path):
        # location = 'file:filestore'
        assert location.startswith('file:'), "Unhandled filestore location %s" % location
        location = location[5:]

        # sanitize location name and path
        location = re.sub('[.]','',location)
        location = location.strip('/\\')

        path = re.sub('[.]','',path)
        path = path.strip('/\\')
        return os.path.join(tools.config['root_path'], location, cr.dbname, path)
         
    def _file_read(self, cr, uid, location, fname, bin_size=False):
        full_path = self._full_path(cr, uid, location, fname)
        r = ''
        try:
            if bin_size:
                r = os.path.getsize(full_path)
            else:
                r = open(full_path,'rb').read().encode('base64')
        except IOError:
            _logger.error("_read_file reading %s",full_path)
        return r

    def _file_write(self, cr, uid, location, value):
        bin_value = value.decode('base64')
        fname = hashlib.sha1(bin_value).hexdigest()
        # scatter files across 1024 dirs
        # we use '/' in the db (even on windows)
        fname = fname[:3] + '/' + fname
        full_path = self._full_path(cr, uid, location, fname)
        try:
            dirname = os.path.dirname(full_path)
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
            open(full_path,'wb').write(bin_value)
        except IOError:
            _logger.error("_file_write writing %s",full_path)
        return fname

    def _file_delete(self, cr, uid, location, fname):
        count = self.search(cr, 1, [('store_fname','=',fname)], count=True)
        if count <= 1:
            full_path = self._full_path(cr, uid, location, fname)
            try:
                os.unlink(full_path)
            except OSError:
                _logger.error("_file_delete could not unlink %s",full_path)
            except IOError:
                # Harmless and needed for race conditions
                _logger.error("_file_delete could not unlink %s",full_path)
                   
    def _data_get(self, cr, uid, ids, name, arg, context=None):
        if context is None:
            context = {}
        result = {}
        location = self.pool.get('ir.config_parameter').get_param(cr, uid, 'ir_tgbox.location')
        bin_size = context.get('bin_size')
        for attach in self.browse(cr, uid, ids, context=context):
            if location and attach.store_fname:
                result[attach.id] = self._file_read(cr, uid, location, attach.store_fname, bin_size)
            else:
                result[attach.id] = attach.db_datas
        return result    
 
    def _data_set(self, cr, uid, id, name, value, arg, context=None):
        # We dont handle setting data to null
        if not value:
            return True
        if context is None:
            context = {}
        location = self.pool.get('ir.config_parameter').get_param(cr, uid, 'ir_tgbox.location')
        file_size = len(value.decode('base64'))
        if location:
            attach = self.browse(cr, uid, id, context=context)
            if attach.store_fname:
                self._file_delete(cr, uid, location, attach.store_fname)
            fname = self._file_write(cr, uid, location, value)
            # SUPERUSER_ID as probably don't have write access, trigger during create
            super(tg_box, self).write(cr, SUPERUSER_ID, [id], {'store_fname': fname, 'file_size': file_size}, context=context)
        else:
            super(tg_box, self).write(cr, SUPERUSER_ID, [id], {'db_datas': value, 'file_size': file_size}, context=context)
        return True
        
    def _sizeof_fmt(self, cr, uid, ids, file_size, arg, context=None):
        res = {}
        val = ''
        if context is None:
            context = {}
        fs_ids = self.browse(cr, uid, ids, context)
       
        for fs in fs_ids:
            for x in ['bytes','KB','MB','GB']:
                
                if fs.file_size < 1024.0:
                    val = "%3.1f %s" % (fs.file_size, x)
                    break
                fs.file_size /= 1024.0                   
            res[fs.id] = val     
        return res
        
    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image, avoid_resize_medium=True)
        return result
        
    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
    
    def _get_icon(self, cr, uid, ids, name, value, args, context=None):
        if context is None:
            context = {}
        
        res = {}
        src = 'tg_box/static/src/img/fileext/'

        for obj  in self.browse(cr, uid, ids, context=context):
            
            if obj.datas_fname:
                ext = os.path.splitext(obj.datas_fname)[1][1:]
                ext = ext.lower()
                icon_filename = "%s.png" % (ext) 
            else:    
                icon_filename = "web.png"
            
            path = addons.get_module_resource('tg_box', 'static', 'src', 'img', 'fileext', icon_filename)
            
            if path:
                icon_path = "%s%s" % (src, icon_filename)
            else:
                icon_path = "%s_blank.png" % (src)
                
            image_file = tools.file_open(icon_path, 'rb')
            try:
                res[obj.id] = image_file.read().encode('base64')
            finally:
                image_file.close()

        return res

    def _get_extension(self, cr, uid, ids, name, value, args, context=None):
        if context is None:
            context = {}

        res = {}

        for obj  in self.browse(cr, uid, ids, context=context):
            
            if obj.datas_fname:
                ext = os.path.splitext(obj.datas_fname)[1][1:]
                ext = ext.upper()
            else:
                ext = "WEB"
            
            res[obj.id] = ext

        return res
           
    _columns ={
        'auth_user_ids' : fields.many2many('res.users', 
                                    'tg_box_authusers_rel', 
                                    'box_id', 
                                    'id', 
                                    'Authorized users'),
        'category_id' : fields.many2one('tg.box.category', 'Category', required=True, help="Select category for the current file"),
        'category_name': fields.related("category_id", "complete_name", type="char", string="Category"),
        'name' : fields.char('File name', size=32, required=True),
        'description' : fields.char('Description', size=128, help="File description"),
        'icon' : fields.function(_get_icon, string='Icon file', method=True, type="binary", store=False),
        'image': fields.binary("Image",
            help="This field holds the image."),
        'image_medium': fields.function(_get_image, fnct_inv=_set_image,
            string="Medium-sized image", type="binary", multi="_get_image",
            store={
                'tg.box': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized image "),
        'image_small': fields.function(_get_image, fnct_inv=_set_image,
            string="Small-sized image", type="binary", multi="_get_image",
            store={
                'tg.box': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Small-sized image"),
        'type': fields.selection( [ ('url','URL'), ('binary','Binary'), ],
                'Type', help="Binary File or URL", required=True, change_default=True),
        'url': fields.char('Url', size=1024),
        'datas': fields.function(_data_get, fnct_inv=_data_set, string='File Content', type="binary", nodrop=True),
        'datas_fname': fields.char('File Name',size=256),
        'extension' : fields.function(_get_extension, string='File extension', method=True, type="char", store=True),
        'store_fname': fields.char('Stored Filename', size=256),
        'file_size': fields.integer('File Size'),
        'hr_filesize' : fields.function(_sizeof_fmt, string='Human readable filesize', method=True, type="char", store=False),
        'db_datas': fields.binary('Database Data'),
        'sequence' : fields.integer('Sequence'),
        'create_date': fields.datetime("Created on", select=True, readonly=True),
        'create_uid': fields.many2one('res.users', 'Author', select=True, readonly=True),
        'write_date': fields.datetime("Modification Date", select=True, readonly=True),
        'write_uid': fields.many2one('res.users', "Last Contributor", select=True, readonly=True),
        'creator_name': fields.related("create_uid", "name", type="char", string="Creator Name"),
        'editor_name': fields.related("write_uid", "name", type="char", string="Editor Name"),
    }
    
    _defaults = {
        'sequence': 1,
        'file_size': 0,
        'type': 'binary',
    }

class inherit_res_users(osv.Model):
    _name = 'res.users'
    _inherit = 'res.users'

    _columns = {
        'box_ids': fields.many2many('tg.box', 
                                        'tg_box_authusers_rel', 'id', 
                                        'box_id', 
                                        'Box documents'), 
    }
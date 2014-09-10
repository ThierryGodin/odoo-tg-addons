'name': 'TG Box',
'version': '1.1.0',
'category': 'Box',
'sequence': 1,
'author': 'Thierry Godin',
'summary': 'Shared box',
---------------------------------

Thanks for downloading this module.

before you install this module you must follow these steps because files are stored on the server and not in database :

- Login Odoo/OpenERP as Administrator
- Go to Configuration -> Parameters -> System Parameters
- Create a new parameter : 
      Key   = ir_tgbox.location  
      Value = file:///tgboxstore
- and save
      
- Now get into server file system and go to /usr/lib/pymodules/python2.7/openerp  (Debian)
- create a folder named "tgboxstore" + chown openerp:openerp + CHMOD 755

signé n1bus
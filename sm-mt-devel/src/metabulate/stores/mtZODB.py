'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

Created on 19 Apr 2010
ZODB02.py Cloned on from ZOBD01.py 12 Jun 2010
ZODB.py Cloned on from ZOBD02.py 07 Jul 2010
Last Updated on 07 Jul 2010

20/04/2010 filepaths always expressed in UNIX format as seems to be expected by ZODB

12/06/2010 ZODB02.py cloned from ZODB01.py with:
    - folders re-configured

07/07/2010 ZODB.py cloned from ZODB02.py for SV versioning

@author: Administrator
'''

import metabulate.utils.utils      as mtutils

class DBstore(mtutils.ODBMS):
    def __init__(self,filename):
        if isinstance(filename,basestring):
            filename = filename.replace('\\','/')               # ZODB filepaths always with UNIX seperators
            from ZODB import FileStorage,DB
            self.storage = FileStorage.FileStorage(filename)
            db = DB(self.storage)
            connection = db.open()
            self.root = connection.root()
    def _commit(self):
        import transaction
        transaction.commit()
    def _close(self):
        self._commit()
        self.storage.close()
    def __getitem__(self,key):
        return self.root[key]
    def __setitem__(self,key,val):
        self.root[key] = val
    def __getattr__(self,attr):
        return getattr(self.root,attr)

'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

Created on 21 Dec 2009
index04.py Cloned from index03.py on 02 Mar 2010
index05.py Cloned from index04.py on 19 Apr 2010
index06.py Cloned from index05.py on 06 May 2010
index07.py Cloned from index06.py on 13 May 2010
index08.py Cloned from index07.py on 12 Jun 2010
index.py Cloned from index08.py on 07 Jul 2010
Last Updated on 07 Jul 2010

Non-singleton versions of "singleton" indexes

As index02.py imports singleton02.py supporting:
    version re-engineered with undefined setters = None
    and defaults with null setters
    also mtutils.empty() = None

02/01/10:
    class savedIndex renamed LoadableIndex
    class ExportableIndex added

02/03/10 index04.py cloned from index03.py with:
    - importing singleton03

19/04/2010 index05.py cloned from index04.py with:
    - Persistent Triple Stores supported

06/05/2010 index06.py cloned from index05.py with:
    - URI support exploited via updated imports

13/05/2010 index07.py cloned from index06.py with:
    - explicit alias_ontology support (via imports)

12/06/2010 index08.py cloned from index07.py with:
    - folders re-configured

07/07/2010 index.py cloned from index08.py with:

@author: Administrator
'''

import metabulate.singletons.singleton  as mtsingleton

class Index(mtsingleton._Transients): pass
class LoadableIndex(mtsingleton._Persistents): pass
class ExportableIndex(mtsingleton._Exportables): pass
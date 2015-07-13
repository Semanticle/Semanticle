'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

Created on 20 Dec 2009
singleton03.py Cloned from singleton02.py on 02 Mar 2010
singleton04.py Cloned from singleton03.py on 18 Mar 2010
singleton05.py Cloned from singleton04.py on 19 Apr 2010
singleton06.py Cloned from singleton05.py on 06 May 2010
singleton07.py Cloned from singleton06.py on 12 May 2010
singleton08.py Cloned from singleton07.py on 12 Jun 2010
singleton.py Cloned from singleton08.py on 07 Jul 2010
Last Updated 20 Aug 2011

As singleton01.py with
    version re-engineered with undefined setters = None
    and defaults with null setters
    also mtutils.empty() = None

02/01/2010:
    Exportables class defined as a subtype of Persistents
    Persistents _loadFile()/_unloadFile() renamed _load()/_unload() respectively

04/01/2010:
    Settings class defined with autoloader

02/03/2010 singleton03.py cloned from singleton02.py with:
    - Transients updated:
       - _mungeKey() slower but handles keys of any structure automatically sorting all components for consistency
       - _isMember() added for consistency with sdict._isMember() but exploiting _mungeKey()
    - index04.py Index exploits updated Transients

18/03/2010 singleton04.py cloned from singleton03.py with:
    - Settings loads config03 - with changed bnf file to support non-infered QueryExpression comperands

08/04/2010:
    - _Transients:
       - _getItem() inputs optional hardcoded default if softcoded one is missing
       - _incItem() defined with optional default setting
    - _Exportables._export() exploits Flatfile._setValue() - other code removed

09/04/2010 standardisation of getter/setter and attribution syntax:
    _get(), _set(), _update() and __init__() methods checked regarding attribution.
    General rule is to reserve getters and setters to externally accessible and decorated attributes.
    These can also be used for just in time attribution (though this isn't currently so outside of the former criteria).
    Attribute setting via _update and __init__ strictly for external accessible attributes.
    Code changed throughout to access all other undecorated attributes directly.
    Python property not currently used to map _get/_set to direct attribute access syntax.

19/04/2010 singleton05.py cloned from singleton04.py with:
    - Persistent Triple Stores supported in config04.dat

06/05/2010 singleton06.py cloned from singleton05.py with:
    - URI support exploited via updated imports

12/05/2010 singleton07.py cloned from singleton06.py with:
    - explicit alias_ontology support

12/06/2010 singleton08.py cloned from singleton07.py with:
    - folders re-configured

07/07/2010 singleton.py cloned from singleton08.py for SVN versioning

10/07/2010:
    - path switched to new location
    - user defined config variable substitution

12/07/2010:
    - imports adjusted to avoid circle with utils and debug
    - _Transients._interpretItem() added to support config variable interpretation within retrieved or supplied default values

27/08/2010 towards handling invalid default settings:
    - _interpretItem()
        - receives optional additional parameter to request both the supplied and the hardcoded default
          be returned with values interpretted.
        - offered now as an alternative to _getItem() rather than a wrapper for _getItem()

30/08/2010:
    - Transients._delItem() defined (needed for Query._solve() progress and results/failures cache maintenance
    - Transients._isMember() renamed _isUnique() to better denote function.

21/09/2010:
    - Transient._isUnique/_getMember() accept optional munge setting for geeater efficiency:
       - False (don't munge this key)
       - True (default - munge the key)

06/10/2010 automatically loads and "compiles" settings file if any constituent settings files are updated

20/08/2011 auto detection of softwarebase for installation portability

@author: Administrator
'''

import copy, time, re, os
from metabulate.utils.utils import Flatfile
from metabulate.utils.utils import sdict

# NOTE configfilepath (the full path to the config files) cannot be interpretted from settings as it required here for their access.
softwarebase    = re.sub('metabulate.*$','',os.path.abspath(__file__))
configfilesbase = softwarebase+'metabulate\\Files\\'
configfilepath  = configfilesbase+'Config'
loadtype = 'pyo'
imextype = 'dat'
resub    = re.compile('(\%([A-Za-z0-9\_\-]+)\%)')                                       # regex for user defined config var substitution

class _Transients(object):
    def __init__(self
                ,items=''
                 ):
        self._update(items=items)
    def __len__(self): return len(self._items)
    def _update(self
               ,items=None
               ):
        if items is not None: self._setItems(items)
    def _reset(self): self._items = sdict()
    def _setItems(self,items):
        if not items: self._items = sdict()
        elif isinstance(items,sdict):
            self._items = items
        return self._items
    def items(self):
        for key,val in self._items.items(): yield key,val
    def values(self):
        for val in self._items.values(): yield val
    def keys(self):
        for key in self._items.keys(): yield key
    def _isEmpty(self):
        if self._items: return False
        else: return True
    def _hasItems(self): return not self._isEmpty()
    def _hasKey(self,item): return item in self._items
    def _interpretItem(self,*args):
        # usage:
        #    alternative to _getItem() below
        #    always performs variable interpretation using Settings 'config' as the source
        #    with optional default should the supplied key not be found or should both
        #     the interpretted value matching this key and the default be required
        # inputs:
        #    args[0] - index key
        #    args[1] - default for missing key
        #    args[2] - if set to 2 returns both the interpretted key value (if found) and the default
        #              if set to 1 or missing returns a single interpretted value
        # returns:
        #    r       - single interpretted value from index if present or if not the interpretted default if supplied
        #                OR - if args[2] == 'pair'
        #              listed pair of values, 1st as above, followed by the interpretted default
        v = None
        if args:
            found = False
            if args[0] in self._items:
                v = self._items[args[0]]
                found = True
            elif len(args) > 1: v = args[1]
            else: None
            i = Settings()._getItem('config')
            if v is not None: v = i._doSubs(v)
            if len(args) > 2 and args[2] == 2:
                if found: v1 = i._doSubs(args[1])
                else: v1 = v
                return (v,v1)
        return v
    def _getItem(self,*args):
        # usage:
        #    gets an index value from its key or returns an optional supplied default
        #    with optional default and interpretter for performing variable substitutions
        # inputs:
        #    args[0] - key value
        #    args[1] - optional default value if key missing
        #    args[2] - optional Persistents to interpret any config variables in args[1] (usually set by _interpretItem() to 'config')
        # returns:
        #    value indexed by item if present otherwise default if supplied
        #    None if no args or no match and no default
        if args:
            if args[0] in self._items: v = self._items[args[0]]
            elif len(args) > 1: v = args[1]
            else: v = None
            if v is not None and len(args) > 2 and isinstance(args[2],_Persistents):
                v = args[2]._doSubs(args[1])                                            # do embedded (CONFIG post instantiation) var subs
            return v
    def _setItem(self,item,value):
        self._items[item] = value; return value
    def _delItem(self,item):
        try: del self._items[item]
        except: pass
    def _incItem(self,item):
        # usage:
        #    increments and returns item value by 1 if it exists and is incrementable
        #    if item doesn't exist sets value to 1 and returns
        #    elif non incrementable returns None
        # inputs:
        #    item - key value
        # returns:
        #    index value incremented or initialised to 1
        #    or if non incrementable returns None
        try: return self._setItem(item,int(self._getItem(item,0))+1)
        except: return None
    def _setMember(self,item,value):
        from metabulate.utils.utils import _mungeKey
        return self._setItem(_mungeKey(item),value)
        # usage:
        #    as _setItem() except it munges the item key first
    def _getMember(self,item,default=None,returnSet=None,dm=None,munge=True):
        # usage:
        #    gets an item from the index if present
        #    if not indexes it against its default, returning this
        #    otherwise returns None
        #    munges the index to ensure it can be hashed
        # inputs:
        #    item      - key whose value is to be retrieved
        #    default   - value to set a new key to if supplied
        #    returnSet - if None returns value if match found, else returns the default if applied
        #    dm        - dictionary or mtcollection munging mode ['keys'|'items'|'values']
        #    munge     - mungeKey [True|False]
        # returns:
        #    value for key if present, default if supplied and key not present, else None
        from metabulate.utils.utils import _mungeKey
        if munge: item = _mungeKey(item,dm)
        if item in self._items: return self._getItem(item,'')
        else:
            if default is not None:
                self._setItem(item,default)
                if returnSet is None: return None
                else: return default
    def _isUnique(self,item,default=None,dm=None,munge=True):
        # usage:
        #    variation of _getMember which only returns True (if not present) or False (if present)
        #    and optionally updates the index
        #    if item and not present and default supplied set it
        # inputs:
        #    item      - key whose value is to be retrieved
        #    default   - value to set a new key to if supplied
        #    dm        - dictionary or mtcollection munging mode ['keys'|'items'|'values']
        #    munge     - mungeKey [True|False]
        # returns:
        #    unique    - [True|False]
        unique = False
        from metabulate.utils.utils import _mungeKey
        if munge: item = _mungeKey(item,dm=dm)
        if not item in self._items:
            if default is not None: self._setItem(item,default)
            unique = True
        return unique
    def _length(self): return len(self._items)
    def _doSubs(self,v): return v
class _Persistents(_Transients):
    def __init__(self
                ,items=''
                ,file=''
                 ):
        _Transients.__init__(self, items=items)
        self._default_file = Flatfile(path=configfilepath
                                     ,name='singleton_index'
                                     ,type=loadtype
                                      )
        self._load(file=file)
    def _update(self
                ,items=None
                ,file=None
                ):
        if items is not None: self._setItems(items)
        if file  is not None: self._setFile(file)
    def _setFile(self, file):
        if not file: self._file = self._default_file
        elif isinstance(file,Flatfile): self._file = file
        return self._file
    def _getFile(self): return self._file
    def _load(self, file=None):
        self._update(file=file)
        file = self._getFile()
        if file: return self._setItems(file._load())
    def _unload(self, file=None):
        self._update(file=file)
        return self._getFile()._unload(self._items)
    def _doSubs(self,v):
        # usage:
        #    finds all embedded variables within input string v
        #    and substitutes their values whether these are defined
        # inputs:
        #    v  - value with optional embedded config variables
        # returns:
        #    v1 - value with any defined embedded config variables substituted for their values
        v1 = v                                                                          # value for user defined variable substitutions
        for (sub,key) in resub.findall(v):                                              # for each config variable to be substitued
            val = self._getItem(key)                                                    #  get value for this variable
            if val is None and key == 'softwarebase':                                   #  if softwarebase var is undefined:
                val = softwarebase                                                      #   set it from script variable
                self._setItem(key,val)                                                  #   and set it for future use
            if val is not None: v1 = v1.replace(sub,val)                                #  if var value defined: substitute it
        return v1
class _Exportables(_Persistents):
    def __init__(self
                ,items=''                                                               # instantiate an existing dict of items
                ,file=''                                                                # loadfile (pickled file to load)
                ,export=''                                                              # BNF file to import
                ,interpretter=''                                                        # BNF file values interpretter (if any)
                 ):
        _Persistents.__init__(self,items=items,file=file)
        self._default_export = Flatfile(path=configfilepath
                                       ,name='singleton_export'
                                       ,type=imextype
                                        )
        self._import(export=export,interpretter=interpretter)
    def _update(self
                ,items=None
                ,file=None
                ,export=None
                ):
        if items  is not None: self._setItems(items)
        if file   is not None: self._setFile(file)
        if export is not None: self._setExport(export)
    def _setItem(self,item,value):
        if (isinstance(item,basestring)
        and isinstance(value,basestring)):
            self._items[item] = value; return value
        else: return None
    def _setExport(self, export):
        if not export: self._export = self._default_export
        elif isinstance(export,Flatfile): self._export = export
        return self._export
    def _getExport(self): return self._export
    def _import(self, export=None, interpretter=None):
        # usage:
        #    imports a BNF export file of keys and values
        #    optionally interprets embedded variables within values against a supplied singleton
        # inputs:
        #    export       - BNF file to import
        #    interpretter - Persistents used to interpret embedded values
        # returns:
        #    items        - instantiated items dict
        if interpretter == 'self': interpretter = self
        self._update(export=export)
        export = self._getExport()
        if export:
            for pair in export._getValues():
                parts = pair.split('::-')
                for c in range(len(parts)): parts[c] = parts[c].replace('\\t','').strip()
                if isinstance(interpretter, _Persistents):
                    newval = interpretter._doSubs(parts[1])                             # do embedded variable substitutions
                self._setItem(parts[0], newval)
            return self._items
    def _export(self, export=None):
        self._update(export=export)
        export = self._getExport()
        ok = False
        if export:
            for item in self._items:
                if not export._setValue(value=item+' ::- '+self._getItem(item,'')
                                       ,luw=time.ctime()
                                        ): break
        return ok
class _Settings(_Persistents):
    def __init__(self
                ,items=''
                ,file=Flatfile(path=configfilepath
                              ,name='settings'
                              ,type=loadtype
                               )
                 ):
        _Persistents.__init__(self,items=items,file=file)
        # files
        sm = file._getModified()
        fs = ['config','alias_ontology','prefs','errors']
        fn = []
        fm = True
        for f in fs:
            f1 = Flatfile(path=configfilepath,name=f,type=imextype)
            fn += [f1]
            fm1 = f1._getModified()
            if f1._getModified() > sm: fm = False
        # initialise
        if not (sm and fm):
            for c,f in enumerate(fn):
                if not c: i = 'self'
                else: i = self._getItem('config')
                self._setItem(fs[c],_Exportables(interpretter=i,export=f))
            self._unload()

_transients = _Transients()
def Transients(): return _transients
_persistents = _Persistents()
def Persistents(): return _persistents
_exportables = _Exportables()
def Exportables(): return _exportables
_settings = _Settings()
def Settings(): return _settings

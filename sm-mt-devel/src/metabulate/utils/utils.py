'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

Created on 21 Dec 2009
utils04.py cloned from utils03.py on 19 Apr 2010
utils05.py cloned from utils04.py on 06 May 2010
utils06.py cloned from utils05.py on 13 May 2010
utils07.py cloned from utils06.py on 12 Jun 2010
utils.py cloned from utils07.py on 07 Jul 2010
Last Updated on 20 Oct 2010

As utils02.py with:
    version re-engineered with undefined setters = None
    and defaults with null setters
    also mtutils.empty() = None

02/01/2010:
    Flatfile._getValues() added reads values line by line from a file
     optionally stripping comments, whitespace and linefeeds

04/01/2010:
    _logical() converts common strings to (semantically) equivalent logical values (for greater API flexibility)

06/01/2010:
    _matchUnion() updated:
     - optionally handles NOT matching provided these trail all EQ matches
     - source documentation updated

14/01/2010:
    Flatfile._setValue() mode parameter. New method reset uses m rather than mode to avoid default reset.

16/01/2010:
    Configurable Exception Handling - exploits mterrors:
     - _pdepth() doesn't raise errors,
       instead it returns an error code so external calling routines can raise the errors instead
       to avoid circular imports with mterrors, mtsingleton

06/02/2010:
    sdict._invert() method to invert dictionary:
     - swaps keys and values
     - optional listvals=True param to retain listed unique values
     - initially exploited by Query._setMatch().doswap()

16/02/2010:
    sdict()._deepUnion() bug fix = deepcopy needed

24/02/2010:
    _stripsplit() defined to compile a list of stripped items from a string

27/02/2010:
    slist._intersection() method defined exploiting set.intersection()

28/03/2010:
    _mungeKey() returns str form of null inputs - needed to index these

02/04/2010:
    _flatten() defined to extract validated leaf elements from a list structure

05/04/2010:
    _genericSetter() defined to set or reset any validated instance variable from input or defined default
    _genericGetter() defined to get any instance value or if undefined optionally set its default

06/04/2010:
    _genericSetter() optionally inputs transformation function to be applied to validated setting(s)
      prior to instantiation as instance._attribute value.

07/04/2010:
    _genericSetter() supports information rich error notifications
    _flatten() accepts supplied defaults for additional attribute setting validation

08/04/2010 further _genericSetter() error notifications:
    - if no existing setting to default to after all supplied values fail: MissingAttributeError raised
    - exception handling simplified a little.

09/04/2010 standardisation of getter/setter and attribution syntax: (note only - nothing regarded as needed here)
    _get(), _set(), _update() and __init__() methods checked regarding attribution.
    General rule is to reserve getters and setters to externally accessible and decorated attributes.
    These can also be used for just in time attribution (though this isn't currently so outside of the former criteria).
    Attribute setting via _update and __init__ strictly for external accessible attributes.
    Code changed throughout to access all other undecorated attributes directly.
    Python property not currently used to map _get/_set to direct attribute access syntax.

10/04/2010 _getSubclasses() function defined.

19/04/2010 utils04.py cloned from utils03.py with:
    - Persistent Triple Stores supported
       - mtutils - enhanced _genericGetter()/_genericSetter() tests persistent _db[varname] as alternative to _varname attributes
       - new _deleteFiles() method defined supporting multiple file deletion
       - new ODBMS abstract superclass (for generalised isinstanceof testing of _db variables)

20/04/2010 Flatfile._setPath() set seperators according to os

06/05/2010 utils05.py cloned from utils04.py with:
    - URI support exploited via updated imports

13/05/2010 utils06.py cloned from utils05.py with:
    - explicit alias_ontology support (via imports)

12/06/2010 utils07.py cloned from utils06.py

07/07/2010 utils.py cloned from utils07.py for SVN versioning

02/08/2010 Flatstore terminator settings supported exploited by Content._termination()

03/08/2010 sdict._doSubs() uses self as a variable store and substitutes variables for values in a string

10/08/2010 slist._difference_update() added

24/08/2010 srbtree sdict compatability:
    - srbtree class added supporting:
        - autovivication
        - same value added methods as sdict
        - inherits from mtcollection
        - adds type specific _sameClassAs() and _create() methods for use by new mtcollection methods
    - mtcollection class defined:
        - sdict value add methods moved to here for shared inheritance by srbtree and sdict
        - methods exploit:
            - self._sameClassAs(collection) instead of _isinstance(sdict/rbtree,..)
            - self._create() instead of sdict/srbtree()
    - sdict:
        - value add methods moved to mtcollection
        - adds type specific _sameClassAs() and _create() methods for use by new mtcollection methods
    - Forwards compatability updates between P2.6/7 and P3
      in handling support of keys(), iteritems(), sort(), map(), itemgetter() and has_key().

27/08/2010 handles invalid default settings:
    - _genericSetter():
        - handling upgraded the check defaults against criteria
        - exploits default supplied as 2 values - the setting and the hardcoded backup if provided
    - _flatten():
        - will raise error if given a variable name and no supplied values matched the criteria
        - new InvalidSettingError raised and notified

30/08/2010 Refactoring:
    - mtcollection/Stack._isMember() renamed _isUnique() to better denote function.

02/09/2010 Refactoring:
    - _getClass(object) method added to get the class name string for an object instance

21/09/2010 _mungeKey() made more efficient, comprehensive and consistent:
    - supports mtcollection keys
    - supports range of index key settings

06/10/2010 Flatfile stats methods added:
    - _getModified() returns last modified time as Long or String
    - _getCreated()  returns created       time as Long or String
    - _getAccessed() returns last accessed time as Long or String
    - _getSize()     returns file size as int

20/10/2010 Flatfile._getValues():
    - strip parameter supports optional stripping either main of suffixed comments.
    - enhancement exploited by TripleStore._import()

@author: Administrator
'''

import os, pickle, re, copy, glob, stat, time

# REMEMBER other imports are made within the body of this source

logicals = {'y':True,'yes':True,'on':True,'true':True,'n':False,'no':False,'off':False,'false':False,'sentinel_none':None,'none':None}
objre = re.compile('^.*\.(.*) (instance|object) at .*$')                                # regex to extract a class name from an object string
clsre = re.compile('.*\'(.*)\.(.*)\'.*')                                                # regex to extract string form of class name group 1 - path, group 2 = class
resub = re.compile('(\%([A-Za-z0-9\_\-]+)\%)')                                          # regex for user defined config var substitution

class ODBMS: pass
class FlatStore:
    def __init__(self
                ,mode=''         # setValue mode default 'aw' for overwrite new and append, 'w' for overwrite, 'a' for append
                ,luw=''          # luw id used with mode = 'aw'
                ,terminator=None
                ):
        self._update(mode=mode,luw=luw,terminator=terminator)
    def _update(self, mode=None, luw=None, terminator=True):
        if mode       is not None: self._setMode(mode)
        if luw        is not None: self._setLuw(luw)
        if terminator is not True: self._setTerminator(terminator)
    def _setMode(self, mode):
        if not mode: self._mode = ''
        elif (isinstance(mode,basestring) and
            (mode == 'w'
          or mode == 'a'
          or mode == 'aw')): self._mode = mode
        return self._mode
    def _getMode(self): return self._mode
    def _setLuw(self, luw):
        if not luw: self._luw = ''
        elif isinstance(luw,basestring): self._luw = luw
        return self._luw
    def _getLuw(self): return self._luw
    def _setTerminator(self, terminator):
        if terminator is None or terminator is False: self._terminator = terminator
        elif isinstance(terminator,basestring): self._terminator = terminator
        return self._terminator
    def _getTerminator(self): return self._terminator
    def _interpretMode(self, mode, luw):
        # usage: processes mode and luw parameters and settings returning appropriate current mode
        #        interpetted in the context of the luw
        oluw = self._getLuw()                                                           # get last luw id
        self._update(mode=mode,luw=luw)                                                 # update with any changed mode or luw id
        mode = self._getMode()                                                          # get this mode
        luw = self._getLuw()                                                            # get this luw id
        if not mode: mode = 'aw'                                                        # default mode is overwrite new then append
        if mode == 'aw':                                                                # if overwrite new then append:
            if luw == oluw: mode = 'a'                                                  #  if same luw: append
            else: mode = 'w'                                                            #  else: overwrite
        return mode
class TextStore(FlatStore):
    def __init__(self, value=''):
        self._value = ''
        self._update(value=value)
    def _update(self, value=''):
        self._setValue(value)
    def _setValue(self, value, mode=None, luw=None):
        # usage: sets value according to mode interpretted in context of luw
        mode = self._interpretMode(mode,luw)                                            # get the file mode appropriate for this call
        if isinstance(value,basestring):
            if mode == 'a': self._value += value
            else: self._value = value
            return value
        else: return 0
    def _getValue(self): return self._value
    def _appendValue(self, value):
        if isinstance(value,basestring): self._setValue(self._getValue()+value)
        return self._getValue()
class Flatfile(FlatStore):
    def __init__(self, path='', name='', type='', mode='', luw='', terminator=None):
        FlatStore.__init__(self)
        self._update(path=path,name=name,type=type,mode=mode,luw=luw,terminator=terminator)
    def _update(self, path=None, name=None, type=None, mode=None, luw=None, terminator=True):
        if path       is not None: self._setPath(path)
        if name       is not None: self._setName(name)
        if type       is not None: self._setType(type)
        if mode       is not None: self._setMode(mode)
        if luw        is not None: self._setLuw(luw)
        if terminator is not True: self._setTerminator(terminator)
    def _setPath(self, path):
        if not path: self._path = ''
        elif isinstance(path,basestring):
            if os.name == 'nt': f = '/'; t = '\\'                                       # get correct path separators for os - Windows
            else: f = '\\'; t = '/'                                                     # or UNIX style
            path = path.replace(f,t)                                                    # replace wrong separators
            if path[:-len(t)] != t: path += t                                           # add missing trailing separator
            self._path = path
        return self._path
    def _getPath(self): return self._path
    def _setName(self, name):
        if not name: self._name = ''
        elif isinstance(name,basestring): self._name = name
        return self._name
    def _getName(self): return self._name
    def _setType(self, type):
        if not type: self._type = ''
        elif isinstance(type,basestring): self._type = type
        return self._type
    def _getType(self): return self._type
    def _getFullname(self,existing=''):
        fn = self._getPath()+self._getName()+'.'+self._getType()
        if not existing or os.path.exists(fn): return fn
        else: return 0
    def _getModified(self,str=False):
        fn = self._getFullname(existing='y')
        if fn:
            mt = os.stat(fn)[stat.ST_MTIME]
            if str: return time.ctime(mt)
            else: return mt
        else: return None
    def _getCreated(self,str=False):
        fn = self._getFullname(existing='y')
        if fn:
            mt = os.stat(fn)[stat.ST_CTIME]
            if str: return time.ctime(mt)
            else: return mt
        else: return None
    def _getAccessed(self,str=False):
        fn = self._getFullname(existing='y')
        if fn:
            mt = os.stat(fn)[stat.ST_ATIME]
            if str: return time.ctime(mt)
            else: return mt
        else: return None
    def _getSize(self):
        fn = self._getFullname(existing='y')
        if fn: return os.stat(fn)[stat.ST_SIZE]
        else: return None
    def _appendValue(self, value):
        # usage: appends file contents creating the file if it doesn't exist
        if isinstance(value,basestring):
            fn = self._getFullname()
            if fn:
                f = open(fn, 'a')
                f.write(value)
                f.close()
                return value
        return 0
    def _setValue(self, value='', mode='', luw=''):
        # usage: sets value of file contents according to mode interpretted in context of luw
        m = self._interpretMode(mode,luw)                                               # get the file mode appropriate for this call
        if isinstance(value,basestring):
            fn = self._getFullname()
            if fn:
                f = open(fn,m)
                f.write(value)
                f.close()
                return value
        return 0
    def _resetValue(self, value=''):
        # usage: set file contents creating the file if it doesn't exist
        if isinstance(value,basestring):
            fn = self._getFullname()
            if fn:
                f = open(fn, 'w')
                f.write(value)
                f.close()
                return value
        return 0
    def _getValue(self):
        fn = self._getFullname(existing='y')
        if fn:
            f = open(fn, 'r')
            value = f.read()
            f.close()
            return value
        return 0
    def _load(self):
        fn = self._getFullname(existing='y')
        object = False
        if fn:
            f = open(fn,'r')
            object = pickle.load(f)
            f.close()
        return object
    def _unload(self, object):
        fn = self._getFullname()
        if fn:
            f = open(fn,'w')
            pickle.dump(object,f)
            f.close()
            return 1
        else: return 0
    def _getValues(self,strip=['main','suffix']):
        fn = self._getFullname(existing='y')
        if fn:
            f = open(fn, 'r')
            if 'suffix' in strip: stripcomments = re.compile('\#\.\..+?$')            # suffix comments start with #.. (note must be #.. not #.)!
            else: stripcomments = None
            try:
                for value in f:
                    if 'main' not in strip or not value.startswith('#'):
                        if stripcomments is not None:
                            value = stripcomments.sub('',value)                         #  strip suffixed comments
                        value = value.rstrip()                                          #  strip whitespace and newline
                        if value: yield value
            finally: f.close()

class Empty: pass
    # instantiate as a null object

# Note definitions ABOVE this CANNOT use Debug class

from debug import Debug

# Note definitions BELOW CAN use Debug class
def _deleteFiles(pattern):
    try:
        for fn in glob.glob(pattern): os.remove(fn)
    except: pass
def _stripsplit(s,sep=','):
    l = slist()
    if isinstance(s,basestring) and isinstance(sep,basestring):
        for i in s.split(sep):
            i = i.strip()
            if i: l += [i]
    return l
def _logical(value):
    if isinstance(value,basestring):
        value1 = value.lower()
        if value1 in logicals: value = logicals[value1]
    return value
def _intersect(*args):
    # usage: input lists within lists of any number and any depth
    #        output single intersection list
    res = []
    if isinstance(args[0],list):
        if len(args) == 1: res = _intersect(*args[0])
        elif len(args) > 1: res = _doIntersect(*args)
    return res
def _doIntersect(*args):
    if len(args) > 1:
        res = []
        for x in args[0]:
            if x in args[1]: res.append(x)
        if len(args) > 2: return _doIntersect(res, *args[2:])
        else: return res
def _pdepth(s,ps=['('],pe=[')'],excl=True):
    # usage:
    #    checks parenthesis balancing in a string
    # inputs:
    #    s    = string to be checked
    # optional inputs:
    #    ps   = list of starting parenthesis
    #    es   = list of matching ending parenthesis
    #    excl = [True|False] If True excludes non-reportable look forward groups from final counts ie (?: ...)
    # returns:
    #    pc   = list of parenthesis counts for each supplied parenthesis type
    #    ec   = error code. (0 - none, 1 - UnspecifiedParenthesisError, 2 - UnbalancedParenthesisError
    # note:
    #    raise errors via return codes here to avoid circular includes
    #    does not cope with all regex expressions for example ORed alternatives. For this reason maxp is no longer exploited for regex evaluation
    pc = slist()
    ex = slist()
    if len(ps) != len(pe) or len(ps) == 0: ec = 1                                       # raise UnspecifiedParenthesisError()
    else:                                                                               # or proceed:
        ec = 0                                                                          #  set error code to ok (so far)
        pcount = slist()
        for c in range(len(ps)): pc[c] = 0; ex[c] = 0; pcount[c] = 0
        c = -1
        while c+1 < len(s):
            c += 1
            if s[c] == '\\': c += 1
            else:
                c1 = -1
                while c1+1 < len(ps):
                    c1 += 1
                    if s[c] == ps[c1]:
                        pcount[c1] += 1; pc[c1] += 1
                        if excl and s[c:(c+3)] == ps[c1]+'?:':
                            ex[c1] += 1
                    elif s[c] == pe[c1]: pcount[c1] -= 1
        for c,p in enumerate(pcount):
            if p != 0: ec = 2; break                                                    # raise UnbalancedParenthesisError(s)
            else: pc[c] -= ex[c]
    return ec,pc
def _splitRegex(r):
    ep = []
    lc = 0
    c = -1
    while c+1 < len(r):
        c += 1
        if r[c] == '\\/': c += 2
        elif r[c] == '\\': c += 1
        elif r[c] == '/':
            if lc > 0: ep += [r[lc:c].replace('\\/','/')]
            lc = c+1
    return ep
def _evalRegex(s,re,ep=[]):
    # usage evaluates a regular expression against a string performing substitutions as required
    # inputs:
    #    s    = string to be processed
    #    re   = compiled regex object
    # optional inputs:
    #    ep   = regex parts [0] - match expression, [1] - substitution expression
    # returns:
    #    s0   - match
    #    s1   - substitution
    gr = slist()
    ig = [re.match(s).group(0)]+list(re.match(s).groups())
    c = pc = len(ig)-1
    if len(ep) == 0 and c < 2: x = 2-c
    else: x = 0
    while c+x > -1:
        if c < 0: c1 = 0
        else: c1 = c
        gr[c+x] = ig[c1]
        c -= 1
    if len(ep) > 1:
        s0 = gr[0]
        s1 = ep[1]
        for c in range(pc,-1,-1):
            s1 = s1.replace('$'+str(c),gr[c])
    else: s0 = gr[1]; s1 = gr[2]
    return s0,s1
def _isEtype(s,c):
    # is evaluated type
    # usage:
    #    isinstance wrapper supporting evaluated instance checking
    #    where the evaluated string may be undefined
    # inputs:
    #    s - string to evaluate
    #    c - class type to check
    # returns:
    #    true - evaluated object
    #    falso - 0
    try:
        o = eval(s)
        if isinstance(o,c): return o
        else: return 0
    except: return 0
def _stripCollection(l,thin=False):
    # usage:
    #    strips aribitrary collections of whitespace double quotes and solitary leaf collections
    l1 = copy.deepcopy(l)
    if isinstance(l1,basestring): l1 = _stripString(l1)
    elif (len(l1) == 1
      and thin
      and isinstance(l1[0],basestring)
          ): l1 = _stripString(l1[0])
    elif isinstance(l1,dict):
        for k,v in l1.items():
            del l1[k]
            k1 = _stripCollection(k,thin=thin)
            v1 = _stripCollection(v,thin=thin)
            l1[k1] = v1
    else:
        if not isinstance(l1,list): l1 = list(l1)
        for c,v in enumerate(l1): l1[c] = _stripCollection(v,thin=thin)
        if not isinstance(l,list):
            if isinstance(l,tuple): l1 = tuple(l1)
            elif isinstance(l,set): l1 = set(l1)
    return l1
def _mungeKey(key,dm=None):
    # usage:
    #    ensures the key is hashable, by recursively checking for lists
    # note:
    #    currently doesn't handle keys with nested dictionaries - but see sdict._isMember() to implement this
    def mungeKey(key,dm):
        if isinstance(key,basestring):
            if key: key1 = _stripString(key)
            else: key1 = key
        elif key is False or key is None or key is True: key1 = str(key)
        else:
            keys = None
            if isinstance(key,dict): keys = [k for k in sorted(key)]
            elif (isinstance(key,list)
               or isinstance(key,tuple)
               or isinstance(key,mtcollection)
                  ): keys = key
            if keys is not None:
                key1 = []
                for k in keys:
                    if isinstance(key,tuple) or isinstance(key,list): key1 += [mungeKey(k,dm)]
                    elif dm == 'keys': key1 += [k]
                    else:
                        v = mungeKey(key[k],dm)
                        if dm == 'values': key1 += [v]
                        else: key1 += [(k,v)]
                if isinstance(key,list): key1 = str(key1)
                else: key1 = tuple(key1)
            else: key1 = ''
        return key1
    if (dm is None
     or not isinstance(dm,basestring)
     or (dm != 'items' and dm != 'keys' and dm != 'values')
       ): dm = 'items'
    key1 = mungeKey(key,dm)
#    print ('mungeKey; key1=',key1)
    return key1
def _isstrnum(s,default=None):
    # usage
    #    checks if string s represents a number
    #    if default is None returns [True|False]
    #    else if True retruns the value or if False the default
    if default is None: r = False
    else: r = default
    try:
        r = float(s)
        if default is None: r = True
    except ValueError: pass
    return r
def _isstrint(s,default=None):
    # usage
    #    checks if string s represents an integer
    #    if default is None returns [True|False]
    #    else if True retruns the value or if False the default
    if default is None: r = False
    else: r = default
    try:
        i = float(s)
        if not (i%1):
            if default is None: r = True
            else: r = i
    except ValueError: pass
    return r
def _isstrpercentage(s,default=None):
    # usage
    #    checks if string s represents a percentage
    #    if default is None returns [True|False]
    #    else if True retruns the value or if False the default
    if default is None: r = False
    else: r = default
    try:
        i = float(s)
        if (i >= 0 or i <= 100):
            if default is None: r = True
            else: r = i
    except ValueError: r = False
    return r
def _flatten(l,t=None,m=None,d=None,logical=False,ev=None,lv=None):
    # usage:
    #    filters unique instances of a given class from anywhere within an arbitrary structure
    #    typical usage for validating list setter input
    # inputs:
    #    l       - arbirarily nested list structure
    #    t       - one or more types - class(es) to be filtered, OR
    #    m       - membership values - one or more acceptable match values , OR neither
    #    d       - default value (for validation of defaults)
    #    logical - logical value (to be processed by _logical())
    #    ev      - supply the attribute name if an error is to be generated
    #    lv      - current recursion level (used to ensure default is only applied at level 0)
    # returns:
    #    l1      - list of unique extracted objects
    def flatten1(l,i,t,m,logical):
        # usage:
        #    sub function of flatten to verify a leaf value
        # inputs:
        #    l       - list of unique verified args
        #    i       - arg to verify
        #    t       - ok type or types of i
        #    m       - ok values of i
        #    logical - [True|False] if True apply logical transforms to i prior to validation
        # returns:
        #    l       - updated list of unique verified args
        #    sok     - Supplied values OK [True|False]
        ok  = False
        if logical: i = _logical(i)                                                     # if logical do a logical transform
        if t:                                                                           # if types validations are supplied:
            for c in t:                                                                 #  check at least 1 is satisfied
                if (
                    (isinstance(i,basestring)
                 and isinstance(c,basestring)
                 and c[:6] == '_isstr' and eval(c+'("'+i+'")')
                    )
                or ((c is None and i is None)
                 or (c is not None and isinstance(i,c))
                    )
                   ):
                    ok  = True
                    break
        elif m:                                                                         # elif match values supplied
            if i in m: ok = True                                                        #  check at least 1 is satisfied
        else: ok = True                                                                 # else no validations so value is ok
        if ok and i not in l: l += [i]                                                  # if an ok value found and not in list: add it
        return l                                                                        # return updated validated value list
    if lv is None: lv = 0
    l1 = []                                                                             # prepare found attributes list
    if t:                                                                               # prepare validation lists for:
        if not isinstance(t,list): t = [t]                                              #  types or
    elif m and not isinstance(m,list): m = [m]                                          #  members
    for i in l:                                                                         # for each supplied element:
        if isinstance(i,list):                                                          #  if a list flatten it
            for i1 in _flatten(i,t=t,m=m,d=d,logical=logical,ev=ev,lv=lv+1):            #   and collate validated matches
                l1 = flatten1(l1,i1,t,m,logical)                                        #   (can't use union because dicts might be target of selection)
        else: l1 = flatten1(l1,i,t,m,logical)
    if not l1 and not lv and d != l[0]:                                                 # no valid supplied values and at level 0:
        if ev is not None:                                                              #  if error variable is named:
            import metabulate.utils.errors as mterrors                                  #   prepare to report an error
            try:                                                                        #   try: (raise and catch the error)
                raise mterrors.InvalidSettingError(ev,l[0],d)                           #    raise the error(varname, value, default used)
            except mterrors.AttributionError, X:                                        #   and except to trap the raised error
                X._notify(c='mtutils',
                          m='_genericSetter()')                                         #    notify InvalidSettingError with params
        if d is not None: l1 = [d]                                                      #  catch all if a default is supplied: use it
    return l1

def _genericSetter(obj,var,vals,m=None,t=None,logical=False,plural=False,f=None,fobj=None):
    # usage:
    #    generalised setter with rich error notifications
    #    will support calling method args present or missing in singular or listed form
    #    will verify supplied values by type, membership or logical value
    #    if no value supplied the default is restored
    #    if values are supplied, those that are valid will be set
    #    else if supplied values are all invalid, it will use existing value if set, or set the default
    # inputs:
    #    obj     - calling object
    #    var     - instance variable to be set (this is the variable name without the prefix 'self._')
    #    vals    - list of setter values
    #    m       - membership values to be validated (single value or list of values) OR
    #    t       - types to be validated (single type or list of types)
    #    logical - is this a string representing a logical value [True|False] - ie. are values to be processed by _logical() before validation?
    #    plural  - [True|False] ie. single or multiple values expected
    #    f       - optional function expressed as a string (e.g. 'f(i)') to transform variable instances i or whole variable v
    #    fobj    - optional object for which function f is invoked
    # returns:
    #    v       - set value or None if nothing set
    # Notes:
    #    1) assumed defaults comply with naming convention self._default_varname
    #    2) functions may appy either to args list or each instance in args list by expressing as follows:
    #        f(v) - where v is the args list, f(i) - where i is each args instance
    default = False                                                                     # assume default isn't applied
    import metabulate.utils.errors as mterrors                                          #   prepare to report attribute instantiation error
    cl = _getClass(obj)                                                                 #    extract calling class from obj
    if vals:                                                                            # if values supplied: (proceed to attempt instantiation)
        v = _flatten(vals,m=m,t=t,logical=logical)                                      #  filter valid values from those supplied
        if not v:                                                                       #  if no valid values: (proceed to issue error and try handling)
            try:                                                                        #   try block to raise the error
                ev = _flatten(vals)                                                     #    get input vals without wrapping
                if not plural: ev = ev[0]
                raise mterrors.SuppliedAttributeValueError(cl,'_'+var,ev)               #    raise the error
            except mterrors.SuppliedAttributeValueError, X:                             #   trap the raised error
                X._notify(c='mtutils',
                          m='_genericSetter()')                                         #    notify SuppliedAttributeValueError with params
            try:                                                                        #   try block to catch error (if any) in nested try block
                try:
                    db = None
                    db = obj._db
                    v = db[var]
                except:
                    if db: raise mterrors.AttributeMissingError(cl,'_'+var)
                    try: v = [getattr(obj,'_'+var)]                                     #    try getting existing value (if any)
                    except AttributeError:
                        raise mterrors.AttributeMissingError(cl,'_'+var)                #    except raise the error with paramters
            except mterrors.AttributeMissingError, X:                                   #   and except to trap the raised error
                X._notify(c='mtutils',
                          m='_genericSetter()')                                         #    notify SuppliedAttributeValueError with params
                default = True                                                          #    flag for default
    else: default = True                                                                # else no values supplied: flag apply default
    try:                                                                                # try: (applying found value(s) or default)
        if default:                                                                     #  if appy default:
            dv = '_default_'+var                                                        #   derive the default attribute name
            try:                                                                        #   try: (using the default attribute)
                d = getattr(obj,dv)                                                     #    get default attribute value if set
                if isinstance(d,tuple) and len(d) == 2: df = d[0]; hdf = d[1]           #    differentiate between settings and
                else: df = d; hdf = None                                                #     and hardcoded defaults if supplied
                v = _flatten([df],m=m,t=t,d=hdf,logical=logical,ev=var)                 #    filter valid values from the default (with logical tranforms if needed)
            except AttributeError:                                                      #   except no such default: (proceed to raise error and apply null)
                raise mterrors.DefaultAttributeMissingError(cl,dv)                      #    raise the error with paramters
        if v:                                                                           #  if valid value exists: (proceed to transform &/or instantiate)
            if f:                                                                       #   if transform function supplied:
                f = f.strip()                                                           #    remove whitespace from function name
                if fobj: f1 = 'fobj.'+f                                                 #    prefix with function object
                else: f1 = f                                                            #    or not..
                try:                                                                    #    try applying the function
                    if f[-2] == 'v': v = eval(f1)                                       #     if function apply to whole value: evaluate whole
                    else:                                                               #     else:
                        for c,i in enumerate(v): v[c] = eval(f1)                        #      collate function evaluations for each item
                except:                                                                 #    except function application failed:
                    fcl  = _getClass(fobj)                                              #     extract the function calling class from fobj
                    raise mterrors.AttributeTransformationFailure(cl,'_'+var,fcl,f,v)   #     raise the error with parameters
            if v and isinstance(v,list) and not plural: v = v[0]                        #  if singular instantiation: use the first in the list
    except mterrors.AttributionError, X:                                                # except trap any raised AttributionError
        X._notify(c='mtutils',
                  m='_genericSetter()')                                                 #  notify DefaultAttributeMissingError with params
        v = ''                                                                          #  default attribute to null value
    try:
        db = obj._db
        if not isinstance(db,ODBMS): raise mterrors.AttributeMissingError
        db[var] = v
    except:
        setattr(obj,'_'+var,v)                                                          # instantiate the attribute value (supplied, existing, default or null)
    return v                                                                            # and return it
def _genericGetter(obj,var,default):
    # usage:
    #    generalised getter
    #    gets obj._var optionally setting the default value if var not yet defined
    # inputs:
    #    obj     - calling object
    #    var     - instance variable to be set (this is the variable name without the prefix 'self._')
    #    default - [True|False|unistantiated_return_value] - if True applies the default value if var not yet defined
    # returns:
    #    v       - set value for var or None if nothing set
    # Note:
    #    default = True processing assumed obj set method complies with naming convention self._setVarname() where Varname is var.capitalize()
    v = None
    try:
        db = obj._db
        if not isinstance(db,ODBMS): raise mterrors.AttributeMissingError
        try: v = db[var]
        except:
            if default is True: v = eval('obj._set'+var[0].upper()+var[1:]+'()')
            elif default is not False: v = default
    except:
        try: v = getattr(obj,'_'+var)
        except AttributeError:
            if default is True: v = eval('obj._set'+var[0].upper()+var[1:]+'()')
            elif default is not False: v = default
    return v
def _getClass(obj):
    # usage:
    #    returns the class name of obj as a String
    # inputs:
    #    obj - object instance
    # returns:
    #    cls - class of obj as a String or None
    try: cls = objre.match(str(obj)).group(1)                                           #    extract calling class from obj
    except: cls = None
    return cls
def _getSubclasses(cls,incSelf=False,asString=True,withPath=False):
    # usage:
    #    gets unique subclasses of a class in various forms
    # inputs:
    #    cls       - root class
    #    incSelf   - include root class in returned list [True|False]
    #    asString  - return list of class strings [True|False]. If False returns class objects
    #    withPath  - include the class path in returned strings [True|False]. If False returns just the class name
    # returns:
    #    scls      - list of unique subclasses in specified format. If none returns empty list.
    def showSubclass(cls,asString,withPath):
        if not asString: return str(sub)
        else:
#            clas = clsre.match(str(sub)).group(2)
            clas = sub.__name__
            if withPath: clas = clsre.match(str(sub)).group(1)+'.'+clas
            return clas
    # End showSubclass
    scls = slist()
    if isinstance(cls,type):
        try: subs = cls.__subclasses__()
        except TypeError: subs = cls.__subclasses__(cls)
        for sub in subs:
            if sub not in scls: scls = scls._union(_getSubclasses(sub))
            scls += [showSubclass(scls,asString,withPath)]
        if incSelf and cls not in scls: scls += [showSubclass(cls,asString,withPath)]
    return scls

def _stripString(s):
    if isinstance(s,basestring):
        s = s.strip()
        if (s[0] == s[-1] and
            (s[0] == "'" or s[0] == '"')):
            s = s[1:-1]
    return s

class ref():
    # simulates pointers
    def __init__(self,obj): self._obj = obj
    def _setObj(self,obj): self._obj = obj; return self._obj
    def _getObj(self): return self._obj
class slist(list):
    def _showDebug(self,
                   clas='',
                   method='',
                   note='',
                   vars=[],
                   line='',
                   level=2):
        Debug()._notify(clas=clas,method=method,note=note,line=line,level=level,vars=vars)
    def __getitem__(self, l):
        if type(l) is not tuple: self._autovivify(l)
        return list.__getitem__(self, l)
    def __setitem__(self, l, o):
        if type(l) is not tuple: self._autovivify(l)
        return list.__setitem__(self, l, o)
    def _autovivify(self, l):
        if l < 0: return
        l1 = len(self)
        if l1 <= l: self.extend(['']*(l-l1+1))
    def _contents(self, quotes='', ending='\n', sep=', ', last_sep=' and '):
        s = ''
        l = len(self)
        if l < 1: return s
        for c,i in enumerate(self):
            s += quotes+str(i)+quotes
            if c+2 < l: s += sep
            elif c+2 == l: s += last_sep
            else: s += ending
        return s
    def _union(self,l): return slist(set(self).union(set(l)))
    def _intersection(self,l): return slist(set(self).intersection(set(l)))
    def _difference(self,l): return slist(set(self).difference(set(l)))
    def _symmetric_distance(self,l): return slist(set(self).union(set(l))-set(self).intersection(set(l)))
    def _difference_update(self,l): return slist(set(self).difference_update(set(l)))
    def _removelist(self,l):
        if isinstance(l,list):
            for i in l:
                if i in self: self.remove(i)
        return self
    def _isSupersetOf(self,l):
        if len(self._intersection(l)) == len(l): return True
        else: return False
    def _isSubsetOf(self,l):
        if len(self._union(l)) == len(l): return True
        else: return False
    def _peel(self, leave=0):
        # usage
        #    removes superfuous outer list nestings
        # inputs:
        #    leave = minimum inner nesting to remain
        #            default of zero strips all inner nestings
        self._showDebug(clas='slist',method='_peel',note='inputs',line=867,level=0,vars=[['self',self],['leave',leave]])
        if len(self) == 1:
            if isinstance(self[0],list):
                self = slist(self[0])._peel(leave=leave)
            if leave and not (isinstance(self[0],list) or
                              isinstance(self[0],tuple)):
                for l in range(leave):
                    self = slist([self])
                    self._showDebug(clas='slist',method='_peel',note='unpeeling',line=875,level=1,vars=[['self',self]])
        self._showDebug(clas='slist',method='_peel',note='returns',line=876,level=0,vars=[['self',self]])
        return self

class islist(slist):
    # usage:
    #    indexed slist - potentially exploited for Queryables ikeys recursive keys list testing
    #    supports all functions of slist plus indexed presence, retrieval and loop testing
    #    primary cost is performance on deletion
    # note:
    #    almost identical to osdict except:
    #     - doesn't support storage of key:value pairs
    #     - does allow duplicate values in list
    #     - value sequence repetition supported and detectable see _loops()
    def __init__(self,*args):
        self._psn = sdict()
        if not args: slist.__init__(self)
        else:
            l = args[0]
            slist.__init__(self,l)
            if l and isinstance(l,list):
                for o,i in enumerate(l):
                    if i in self._psn: self._psn[i] += [o]
                    else: self._psn[i] = [o]
    def __setitem__(self,o,i):
        if i in self._psn and o not in self._psn[i]: self._psn[i] += [o]
        else: self._psn[i] = [o]
        slist.__setitem__(self,o,i)
    def __delitem__(self,o):
        if (type(o) == type(1)
        and o >= 0
        and o < len(self)
            ):
            done = sdict()
            for i in self[o:]:
                if i not in done:
                    ol = []
                    for p in self._psn[i]:
                        if p != o:
                            if p > o: p -= 1
                            ol += [p]
                    if ol: self._psn[i] = ol
                    else: del self._psn[i]
                    done[i] = ''
            list.__delitem__(self,o)
    def __iadd__(self,l):
        if isinstance(l,list):
            o = len(self)
            for i in l:
                self.__setitem__(o,i)
                o += 1
        return self
    def __contains__(self,i):
        return i in self._psn
    def remove(self,i):
        l = copy.deepcopy(self)
        if i in self._psn:
            ol = self._psn[i]
            for c in range(len(ol)-1,-1,-1):
                del l[ol[c]]                   # for some reason ol won't reverse sort!?!
        return l
    def _getOffset(self,i):
        # usage:
        #    gets offsets of item self (found by value)
        # inputs:
        #    i - item value
        # returns:
        #    ordered list of offsets at which this value appears in self
        if i in self._psn: return self._psn[i]
        else: return None
    def _loops(self,i,minspan=0):
        # usage:
        #    tests if item would cause a sequence of values to loop in self
        #    example: adding 4 to ...1,2,3,4,1,2,3 would loop on 1,2,3,4
        #             adding 3 to ...1,2,3,4,1,2 doesn't loop on anything although 3 is already present
        # inputs:
        #    i - item value to test
        # returns:
        #    r - if True would cause a value loop or
        #        if False would not cause a value loop
#        print ('minspan=',minspan)
        r = False
        if i in self._psn:
            l  = len(self)
            ol = self._psn[i]
            c = len(ol)
#            print ('ol=',ol,'c=',c,'l=',l,'ol[c-1]=',ol[c-1],'l-minspan=',l-minspan)
            while c-1 >= 0 and ol[c-1] >= l-minspan:
                c -= 1
#                print ('ol[c-1]=',ol[c-1],'l-minspan=',l-minspan)
#            print ('c=',c)
            if c > 0:
                p1 = ol[c-1]
                p0 = 2*p1-l
#                print ('p1=',p1,'p0=',p0)
                while (p1+1 < len(self)
                   and p0+1 >= 0
                   and self[p0+1] == self[p1+1]
                       ):
                    p0 += 1
                    p1 += 1
                if p1+1 == len(self): r = True
        return r
    def _showDebug(self,
                   clas='',
                   method='',
                   note='',
                   vars=[],
                   line='',
                   level=2):
        Debug()._notify(clas=clas,method=method,note=note,line=line,level=level,vars=vars)

class mtcollection(object):
    def _yieldMatch(self,s,e,keys,bound):
        # uasage:
        #    inputs as self a multilevel sdict of arbitrary depth
        #     from which it yields lists of keys between depths s(tart) and e(nd) matching supplied list of keys
        #     base method from which Sotre._solveTriple1 was spawned, unlike which this method will work for any
        #     multilevel dictionary, but it is however ignorant of the sementics of triples (e.g. nested triples)
        self._showDebug(clas='mtcollection',method='_yieldMatch',note='inputs',line=994,level=0,vars=[['self',self],['s',s],['e',e],['keys',keys],['bound',bound]])
        o = slist()
        b = slist()
        if e > 0:
            if keys: this = keys[0]
            else: this = self
            self._showDebug(clas='mtcollection',method='_yieldMatch',line=1000,level=1,vars=[['this',this],['self',self]])
            c = -1
            for dummy in this:
                if keys and dummy == '*': bv = ''; this1 = self
                elif keys and dummy[:1] == '?': bv = dummy[1:]; this1 = self
                else: this1 = [dummy]; bv = ''
                self._showDebug(clas='mtcollection',method='_yieldMatch',line=1006,level=1,vars=[['bv',bv],['this1',this1]])
                for k in this1:
                    self._showDebug(clas='mtcollection',method='_yieldMatch',line=1008,level=1,vars=[['k',k]])
                    c += 1
                    self._showDebug(clas='mtcollection',method='_yieldMatch',line=1010,level=1,vars=[['e',e],['c',c],['keys',keys],['bv',bv],['bound',bound]])
                    b1 = self._create()
                    b1 = srbtree()
                    if keys and bv:
                        b1[bv] = k
                        self._showDebug(clas='mtcollection',method='_yieldMatch',line=1015,level=2,vars=[['b1',b1]])
                        self._showDebug(clas='mtcollection',method='_yieldMatch',line=1016,level=2,vars=[['c',c]])
                    if c >= len(bound[0]) or not bound[0][c]:
                        bound[0] = slist(bound[0])
                        bound[0][c] = {}
                    ok = 1
                    if b1 or bound[0][c]:
                        self._showDebug(clas='mtcollection',method='_yieldMatch',line=1022,level=2,vars=[['bound[0][c]',bound[0][c]]])
                        b1 = b1._matchUnion(bound[0][c])
                        if not b1: ok = 0
                    if ok:
                        bound[0][c] = b1
                        self._showDebug(clas='mtcollection',method='_yieldMatch',line=1027,level=2,vars=[['b1',b1],['bound[0][c]',bound[0][c]]])
                        if e > 1:
                            self._showDebug(clas='mtcollection',method='_yieldMatch',line=1029,level=2,vars=[['self[k]',self[k]]])
                            self._showDebug(clas='mtcollection',method='_yieldMatch',line=1030,level=2,vars=[['keys[1:]',keys[1:]]])
                            self._showDebug(clas='mtcollection',method='_yieldMatch',line=1031,level=2,vars=[['bound[1:]',bound[1:]]])
                            self[k]._addDebug(4,self._getDebug(4))
                            for o,b in self[k]._yieldMatch(s-1,e-1,keys[1:],bound[1:]):
                                self._showDebug(clas='mtcollection',method='_yieldMatch',line=1034,level=1,vars=[['o',o],['b',b],['b1',b1],['s',s],['e',e]])
                                ok = 1
                                if b1 or b:
                                    b = b._matchUnion(b1)
                                    if not b: ok = 0
                                if ok:
                                    if s < 1: o[0:0] = [k]
                                    self._showDebug(clas='mtcollection',method='_yieldMatch',note='yields',line=1041,level=0,vars=[['o',o],['b',b]])
                                    yield o,b
                                    self._showDebug(clas='mtcollection',method='_yieldMatch',line=1043,level=1,vars=[['e',e],['b1',b1]])
                        else:
                            self._showDebug(clas='mtcollection',method='_yieldMatch',note='yields',line=1045,level=0,vars=[['k',k],['b1',b1],['e',e]])
                            yield [k],b1
    def _invert(self,listvals=True):
        # usage:
        #    inverts a collection
        #    ie. swaps keys and values
        # inputs:
        #    listvals - optional (True|False)
        #               if True retains as values in inverted dict a list of all unique keys for the value
        #               ie: {a1:[a],b1:[b,c]} = {a:a1,b:b1,c:b1}._invert(listvals=True)
        # returns:
        #    d        - self inverted
        def listval(d,k,v):
            try:
                if k not in d: d[k] = [v]
                elif v not in d[k]: d[k] += [v]
            except TypeError:
                if str(k) not in d: d[str(k)] = [v]
                elif v not in d[str(k)]: d[str(k)] += [v]
            return d
        d = self._create()
        if listvals:
            for k,v in self.items():
                if isinstance(v,list):
                    for i in v: d = listval(d,i,k)
                else: d = listval(d,v,k)
        else:
            for k,v in self.items():
                if isinstance(v,list):
                    for i in v:
                        try: d[i] = k
                        except TypeError: d[str(i)] = k
                else:
                    try: d[v] = k
                    except TypeError: d[str(v)] = k
        return d

    def _deepUnion(self,d,replace=False):
        # merges nested dictionaries of arbitrary depth and structure
        # eg where:
        #  i  = {'a': ['a1', 'a2'], 'c': {'c2': 'vc2', 'c1': 'vc1'}, 'b': ['b1', 'b2'], 'd': ['ld1', 'ld2']}
        #  i1 = {'c': {'c1': 'vc1'}, 'b': 'b0', 'd': {'d1': 'vd1'}}
        # i._union(i1)=
        #  {'a': ['a1', 'a2'], 'c': {'c2': 'vc2', 'c1': 'vc1'}, 'b': ['b1', 'b2', 'b0'], 'd': ['ld1', 'ld2', {'d1': 'vd1'}]}
        # inputs:
        #    d        - dict to be merged with self
        #    replace  - if True where keys in d match keys in self, value of key in self replaced by value in d
        self._showDebug(clas='mtcollection',method='_deepUnion',note='inputs',line=1092,level=0,vars=[['self',self]])
        self._showDebug(clas='mtcollection',method='_deepUnion',note='inputs',line=1093,level=0,vars=[['d',d]])
        if not self and self._sameClassAs(d):
            self._showDebug(clas='mtcollection',method='_deepUnion',note='returns',line=1095,level=0,vars=[['d',d]])
            return d
        else:
            try:
                for k in d:
                    self._showDebug(clas='mtcollection',method='_deepUnion',note='step1',line=1100,level=2,vars=[['k',k]])
                    if k not in self: self[k] = copy.deepcopy(d[k])
                    elif self[k] != d[k]:
                        self._showDebug(clas='mtcollection',method='_deepUnion',note='step2',line=1103,level=2,vars=[['self[k]',self[k]],['d[k]',d[k]]])
                        if replace: self[k] = copy.deepcopy(d[k])
                        elif (self._sameClassAs(self[k]) and
                            isinstance(d[k],dict)):
                            self[k] = self[k]._deepUnion(d[k])
                            self._showDebug(clas='mtcollection',method='_deepUnion',note='step2',line=1108,level=2,vars=[['self[k]',self[k]]])
                        else:
                            if not isinstance(d[k],list): d[k] = [d[k]]
                            if not isinstance(self[k],list): self[k] = [self[k]]
                            for k1 in d[k]:
                                if k1 not in self[k]: self[k] += [k1]
                                self._showDebug(clas='mtcollection',method='_deepUnion',note='step3',line=1114,level=2,vars=[['self[k]',self[k]]])
                self._showDebug(clas='mtcollection',method='_deepUnion',note='returns',line=1115,level=0,vars=[['self',self]])
                return self
            except KeyError: pass
    def _matchUnion(self,d,polarity=1):
        # usage:
        #    primarily for binding variables
        #    union which only succeeds if contents of matching keys also match by value interestion and according to polarity
        # inputs:
        #    d        - dict to be unified with self. Typically a fresh set of variable bindings
        #    polarity - logical polarity of d. (EQ or NOTEQ)
        # returns:
        #    self augmented by merging d as follows:
        #        All keys in d new to self get added with their values
        #        keys in d which already exist in self fail the merge by emptying self if:
        #            polarity > 0 (EQ)    and values for any key doesn't match OR
        #            polarity < 0 (NOTEQ) and values for any key match (ie. an existing value is one which result must NOTEQ)
        # note:
        #    dict d with polarity NOTEQ should only be submitted after all dicts with EQ polarity (in any given Equation)
        self._showDebug(clas='mtcollection',method='_matchUnion',note='inputs',line=1133,level=0,vars=[['self',self],['d',d],['polarity',polarity]])
        for k in d:
            self._showDebug(clas='mtcollection',method='_matchUnion',line=1135,level=2,vars=[['k',k],['self',self]])
            if k:
                if k not in self: self[k] = d[k]                                        # if a new variable: add its binding
                elif (                                                                  # elif an existing variable compare bindings:
                      (polarity > 0 and self[k] != d[k])                                #  if combination should match     but doesn't
                   or (polarity < 0 and self[k] == d[k])                                #  if combination should NOT match but does
                      ): self = self._create(); break                                #  discard bindings
        self._showDebug(clas='mtcollection',method='_matchUnion',note='returns',line=1142,level=0,vars=[['self',self]])
        return self
    def _reduceTo(self,template={},mode=''):
        # returns variant of self containing just the key:value pairs for keys in template
        # mode=all ensures all or nothing matching:
        #    ie any bindings from the template which aren't instantiated in self cause an empty reduction
        self._showDebug(clas='mtcollection',method='_reduceTo',note='inputs',line=1148,level=0,vars=[['self',self],['template',template],['mode',mode]])
        r = self._create()
        all = 1
        for k in template:
            self._showDebug(clas='mtcollection',method='_reduceTo',line=1152,level=2,vars=[['k',k],['self',self]])
            if k in self: r[k] = self[k]
            else: all = 0
        self._showDebug(clas='mtcollection',method='_reduceTo',note='after',line=1155,level=1,vars=[['r',r]])
        if mode == 'all' and not all: r = {}
        self._showDebug(clas='mtcollection',method='_reduceTo',note='returns',line=1157,level=0,vars=[['r',r]])
        return r
    def _yieldArray(self,s,e,*keys):
        # uasage: inputs as self a multilevel collection of arbitrary depth
        # from which it yields lists of keys between depths s(tart) and e(nd) matching supplied list of keys
        self._showDebug(clas='mtcollection',method='_yieldArray',note='inputs',line=1162,level=0,vars=[['self',self],['s',s],['e',e],['keys',keys]])
        o = slist()
        if e > 0:
            if keys: this = keys[0]
            else: this = self
            self._showDebug(clas='mtcollection',method='_yieldArray',line=1167,level=1,vars=[['this',this]])
            for k in this:
                self._showDebug(clas='mtcollection',method='_yieldArray',line=1169,level=2,vars=[['k',k]])
                if e > 1:
                    for o in self[k]._yieldArray(s-1,e-1,*keys[1:]):
                        if s < 1: o[0:0] = [k]
                        self._showDebug(clas='mtcollection',method='_yieldArray',line=1173,level=2,vars=[['o',o]])
                        yield o
                else:
                    self._showDebug(clas='mtcollection',method='_yieldArray',note='yields',line=1176,level=0,vars=[['[k]',[k]]])
                    yield [k]
    def _isUnique(self, members):
        # usage:
        #    tests if self is in members
        #    where members is dict indexed by tuples of sorted key, value tuples obtained from previous calls to this
        # inputs:
        #    members - a collection constructed from previous invocations of this method
        # returns:
        #    updated members, and found (set to True or False) sorted
        self._showDebug(clas='mtcollection',method='_isUnique',note='inputs',line=1186,level=0,vars=[['self',self],['members',members]])
        unique = True
        vars = [(var,self[var]) for var in self]
        if vars:
            vars.sort()
            vars = tuple(vars)
            if vars not in members:
                members[vars] = ''
            else: unique = False
        self._showDebug(clas='mtcollection',method='_isUnique',note='returns',line=1195,level=0,vars=[['members',members],['unique',unique]])
        return members,unique
    def _doSubs(self,s1):
        # usage:
        #    finds all embedded variables within input string s1
        #    and substitutes their values from self into string s2
        # inputs:
        #    s1  - string with optional embedded variables
        # returns:
        #    s2 - value with any defined embedded variables substituted for their values
        # note:
        #    embedded vars like %var1%, %myvar% where
        #    var and myvar are keys in self. Eg:
        #    s1   = 'Header: %title% %start% %end%' produces
        #    s2   = 'Header: start-time %end%' where
        #    self = {'title':None, 'start':'start-time'}
        s2 = s1                                                                         # perform substitution on s2
        for (sub,key) in resub.findall(s1):                                             # for each sub and key pair in s1:
            if key in self:                                                             #  if key in self:
                val = self[key]                                                         #   get its val
                if val is None: val = ''                                                #   if val is None: set to null
                s2 = s2.replace(sub,val)                                                #   replace all sub with val
        s2 = re.sub(' +',' ',s2)                                                        # reduce duplicate spaces
        return s2                                                                       # return s2

class sdict(dict,mtcollection):
    def __init__(self):
        dict.__init__(self)
    def _showDebug(self,
                   clas='',
                   method='',
                   note='',
                   vars=[],
                   line='',
                   level=2):
        Debug()._notify(clas=clas,method=method,note=note,line=line,level=level,vars=vars)
    def __getitem__(self,i):
        try:
            return dict.__getitem__(self,i)
        except KeyError:
            v = self[i] = type(self)()
            return v
    def __iadd__(self,i):
        if not self: self = i
        else: self += i
        return self
    def _sameClassAs(self,i): return isinstance(i,sdict)
    def _create(self): return sdict()

class osdict(sdict):
    # usage:
    #    chronologically ordered sdict - key ordered is preserved
    # notes:
    #    similar to islist but:
    #     - maintain key value pairs
    #     - ensures keys are unique
    #     - cannot detect repeated key sequences
    def __init__(self):
        sdict.__init__(self)
        self._order = slist()
        self._psn = sdict()
    def __setitem__(self,i,v):
        if i not in self:
            self._psn[i] = len(self._order)
            self._order += [i]
        dict.__setitem__(self,i,v)
    def __delitem__(self,i):
        if i in self:
            p = self._psn[i]
            for k in self._order[p+1:]: self._psn[k] -= 1
            self._order.remove(i)
            del self._psn[i]
            dict.__delitem__(self,i)
    def __iter__(self):
        # usage:
        #    overrides Python iteration ie: for k,v in dict: ...
        for k in self._order: yield k, self[k]
    def __reversed__(self):
        for k in self._order.reverse(): yield k, self[k]
    def __str__(self): return repr(self)
    def __repr__(self):
        s = ''
        for k in self._order:
            v = self[k]
            if isinstance(k,basestring): k = "'"+k+"'"
            else: k = str(k)
            if isinstance(v,basestring): v = "'"+v+"'"
            else: v = str(v)
            s += k+':'+v+',';
        if s: return '{'+s[:-1]+'}'
        else: return '{}'
    def _resetitem(self,i,v):
        if i in self: del self[i]
        self[i] = v
    def _getOffset(self,i):
        if i in self._psn: return self._psn[i]
        else: return None
    def _getNext(self,key=None,pos=None):
        nkey = None
        if (pos is not None
        and type(pos) == type(1)
        and pos >= 0
        and pos < len(self._order)-1
            ): nkey = self._order[pos+1]
        elif key is not None:
            try:
                if (key in self._psn
                and self._psn[key]+1 < len(self._order)
                    ): nkey = self._order[self._psn[key]+1]
            except: pass
        return nkey
    def _getPrev(self,key=None,pos=None):
        nkey = None
        if (pos is not None
        and type(pos) == type(1)
        and pos > 0
        and pos < len(self._order)
            ): nkey = self._order[pos-1]
        elif key is not None:
            try:
                if (key in self._psn
                and self._psn[key] > 0
                    ): nkey = self._order[self._psn[key]-1]
            except: pass
        return nkey
    def _getFirst(self):
        if self._order: return self._order[0]
        else: return None
    def _getLast(self):
        if self._order: return self._order[-1]
        else: return None
    def _repeats(self,i):
        r = False
        if i in self._psn:
            l  = len(self._order)
            p1 = self._psn[i]
            p0 = 2*p1-l
            while (p1+1 < len(self._order)
               and p0+1 >= 0
               and self._order[p0+1] == self._order[p1+1]
                   ):
                p0 += 1
                p1 += 1
            if p1+1 == len(self._order): r = True
        return r
    def _showDebug(self,
                   clas='',
                   method='',
                   note='',
                   vars=[],
                   line='',
                   level=2):
        Debug()._notify(clas=clas,method=method,note=note,line=line,level=level,vars=vars)


from metabulate.stores.tree_rb import rbtree

class srbtree(rbtree,mtcollection):
    def __init__(self):
        rbtree.__init__(self)
    def _showDebug(self,
                   clas='',
                   method='',
                   note='',
                   vars=[],
                   line='',
                   level=2):
        Debug()._notify(clas=clas,method=method,note=note,line=line,level=level,vars=vars)
    def __getitem__(self,i):
        try:
            return rbtree.__getitem__(self,i)
        except KeyError:
            v = self[i] = type(self)()
            return v
    def __iadd__(self,i):
        if not self: self = i
        else: self += i
        return self
    def _sameClassAs(self,i): return isinstance(i,srbtree)
    def _create(self): return srbtree()

class Stack(object):
    def __init__(self
                ,items=[]
                ,type=''
                 ):
        self._default_type = 'fifo'                                                     # file listing source files for debug output re-numbering
        self._update(items=items,type=type)
    def _update(self, items=None, type=None):
        if items is not None: self._setItems(items)
        if type  is not None: self._setType(type)
    def _setItems(self,items):
        if not items: items = []
        elif not isinstance(items,list): items = [items]
        self._items = items
        return self._items
    def _getItems(self): return self._items
    def _setType(self,type):
        if not type: self._type = self._default_type
        elif (isinstance(type,basestring) and
            (type == 'fifo' or
             type == 'lifo')): self._type = type
        return self._type
    def _getType(self): return self._type
    def _push(self,item,unique=False):
        if not (unique and self._isUnique(item)):
            self._items = [item] + self._items
    def _pop(self):
        items = self._getItems()
        if items:
            if type == 'fifo': item, items = items[0],  items[1:]
            else:              item, items = items[-1], items[:-1]
            self._setItems(items)
            return item
    def _isEmpty(self):         return not self._getItems()
    def _isUnique(self,item):   return item in self._getItems()
    def _isType(self,type):     return (self._getType() == type)
    def _getItem(self,o):       return self._getItems()[o]
    def _length(self):          return len(self._getItems())

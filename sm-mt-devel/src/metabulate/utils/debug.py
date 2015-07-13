'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

Created on 21 Dec 2009
debug05 Cloned from debug04.py on 19 Apr 2010
debug06 Cloned from debug05.py on 06 May 2010
debug07 Cloned from debug06.py on 13 May 2010
debug08 Cloned from debug07.py on 12 Jun 2010
debug Cloned from debug08.py on 07 Jul 2010
Last Updated on 12 Jul 2010

########################

Objectives:

Debugging complex application is much less about stepping thru program flow and
much more about being able to dice and slice different aspects of program flow.

This utility supports the following USPs:

1. Dice and slice by class, method, variable, and/or notes.
2. Aggregate above into groups of different criteria.
3. Do so in a way which is transparent to the normal functioning of the application.
4. Direct debug outputs to files or the console.
5. Collect multiple debug cross sections for comparison from a single program run.

########################

As debug03.py with:
    version re-engineered with undefined setters = None
    and defaults with null setters
    also mtutils.empty() = None

02/01/10:
    _renumberSources() exploits Flatfile._getValues()

08/02/2010:
    _renumberSources():
      - renamed to _processSources()
      - supports one or more of the following actions 'renumber'|'activate'|'deactivate'
      - implemented via processSource() renamed from renumber()
      - with counts maintained for number lines affected by each action in each source

09/04/2010 standardisation of getter/setter and attribution syntax: (note only - nothing regarded as needed here)
    _get(), _set(), _update() and __init__() methods checked regarding attribution.
    General rule is to reserve getters and setters to externally accessible and decorated attributes.
    These can also be used for just in time attribution (though this isn't currently so outside of the former criteria).
    Attribute setting via _update and __init__ strictly for external accessible attributes.
    Code changed throughout to access all other undecorated attributes directly.
    Python property not currently used to map _get/_set to direct attribute access syntax.

19/04/2010 debug05.py cloned from debug04.py with:
    - Persistent Triple Stores supported

06/05/2010 debug06.py cloned from debug05.py with:
    - URI support exploited via updated imports

13/05/2010 debug07.py cloned from debug06.py with:
    - explicit alias_ontology support (via imports)

12/06/2010 debug08.py cloned from debug07.py with:
    - folders re-configured

07/07/2010 debug.py cloned from debug08.py for SVN versioning

11/07/2010 default debuglist location updated for config variables

12/07/2010 debugger.py spawned from this:
    - Debug sources activation and de-activation moved to debugger
    - enables config variable interpretation in debugger settings without circular conflists between this, utils and singleton

@author: Administrator
'''
from utils import Flatfile
import fileinput
import re
import os.path
import time

class _Debug(object):
    def __init__(self
                ,criteria=[]                                         # criteria objects for publishing debug notifications
                 ):
        self._update(criteria=criteria)
    def _update(self, criteria=None, sources=None):
        if criteria is not None: self._setCriteria(criteria)
    def _setCriteria(self,criteria):
        c = []
        for criterion in criteria:
            if isinstance(criterion,Criteria): c += [criterion]
        self._criteria = c
        return self._criteria
    def _getCriteria(self): return self._criteria
    def _notify(self,
                clas='',
                method='',
                note='',
                line='',
                vars=[],
                level=2):
        criteria = self._getCriteria()
        if criteria:
            for criterion in criteria:
                criterion._notify(clas=clas,method=method,note=note,line=line,vars=vars,level=level)

_debug = _Debug()
def Debug(): return _debug

class Criteria:
    def __init__(self
                ,classes=[]
                ,methods=[]
                ,notes=[]
                ,vars=[]
                ,lines=[]
                ,level=''                         # reporting level; 0 - unspecified, 1 - least, 2 - some, 3 - most
                ,targets=''
                ):
        # implementation defaults
        self._luw             = str(time.time())  # luw id as a millisecond timestamp (used for Flatfile._setValue())
        self._num             = 0                 # debug output number
        # supplied variable defaults
        self._default_level   = 3
        self._default_targets = ['display']
        self._update(classes=classes,methods=methods,notes=notes,vars=vars,lines=lines,level=level,targets=targets)
    def _update(self
               ,classes=None
               ,methods=None
               ,notes=None
               ,vars=None
               ,lines=None
               ,level=None
               ,targets=None
                ):
        # usage:
        #    polymorphic object resetter
        if classes is not None: self._setClasses(classes)
        if methods is not None: self._setMethods(methods)
        if notes   is not None: self._setNotes(notes)
        if vars    is not None: self._setVars(vars)
        if lines   is not None: self._setLines(lines)
        if level   is not None: self._setLevel(level)
        if targets is not None: self._setTargets(targets)
    def _checkList(self,ls):
        if not ls: ls = []
        elif not isinstance(ls,list): ls = [ls]
        l1 = []
        for l in ls:
            if isinstance(l,basestring): l1 += [l]
        return l1
    def _setClasses(self,classes):
        self._classes = self._checkList(classes)
        return self._classes
    def _getClasses(self): return self._classes
    def _passClasses(self,v):
        ok = True
        if v:
            m = self._getClasses()
            if m and v not in m: ok = False
        return ok
    def _setMethods(self,methods):
        self._methods = self._checkList(methods)
        return self._methods
    def _getMethods(self): return self._methods
    def _passMethods(self,v):
        ok = True
        if v:
            m = self._getMethods()
            if m and v not in m: ok = False
        return ok
    def _setNotes(self,notes):
        self._notes = self._checkList(notes)
        return self._notes
    def _getNotes(self): return self._notes
    def _passNotes(self,v):
        ok = False
        if self._getNotes():
            if v:
                for v1 in self._getNotes():
                    if v1 in v:
                        ok = True
                        break
        else: ok = True
        return ok
    def _setVars(self,vars):
        self._vars = self._checkList(vars)
        return self._vars
    def _getVars(self): return self._vars
    def _passVars(self,v):
        ok = []
        if v and self._getVars():
            for [v1,c] in v:
                if v1 in self._getVars():
                    ok += [[v1,c]]
        else:
            if v: ok = v
            else: ok = True
        return ok
    def _setLines(self,lines):
        l = []
        if isinstance(lines,list):
            for ls in lines:
                if (isinstance(ls,list) and
                    len(ls) == 2 and
                    isinstance(ls[0],int) and
                    isinstance(ls[1],int)):
                    l += [ls]
        self._lines = l
        return self._lines
    def _getLines(self): return self._lines
    def _passLines(self,v):
        ok = False
        if v and self._getLines():
            for [v1,v2] in self._getLines():
                if v1 <= v and v <= v2:
                    ok = True
                    break
        else: ok = True
        return ok
    def _setLevel(self,level):
        if level == '': self._level = self._default_level
        elif isinstance(level,int): self._level = level
        return self._level
    def _getLevel(self): return self._level
    def _passLevel(self,v):
        if (not v or
            not self._getLevel() or
            v <= self._getLevel()): ok = True
        else: ok = False
        return ok
    def _setTargets(self,files):
        if not files: l = self._default_targets
        else:
            if not isinstance(files,list): files = [files]
            l = []
            for file in files:
                if ((isinstance(file,basestring) and file=='display') or
                    isinstance(file,Flatfile)): l += [file]
        self._targets = l
        return self._targets
    def _getTargets(self): return self._targets
    def _getLuw(self): return self._luw
    def _setNum(self,num):
        if isinstance(num,int): self._num = num; return num
        else: return 0
    def _incNum(self): self._num += 1; return self._num
    def _getNum(self): return self._num
    def _getSnum(self,w):
        return '%s' % (str(self._num).rjust(w))
    def _notify(self,
                clas='',
                method='',
                note='',
                line='',
                vars=[],
                level=2):
        clas = clas.strip()
        method = method.strip()
        note = note.strip()
        vars = self._passVars(vars)
        if (self._passClasses(clas) and
            self._passMethods(method) and
            self._passNotes(note) and
            self._passLines(line) and
            vars and
            self._passLevel(level) and
            self._getTargets()):
            self._incNum(); s = self._getSnum(4)+' '
            s1 = ''
            if clas: s += clas
            if method:
                if s: s += '.'
                s += method
            if line:
                if s: s += ' '
                s += str(line)
            if s: s += ': '
            if note: s += note+' '
            if vars and isinstance(vars,list):
                for [v,c] in vars:
                    s1 += ', '+v+' = '+str(c)
            if s1: s += s1[2:]
            for t in self._getTargets():
                if t == 'display': print (s)
                elif isinstance(t,Flatfile): t._setValue(s+'\n',luw=self._getLuw())

'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

Created on 21 Dec 2009
protocol04.py Cloned from protocol03.py on 19 Apr 2010
protocol05.py Cloned from protocol04.py on 06 May 2010
protocol06.py Cloned from protocol05.py on 13 May 2010
protocol07.py Cloned from protocol06.py on 12 Jun 2010
protocol.py Cloned from protocol07.py on 07 Jul 2010
Last Updated on 07 Jul 2010

As protocol02.py with the following checked:
    version re-engineered with undefined setters = None
    and defaults with null setters
    also mtutils.empty() = None

    Only update was to remove self._debug instance variable - not needed

24/03/2010:
    _translate re-engineered: changes needed to support output of rules as dicts
      - improved recursion.
      - bug fixes on application of start/end chars
      - dicts and sets supported
      - method documentation updated

25/03/2010:
    - Attributes added:
       _nestLevel to allow switching protocol at a specified depth in the source structure
       _ignoreLevel to allow start/endIgnore chars to be applied to upper levels of structure
       _dictSeperator to translate char seperating keys from values
    - PyProtocol and NestpyProtocol classes added bypassing translation for all or nested structures
    - _factory() method to return constructed protocol objects from a string denoting their type

06/04/2010:
    _factory() moved to new class Protocols. So method may be handed with its object
      as a transformation function to mtutils._genericSetter()

10/04/2010:
    - Protocols._getAvailable() defined to return list of available protocols for input to the _factory() method

19/04/2010 protocol04.py cloned from protocol03.py with:
    - Persistent Triple Stores supported

06/05/2010 protocol05.py cloned from protocol04.py with:
    - URI support exploited via updated imports

13/05/2010 protocol06.py cloned from protocol05.py with:
    - explicit alias_ontology support (via imports)

12/06/2010 protocol07.py cloned from protocol06.py with:
    - folders re-configured

07/07/2010 protocol.py cloned from protocol07.py for SVN versioning

@author: Administrator
'''

import metabulate.utils.utils           as mtutils
import metabulate.utils.debug           as mtdebug

class Protocols:
    def _factory(self,protocol):
        if not isinstance(protocol,Protocol):
            try: protocol = eval(protocol.title()+'Protocol()')
            except: protocol = None
        return protocol
    def _getAvailable(self):
        # usage:
        #    returns list of available protocols for above _factory() method by testing subclasses of Protocol
        a = []
        for p in mtutils._getSubclasses(Protocol):
            p1 = p.replace('Protocol','').lower()
            if p1 not in a: a += [p1]
        return a

class Protocol(object):
    def __init__(self):
        self._nestLevel = 2
        self._ignoreLevel = 0
        self._nest = self
        self._separator = ' '
        self._dictSeparator = ':'
        self._startElement = ''
        self._endElement = ''
        self._endRow = ''
        self._endline = '\n'
        self._startIgnore = ''
        self._endIgnore = ''
        self._startList = '['
        self._endList = ']'
        self._startTuple = '('
        self._endTuple = ')'
        self._startSet = '('
        self._endSet = ')'
        self._startDict = '{'
        self._endDict = '}'
        self._empty = ''
    def _showDebug(self,
                   clas='',
                   method='',
                   note='',
                   vars=[],
                   line='',
                   level=2):
        mtdebug.Debug()._notify(clas=clas,method=method,note=note,line=line,level=level,vars=vars)
    def _translate(self,v,endline=True,level=0):
        # usage:
        #    variably expresses standard Pythonic structures as strings
        # inputs:
        #    v       - value of initial structure
        #    endline - include endline chars [True|False]
        #    level   - recursion depth (implementation parameter)
        # outputs:
        #    s       - v translated to a string
        self._showDebug(clas='Protocol',method='_translate',note='inputs',line=113,level=0,vars=[['v',v],['endline',endline],['level',level]])
        s = ''
        if v:
            endline=mtutils._logical(endline)
            if (isinstance(v,list)
             or isinstance(v,tuple)
             or isinstance(v,set)
             or isinstance(v,dict)
                ):
                if level <= self._ignoreLevel: start = self._startIgnore; end = self._endIgnore
                elif isinstance(v,list):  start = self._startList;  end = self._endList
                elif isinstance(v,dict):  start = self._startDict;  end = self._endDict
                elif isinstance(v,tuple): start = self._startTuple; end = self._endTuple
                elif isinstance(v,set):   start = self._startSet;   end = self._endSet
                if level <= self._nestLevel: next = self
                else: next = self._nest
                for c,i in enumerate(v):
                    if isinstance(v,dict):
                        s1 = next._translate(i,endline=False,level=level+1)
                        s2 = next._translate(v[i],endline=False,level=level+1)
                        s += s1+self._dictSeparator+s2
                    else: s += next._translate(i,endline=False,level=level+1)
                    if c+1 < len(v): s += self._separator
                if s: s = start+s+end
            elif isinstance(v,basestring): s += self._startElement+v+self._endElement
            elif not isinstance(v,mtutils.Empty): s += self._startElement+str(v)+self._endElement
            else: s += self._empty
            if not level: s += self._endRow
            if endline is True: s += self._endline
        self._showDebug(clas='Protocol',method='_translate',note='returns',line=141,level=0,vars=[['s',s]])
        return s
class PyProtocol(Protocol):
    def _translate(self,v,endline=True,level=0):
        s = str(v)
        if endline is True: s += self._endline
        return s
class NestpyProtocol(Protocol):
    def __init__(self):
        Protocol.__init__(self)
        self._ignoreLevel = 0
        self._nestLevel = 1
        self._nest = PyProtocol()
class TextProtocol(Protocol):
    def __init__(self):
        Protocol.__init__(self)
class CsvProtocol(Protocol):
    def __init__(self):
        self._ignoreLevel = 1
        self._nestLevel = 2
        self._nest = PyProtocol()
        self._separator = ', '
        self._dictSeparator = ','
        self._startElement = ""
        self._endElement = ""
        self._endRow = ''
        self._endline = '\n'
        self._startIgnore = ''
        self._endIgnore = ''
        self._startList = '"['
        self._endList = ']"'
        self._startTuple = '"'
        self._endTuple = '"'
        self._startSet = '"('
        self._endSet = ')"'
        self._startDict = ''
        self._endDict = ''
class RelationalProtocol(Protocol):
    def __init__(self):
        self._ignoreLevel = 1
        self._nestLevel = 2
        self._nest = PyProtocol()
        self._separator = ', '
        self._dictSeparator = ':'
        self._startElement = '"'
        self._endElement = '"'
        self._endRow = ''
        self._endline = '\n'
        self._startIgnore = ''
        self._endIgnore = ''
        self._startList = "'"
        self._endList = "'"
        self._startTuple = "'"
        self._endTuple = "'"
        self._startSet = "'"
        self._endSet = "'"
        self._startDict = "'"
        self._endDict = "'"
        self._empty = 'NULL'
class NtripleProtocol(Protocol):
    def __init__(self):
        self._ignoreLevel = 1
        self._nestLevel = 2
        self._nest = PyProtocol()
        self._separator = ' '
        self._dictSeparator = ':'
        self._startElement = '<'
        self._endElement = '>'
        self._endRow = '.'
        self._endline = '\n'
        self._startIgnore = ''
        self._endIgnore = ''
        self._startList = "'"
        self._endList = "'"
        self._startTuple = "<"
        self._endTuple = ">"
        self._startSet = "'"
        self._endSet = "'"
        self._startDict = "'"
        self._endDict = "'"
        self._empty = 'NULL'

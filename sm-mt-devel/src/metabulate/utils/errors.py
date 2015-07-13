'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

Created on 15 Jan 2010
errors02.py Cloned from errors01.py on 19 Apr 2010
errors03.py Cloned from errors02.py on 05 May 2010
errors04.py Cloned from errors03.py on 13 May 2010
errors05.py Cloned from errors04.py on 12 Jun 2010
errors.py Cloned from errors05.py on 07 Jul 2010
Last Updated 10 Sep 2010

Exceptions Handler
- Error messages defined in file specified by errorlogfile mtconfig settings
- This file also provides message variable slots
- Trapped errors may be output to one or more speficied targets and/or trigger an abort
  according to minimum message levels for either also defined in mtconfig. This supported by:
   - Singleton MTerrorlog which holds current configuration settings, and
   - Superclass MTerror:
      - __repr__() method to represent the current error string, obtaining its template from errors.dat
      - _notify() method which outputs the current error string to the chosen targets subject to report and abort criteria

19/02/2010: QueryElementInterpolationError added
21/02/2010: RuleQueryElementCardinalityError added

07/04/2010:
    - SuppliedAttributeValueError, DefaultAttributeMissingError and AttributeTransformationFailure added
    - MTerror.__repr__() updated so substituted values in error message are always strings
    - mtsingleton import switched to singleton04

08/04/2010:
    - AttributionError superclass defined

09/04/2010 standardisation of getter/setter and attribution syntax:
    (mtutils._genericGetter/_genericSetter not required and furthermore problematic potentialy raising recursive errors)
        _get(), _set(), _update() and __init__() methods checked regarding attribution.
        General rule is to reserve getters and setters to externally accessible and decorated attributes.
        These can also be used for just in time attribution (though this isn't currently so outside of the former criteria).
        Attribute setting via _update and __init__ strictly for external accessible attributes.
        Code changed throughout to access all other undecorated attributes directly.
        Python property not currently used to map _get/_set to direct attribute access syntax.

19/04/2010 errors02.py cloned from errors01.py with:
    - Persistent Triple Stores supported

05/05/2010 errors03.py cloned from errors02.py with:
    - URI support exploited via updated imports
    - URI errors added

13/05/2010 errors04.py cloned from errors03.py with:
    - explicit alias_ontology support (via imports)

12/06/2010 errors05.py cloned from errors04.py with:
    - folders re-configured

07/07/2010 errors.py cloned from errors05.py for SVN versioning

12/07/2010 settings support interpetation of config variables

27/08/2010 invalid setting arror added

10/09/2010 potential query ambiguity error added

@author: Administrator
'''

import time
from utils import Flatfile, _logical
import metabulate.singletons.singleton  as mtsingleton

mtconfig  = mtsingleton.Settings()._getItem('config')
mtexcepts = mtsingleton.Settings()._getItem('errors')
levels = {'W':1, 'E':2, 'S':3}

class _MTerrorlog:
    def __init__(self
                ,minreportlevel=''
                ,minabortlevel=''
                ,targets=''
                 ):
        self._default_errorlogfile = Flatfile(path=mtconfig._interpretItem('errorlogfile_path','%configfilesbase%Errors\\')
                                             ,name=mtconfig._interpretItem('errorlogfile_name')
                                             ,type=mtconfig._interpretItem('errorlogfile_type')
                                              )
        self._default_minreportlevel  = mtconfig._interpretItem('errors_minreportlevel',1)
        self._default_minabortlevel   = mtconfig._interpretItem('errors_minabortlevel',3)
        self._default_targets         = [self._default_errorlogfile]
        self._default_errorstoconsole = _logical(mtconfig._interpretItem('errorstoconsole'))
        if self._default_errorstoconsole: self._default_targets += ['display']
        self._update(minreportlevel=minreportlevel,minabortlevel=minabortlevel,targets=targets)
    def _update(self
               ,minreportlevel=None
               ,minabortlevel=None
               ,targets=None
                ):
        if minreportlevel is not None: self._setMinreportlevel(minreportlevel)
        if minabortlevel  is not None: self._setMinabortlevel(minabortlevel)
        if targets        is not None: self._setTargets(targets)
    def _setMinreportlevel(self,level):
        if level == '': self._minreportlevel = self._default_minreportlevel
        elif isinstance(level,int): self._minreportlevel = level
        return self._minreportlevel
    def _getMinreportlevel(self): return self._minreportlevel
    def _setMinabortlevel(self,level):
        if level == '': self._minabortlevel = self._default_minabortlevel
        elif isinstance(level,int): self._minabortlevel = level
        return self._minabortlevel
    def _getMinabortlevel(self): return self._minabortlevel
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

_mterrorlog = _MTerrorlog()
def MTerrorlog(): return _mterrorlog

class MTerror(Exception):
    def __init__(self, id, level, args):
        self._id    = id
        self._level = level
        self._args  = args
        self._time  = '('+time.ctime()+')'
    def __repr__(self):
        # usage:
        #    generates error string from string template and variables
        # returns:
        #    out - generated error string
        out = ''
        try:                                                            # try getting the error string template
            out = mtexcepts._getItem(self._id)                          #  from the index of the error messages data file
        except IndexError: pass                                         # ignoring failed indexes
        if out:                                                         # if a template: (substitute its variable slots)
            for c,new in enumerate(self._args):                         #  for each variable
                old = '$'+str(c)                                        #   get the var slot name
                if not isinstance(new,basestring): new = str(new)
                out = out.replace(old,new)                              #   replace slot name with its value in the error msg
        return out                                                      # return the error string
    def _notify(self,c=None,m=None):
        # usage:
        #    compile error msg, notify targets and/or abort according to settings
        # inputs:
        #    c - source class name
        #    m - source method name
        el = MTerrorlog()                                               # get the MTerrorlog singleton
        ls = self._level                                                # get this msg level
        try: li = levels[self._level]                                   # try interpreting level as an integer
        except: li = 4                                                  # if not assume max severity
        if li >= int(el._minreportlevel):                               # if this error to be reported:
            s = self.__repr__()                                         #  get the error string
            if s:                                                       #  if an error string: complete and output it
                if m is not None: s1 = '.'+m                            #   add source method (if any)
                if c is not None: s1 = c+s1                             #   add source class  (if any)
                else: s1 = s1[1:]                                       #   combine class & method with a '.'
                if s1: s1 = ls+' '+s1                                   #   add message level
                else: s1 = ls
                if s1: s1 = self._time+' '+s1                           #   add timestamp
                else: s1 = self._time
                s = s1+': '+s                                           #   finalise error message
                for t in el._getTargets():                              #   for each target to notify:
                    if t == 'display': print (s)                        #    if target is 'display' print msg
                    elif isinstance(t,Flatfile): t._setValue(s+'\n')    #    elif a Flatfile output as a log
        if li >= int(el._minabortlevel): raise type(self)               # perform abort? (note abort may follow notify)

class QueryableError(MTerror): pass
class EquationListTypesError(QueryableError):
    def __init__(self,*args):
        MTerror.__init__(self,'EquationListTypesError','W',args)
class EquationListFormatError(QueryableError):
    def __init__(self,*args):
        MTerror.__init__(self,'EquationListFormatError','W',args)
class EquationFormatError(QueryableError):
    def __init__(self,*args):
        MTerror.__init__(self,'EquationFormatError','W',args)
class EquationLogicError(QueryableError):
    def __init__(self,*args):
        MTerror.__init__(self,'EquationLogicError','W',args)
class QueryListFormatError(QueryableError):
    def __init__(self,*args):
        MTerror.__init__(self,'QueryListFormatError','W',args)
class QueryFormatError(QueryableError):
    def __init__(self,*args):
        MTerror.__init__(self,'QueryFormatError','W',args)
class QueryTripleError(QueryableError):
    def __init__(self,*args):
        MTerror.__init__(self,'QueryTripleError','W',args)
class QueryElementInterpolationError(QueryableError):
    def __init__(self,*args):
        MTerror.__init__(self,'QueryElementInterpolationError','W',args)
class QueryExpressionError(QueryableError):
    def __init__(self,*args):
        MTerror.__init__(self,'QueryExpressionError','W',args)
class RuleQueryElementCardinalityError(QueryableError):
    def __init__(self,*args):
        MTerror.__init__(self,'RuleQueryElementCardinalityError','W',args)
class QueryPotentialAmbiguityError(QueryableError):
    def __init__(self,*args):
        MTerror.__init__(self,'QueryPotentialAmbiguityError','W',args)

class SolutionError(MTerror): pass
class SolutionQueryStoreError(SolutionError):
    def __init__(self,*args):
        MTerror.__init__(self,'SolutionQueryStoreError','W',args)

class PatternError(MTerror): pass
class PatternTripleSizeError(PatternError):
    def __init__(self,*args):
        MTerror.__init__(self,'PatternTripleSizeError','W',args)
class PatternEmptyError(PatternError):
    def __init__(self,*args):
        MTerror.__init__(self,'PatternEmptyError','W',args)
class PatternDictionaryError(PatternError):
    def __init__(self,*args):
        MTerror.__init__(self,'PatternDictionaryError','W',args)

class ParseError(MTerror): pass
class ParseIncompleteError(ParseError):
    def __init__(self,*args):
        MTerror.__init__(self,'ParseIncompleteError','W',args)
class ParseInvalidRegexError(ParseError):
    def __init__(self,*args):
        MTerror.__init__(self,'ParseInvalidRegexError','W',args)
class ParseRulesLoadingError(ParseError):
    def __init__(self,*args):
        MTerror.__init__(self,'ParseRulesLoadingError','W',args)

class ExpressionError(MTerror): pass
class UnbalancedParenthesisError(ExpressionError):
    def __init__(self,*args):
        MTerror.__init__(self,'UnbalancedParenthesisError','W',args)
class UnspecifiedParenthesisError(ExpressionError):
    def __init__(self,*args):
        MTerror.__init__(self,'UnspecifiedParenthesisError','E',args)

class AttributionError(MTerror): pass
class SuppliedAttributeValueError(AttributionError):
    def __init__(self,*args):
        MTerror.__init__(self,'SuppliedAttributeValueError','W',args)
class AttributeMissingError(AttributionError):
    def __init__(self,*args):
        MTerror.__init__(self,'AttributeMissingError','W',args)
class DefaultAttributeMissingError(AttributionError):
    def __init__(self,*args):
        MTerror.__init__(self,'DefaultAttributeMissingError','W',args)
class AttributeTransformationFailure(AttributionError):
    def __init__(self,*args):
        MTerror.__init__(self,'AttributeTransformationFailure','W',args)
class InvalidSettingError(AttributionError):
    def __init__(self,*args):
        MTerror.__init__(self,'InvalidSettingError','W',args)

class StoreError(MTerror): pass
class AddTripleError(StoreError):
    def __init__(self,*args):
        MTerror.__init__(self,'AddTripleError','W',args)

class URIerror(MTerror): pass
class URIparseError(URIerror):
    def __init__(self,*args):
        MTerror.__init__(self,'URIparseError','W',args)
class URIauthorityError(URIerror):
    def __init__(self,*args):
        MTerror.__init__(self,'URIauthorityError','W',args)
class URInamespaceError(URIerror):
    def __init__(self,*args):
        MTerror.__init__(self,'URInamespaceError','W',args)
class URIaddNamespaceError(URIerror):
    def __init__(self,*args):
        MTerror.__init__(self,'URIaddNamespaceError','W',args)
class URIdeleteNamespaceError(URIerror):
    def __init__(self,*args):
        MTerror.__init__(self,'URIdeleteNamespaceError','W',args)
class URIsupportOff(URIerror):
    def __init__(self,*args):
        MTerror.__init__(self,'URIsupportOff','W',args)

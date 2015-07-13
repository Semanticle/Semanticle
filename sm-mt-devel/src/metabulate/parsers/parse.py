'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

Created on 21 Dec 2009
parse17.py Cloned from parse16.py on 02 Mar 2010
parse18.py Cloned from parse17.py on 18 Mar 2010
parse19.py Cloned from parse18.py on 19 Apr 2010
parse20.py Cloned from parse19.py on 06 May 2010
parse21.py Cloned from parse20.py on 13 May 2010
parse22.py Cloned from parse21.py on 12 Jun 2010
parse.py Cloned from parse22.py on 07 Jul 2010
Last Updated on 06 Oct 2010

As parse15.py with:
    version re-engineered with undefined setters = None
    and defaults with null setters
    also mtutils.empty() = None

02/01/2010:
    _import() exploits new Flatfile._getValues()

04/01/2010:
    uses singleton settings['config'] - requiring import of mtsingleton

02/03/2010 parse17.py cloned from parse16.py with:
    - singleton03 exploited

10/03/2010:
    - better handling of nested triples - allows mixed triples and vals
       - userexits02.py handles partial matches compatibly with other BNF clauses
       - eexp_test04.bnf updated BNF

16/03/2010:
    - exploited re-engineered user exit to get nested triples

18/03/2010 parse18.py cloned from parse17.py with:
    - exploits non-infered QueryExpression comperands

07/04/2010 exploits mtutils._genericSetter()/_genericGetter() for just in time attribute instantiation

08/04/2010: hardcoded config and prefs also defined

09/04/2010 standardisation of getter/setter and attribution syntax:
    _get(), _set(), _update() and __init__() methods checked regarding attribution.
    General rule is to reserve getters and setters to externally accessible and decorated attributes.
    These can also be used for just in time attribution (though this isn't currently so outside of the former criteria).
    Attribute setting via _update and __init__ strictly for external accessible attributes.
    Code changed throughout to access all other undecorated attributes directly.
    Python property not currently used to map _get/_set to direct attribute access syntax.

19/04/2010 parse19.py cloned from parse18.py with:
    - Persistent Triple Stores supported

06/05/2010 parse20.py cloned from parse19.py with:
    - URI support exploited via updated imports

07/05/2010: bnf definitions updated to support URI <val> expressions

13/05/2010 parse21.py cloned from parse20.py with:
    - explicit alias_ontology support (via imports)

12/06/2010 parse22.py cloned from parse21.py with:
    - folders re-configured

07/07/2010 parse.py cloned from parse22.py for SVN versioning

12/07/2010 settings support interpetation of config variables

06/10/2010 automatically loads and "compiles" rules file if bnf source is updated

@author: Administrator
'''

import re
import metabulate.utils.utils           as mtutils
import metabulate.utils.debug           as mtdebug
import metabulate.utils.errors          as mterrors
import metabulate.singletons.singleton  as mtsingleton
import metabulate.parsers.userexits     as mtpexits
import fileinput
import os.path

safesplit = re.compile('\>\s*\<')                                                   # regex split clauses with(out) spacing
mtconfig = mtsingleton.Settings()._getItem('config')

class Parser:
    _default_select   = ['<exp>']
    _default_filepath = mtconfig._interpretItem('parserfile_path','%configfilesbase%Config\\')
    _default_filename = mtconfig._interpretItem('parserfile_name_query','eexp_test')
    def __init__(self
                ,select=None
                ,filepath=None
                ,filename=None
                ):
        self._rules     = []
        self._rulesUsed = mtutils.slist()
        self._cache     = mtutils.sdict()
        self._i_rules   = mtutils.sdict()
        self._update(select=select,filepath=filepath,filename=filename)
    def _update(self
               ,select=None
               ,filepath=None
               ,filename=None
                ):
        if select   is not None: self._setSelect(select)
        if filepath is not None: self._setFilepath(filepath)
        if filename is not None: self._setFilename(filename)
    def _setSelect(self,*args):
        return mtutils._genericSetter(self,'select',args,t=basestring,plural=True)
    def _getSelect(self,default=True):
        return mtutils._genericGetter(self,'select',default)
    def _setFilepath(self,*args):
        return mtutils._genericSetter(self,'filepath',args,t=basestring)
    def _getFilepath(self,default=True):
        return mtutils._genericGetter(self,'filepath',default)
    def _setFilename(self,*args):
        return mtutils._genericSetter(self,'filename',args,t=basestring)
    def _getFilename(self,default=True):
        return mtutils._genericGetter(self,'filename',default)
    def _showDebug(self
                  ,clas=''
                  ,method=''
                  ,note=''
                  ,vars=[]
                  ,line=''
                  ,level=2
                  ):
        mtdebug.Debug()._notify(clas=clas,method=method,note=note,line=line,level=level,vars=vars)
    def _import(self,filename=None,mode='new'):
        # usage:
        #    loads self._i_rules from filename.pys or if not available
        #    loads BNF clauses from filename.bnf and generates self._i_rules also saving to filename.pys
        self._showDebug(clas='Parser',method='_import',note='inputs',line=133,level=0,vars=[['filename',filename],['mode',mode]])
        stripcomments = re.compile('\#\.\..+?$')                                    # suffix comments start with #..
        self._update(filename=filename)                                             # update filename if supplied
        rf = mtutils.Flatfile(path=self._getFilepath()
                             ,name=self._getFilename()
                             ,type=mtconfig._getItem('parserfile_loadtype')
                              )                                                     # get "compiled" rules file object
        sf = mtutils.Flatfile(path=self._getFilepath()
                             ,name=self._getFilename()
                             ,type=mtconfig._getItem('parserfile_bnftype')
                              )                                                     # get bnf source file object
        rm = rf._getModified()                                                      # get rules file last modified time
        if rm and rm > sf._getModified(): i_rules = rf._load()                      # if rules file exists and still relevant: load it
        else: i_rules = None                                                        # else: prepare to (re-)generate it
        if i_rules: self._i_rules = i_rules
        else:                                                                       # re-generate "compiled" rules file
            first = 1                                                               #  first rule flag
            for value in sf._getValues():                                           #  read lines getting stripped values
                if first:                                                           #  if first rule:
                    first = 0                                                       #   no longer first
                    if mode == 'new': self._rules = []                              #   if mode == 'new' make new rules list
                self._rules += [value]                                              #   append rule to rules list
            if self._rules: rf._unload(self._setI_Rules())                          #   process further and serialise
        self._showDebug(clas='Parser',method='_import',note='returns',line=156,level=0,vars=[['self._i_rules',self._i_rules]])
        return self._i_rules
    def _setI_Rules(self):
        # pre-process rules into strings or copiled regex
        # splitting regex parts and counting match groups
        # in i_rules indexed by lhs
        # with rhs sorted by inverse (clause count, rhs clause string length)
        i_rules = mtutils.sdict()
        for rule in self._rules:
            equation = rule.split('::-')
            if len(equation) == 2:                                                          # only if lhs and rhs
                ok = 1                                                                      # default ok
                uc = 0                                                                      # dummy usage count for later sorting by most used first
                ep = mtutils.slist()
                for c in range(2): equation[c] = equation[c].strip()                        # strip lhs and rhs
                if equation[1].startswith('/') and equation[1].endswith('/'):               # rhs is a regex
                    ep = mtutils._splitRegex(equation[1])
                    try:                                                                    # try processing regex:
                        ec,pc = mtutils._pdepth(ep[0])                                      #  count and validate inner parenthesis
                        if ec == 1: raise mterrors.UnbalancedParenthesisError(ep[0])        #  test error code to raise errors
                        elif ec == 2: raise mterrors.UnspecifiedParenthesisError()
                        self._showDebug(clas='Parser',method='_setI_Rules',line=177,level=1,vars=[['equation[1]',equation[1]],['ep',ep],['ok',ok],['pc',pc]])
                        if not ep[0].startswith('^'): ep[0] = '^'+ep[0]                     #   ensure it matches from beginning
                        try: equation[1] = re.compile(ep[0])                                #   try compiling the pattern
                        except: raise mterrors.ParseInvalidRegexError(ep[0])                #   escalate failure
                    except mterrors.ParseError, X:
                        X._notify(c='Parser',
                                  m='_setI_Rules()')                                        # notify ParseError
                elif equation[1].startswith('{') and equation[1].endswith('}'):             # rhs is a userexit Element method
                    equation[1] = mtpexits.Test(equation[1][1:-1].strip())                  #  instantiate rhs a userexit Test
                else:                                                                       # rhs is a string or clause(s)
                    equation[1] = safesplit.sub('>~#!@!#~<',equation[1])                    #  sub special clause seperator
                self._showDebug(clas='Parser',method='_setI_Rules',line=188,level=1,vars=[['equation[0]',equation[0]],['equation[1]',equation[1]]])
                if ok:                                                                      # add to i_rules if OK
                    if equation[0] not in i_rules:                                          #  if rhs not in
                        i_rules[equation[0]] = [[equation[1],uc,ep]]                        #   add it
                        self._showDebug(clas='Parser',method='_setI_Rules',line=192,level=1,vars=[['equation[0]',equation[0]]])
                    else:                                                                   # insert new lhs into list sorted by size
                        l1 = len(i_rules[equation[0]])                                      # set up manual break and list counter
                        c = -1
                        while c+1 < l1:
                            c += 1
                            self._showDebug(clas='Parser',method='_setI_Rules',line=198,level=2,vars=[['l1',l1],['c',c],['i_rules[equation[0]][c]',i_rules[equation[0]][c]],['equation[1]',equation[1]]])
                            if (i_rules[equation[0]][c][1] < uc):                           # if new rhs has more clauses
                                i_rules[equation[0]][c:c] = [[equation[1],uc,ep]]           #   insert it here into the rhs list
                                c = l1                                                      #   and break
                            elif i_rules[equation[0]][c][0] == equation[1]: c = l1          # elif rhs is not new break
                            elif c+1 == l1:                                                 # elif at end of list
                                i_rules[equation[0]] += [[equation[1],uc,ep]]               # append new rhs to list
                        self._showDebug(clas='Parser',method='_setI_Rules',line=205,level=1,vars=[['i_rules[equation[0]]',i_rules[equation[0]]]])
        self._i_rules = i_rules
        self._showDebug(clas='Parser',method='_setI_Rules',note='returns',line=207,level=0,vars=[['i_rules',i_rules]])
        return i_rules
    def _updateI_Rules(self,filename=None):
        # usage: resorts i_rules according to updated usage counts and serialises
        # inputs: optional filename
        for lhs in self._rulesUsed:
            l = len(self._i_rules[lhs])-1
            c = l
            while c-1 > 0:
                c -= 1
                if self._i_rules[lhs][c][1] < self._i_rules[lhs][c+1][1]:
                    c1 = c
                    while c1 < l and self._i_rules[lhs][c1][1] < self._i_rules[lhs][c1+1][1]:
                        t = self._i_rules[lhs][c1]
                        self._i_rules[lhs][c1] = self._i_rules[lhs][c1+1]
                        self._i_rules[lhs][c1+1] = t
                        c1 += 1
        self._update(filename=filename)
        mtutils.Flatfile(path=self._getFilepath()
                        ,name=self._getFilename()
                        ,type='pyo'
                        )._unload(self._i_rules)                                        #  serialise updates
        return self._i_rules
    def _parse(self,sentence=None,top='<exp>',select=None):
        # generic BNF driven top down parser
        # usage:
        #    inputs:
        #        s        = sentence to be parsed
        #        top      = root clause
        #        select   = list of clauses to be solved
        #    yields: sentence,binding
        #        sentence = sentence expressed as list of parsed components
        #        binding  = index of bound clauses solved
        def parse(s,lhs,level=0):                                               # recursive top down parser
            def parse1(s,l_rhs,level,lhs,c):                                    # recursive parser of rhs clause list
                def parse2(s,rhs,level,lhs,c):                                  # parser of single rhs clause
                    self._showDebug(clas='Parser',method='_parse',note='.parse.parse1.parse2 inputs',line=243,level=0,vars=[['s',s],['rhs',rhs],['level',level],['lhs',lhs],['c',c]])
                    smatch = bmatch = ''                                        #   prepare to get match and sub_binding
                    bound1 = {}
                    s1 = s
                    if isinstance(rhs,basestring):                              #   if string for matching
                        rhs = rhs.strip()                                       #    strip it
                        if rhs.startswith('<') and rhs.endswith('>'):           #    if a nested clause
                            for s1,match,bound1 in parse(s,rhs,level=level+1):  #     for each parsed rhs:
                                bound = bound1                                  #      temp sub_binding store
                                if lhs in bound1:                               #      if rhs clause is recursive
                                    del bound1[lhs]                             #       remove it from temp binding
                                    self._i_rules[lhs][c][1] -= 1               #       remove it from count of BNF clauses used
                                self._showDebug(clas='Parser',method='_parse',note='.parse.parse1.parse2 yields',line=255,level=0,vars=[['s1',s1],['match',match],['bound',bound],['bound1',bound1]])
                                yield s1,match,bound,bound1                     #      yield match data
                        else:                                                   #    if a simple text matching
                            if s1.startswith(rhs):                              #     if match
                                smatch = bmatch = rhs                           #      record solving and binding matches
                    elif isinstance(rhs,mtpexits.Test):
                        tmp = rhs._eval(mtpexits.Element(s))
                        if tmp:
                            smatch = tmp[0]
                            bmatch = tmp[1]
                    elif rhs.match(s):                                          #   else if a regex match
                        ep = self._i_rules[lhs][c][2]                           #    get regex parts
                        smatch,bmatch = mtutils._evalRegex(s,rhs,ep=ep)         #    get solving & binding matches from regex
                    self._showDebug(clas='Parser',method='_parse',note='.parse.parse1.parse2 yields',line=268,level=1,vars=[['smatch',smatch],['bmatch',bmatch]])
                    if bmatch:                                                  #   if match recorded
                        s1 = s[len(smatch):]                                    #    remove solving match from the remaining sentence
                        bound = match = bmatch                                  #    temp bound and match store
                        self._showDebug(clas='Parser',method='_parse',note='.parse.parse1.parse2 yields',line=272,level=0,vars=[['s1',s1],['match',match],['bound',bound],['bound1',bound1]])
                        yield s1,match,bound,bound1                             #    yield match data
                self._showDebug(clas='Parser',method='_parse',note='.parse.parse1 inputs',line=274,level=0,vars=[['s',s],['l_rhs',l_rhs],['level',level],['lhs',lhs],['c',c]])
                for s,match,bound,bound1 in parse2(s,l_rhs[0],level,lhs,c):     #   for each match of first rhs clause
                    if match:                                                   #    if match:
                        self._showDebug(clas='Parser',method='_parse',note='.parse.parse1',line=277,level=2,vars=[['s',s],['lhs',lhs],['match',match],['bound',bound],['bound1',bound1]])
                        i_match = mtutils.sdict()                               #     set default match index
                        i_bound = mtutils.sdict()                               #     set default binding index
                        i_match = i_match._deepUnion({lhs:[match]})             #     record this clause match in i_match
                        self._i_rules[lhs][c][1] += 1                           #     increment BNF clause usage count
                        if lhs not in self._rulesUsed: self._rulesUsed += [lhs] #     flag usage of this clause
                        self._showDebug(clas='Parser',method='_parse',note='.parse.parse1',line=283,level=2,vars=[['lhs',lhs],['bound1',bound1],['self._getSelect()',self._getSelect()]])
                        i_bound = i_bound._deepUnion(bound1)                    #     index sub_binding in i_bound
                        if not self._getSelect() or lhs in self._getSelect():   #     if this binding required
                            i_bound = i_bound._deepUnion({lhs:[bound]})         #      add it to bound index
                        if len(l_rhs) == 1:                                     #     if only 1 rhs clause
                            self._showDebug(clas='Parser',method='_parse',note='.parse.parse1 yields',line=288,level=0,vars=[['s',s],['i_match',i_match],['i_bound',i_bound]])
                            yield s,i_match,i_bound                             #      yield it as a match
                        else:                                                   #     else (more clauses):
                            for s,i_match1,i_bound1 in parse1(s,l_rhs[1:],level,lhs,c): # parse the remaining rhs clauses
                                i_match = i_match._deepUnion(i_match1)          #        index match in i_match
                                i_bound = i_bound._deepUnion(i_bound1)          #        index sub_binding in i_bound
                                self._showDebug(clas='Parser',method='_parse',note='.parse.parse1 yields',line=294,level=0,vars=[['s',s],['i_match',i_match],['i_bound',i_bound]])
                                yield s,i_match,i_bound                         #        and yield match data
            s = s.strip()                                                       # strip leading and trailing whitespace from sentence
            lhs = lhs.strip()                                                   # and from lhs
            self._showDebug(clas='Parser',method='_parse',note='.parse inputs',line=298,level=0,vars=[['s',s],['lhs',lhs],['level',level]])
            self._showDebug(clas='Parser',method='_parse',note='.parse',line=299,level=1,vars=[['self._i_rules[lhs]',self._i_rules[lhs]]])
            if s:                                                               # if anything still to parse
                l = len(self._i_rules[lhs])                                     #  prepare to loop through each rhs variant
                c = -1
                while c+1 < l:                                                  #  for each rhs of this lhs
                    c += 1
                    rhs = self._i_rules[lhs][c][0]
                    if isinstance(rhs,basestring): l_rhs = rhs.split('~#!@!#~') #  and split clauses around this seperator
                    else: l_rhs = [rhs]
                    self._showDebug(clas='Parser',method='_parse',note='.parse',line=308,level=1,vars=[['c',c],['rhs',rhs],['l_rhs',l_rhs]])
                    match = ''
                    s1 = s
                    for s1,i_match,i_bound in parse1(s1,l_rhs,level,lhs,c):     #  for each match of the rhs clauses
                        self._showDebug(clas='Parser',method='_parse',note='.parse yields',line=312,level=0,vars=[['s1',s1],['i_match',i_match],['i_bound',i_bound]])
                        yield s1,i_match,i_bound                                #   yield match data
        # main parse method - prepare to submit to recursive top down parser
        if sentence:
            self._update(select=select)                                         # update select & debug if supplied
            sentence = sentence.strip()
            self._showDebug(clas='Parser',method='_parse',note='inputs',line=318,level=0,vars=[['sentence',sentence],['top',top],['select',select],['self._cache',self._cache]])
            if sentence in self._cache: return self._cache[sentence]
            if not self._i_rules:
                self._import()                                                  # if pre_compiled parse not loaded: load it
                if not self._i_rules:
                    raise mterrors.ParseRulesLoadingError('"'
                                                         +self._getFilepath()
                                                         +self._getFilename()
                                                         +'.'+mtconfig._getItem('parserfile_loadtype')
                                                         +' or '
                                                         +'.'+mtconfig._getItem('parserfile_bnftype')
                                                         +'"'
                                                          )
            s = sentence
            for s,i_match,i_bound in parse(sentence,top):                       # parse sentence
                self._showDebug(clas='Parser',method='_parse',line=333,level=1,vars=[['s',s],['i_match',i_match],['i_bound',i_bound]])
                if not s:                                                       # if everything is parsed
                    self._cache[sentence] = [i_match,i_bound]
                    self._updateI_Rules()                                       #  save updated BNF clause usages
                    self._showDebug(clas='Parser',method='_parse',note='returns',line=337,level=0,vars=[['s',s],['i_match',i_match],['i_bound',i_bound]])
                    return [i_match,i_bound]                                    #  return sentence and bindings
            raise mterrors.ParseIncompleteError(sentence,s)                     # otherwise trap incomplete parse error

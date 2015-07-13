'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

fti.py Created on 11 Aug 2010
Last Updated 27 Aug 2010

24/08/2010:
    - Forwards compatability updates between P2.6/7 and P3
      in handling support of keys(), iteritems(), sort(), map(), itemgetter() and has_key().

27/08/2010 Towards handling of invalid default settings:
    - all defaults used only by _genericSetter() are now obtained in dual format comprising:
        - the supplied default via settings
        - a backup last resort hardcoded default if this is invalid

@author: Administrator
'''
import re
import metabulate.utils.utils           as mtutils
import metabulate.utils.debug           as mtdebug
import metabulate.singletons.singleton  as mtsingleton

mtprefs  = mtsingleton.Settings()._getItem('prefs')
# extract and complie list of fti regex from prefs or hardcoded default
ws = eval(mtprefs._interpretItem('fti_regex',"['[A-Za-z0-9]+','[A-Za-z0-9\-\_]+']"))
if isinstance(ws,basestring): wr = [ws]
elif isinstance(ws,list):
    wr = mtutils.slist()
    wr += ws
    wr = wr._peel(1)
ftire = [re.compile(w) for w in wr]

class fti(object):
    # defaults
    _default_usecase    = mtprefs._interpretItem('fti_usecase','true',2)          # case sensitivity
    _default_splitmatch = mtprefs._interpretItem('fti_splitmatch','true',2)       # discontiguous matching
    _default_splitmodes = mtutils._stripsplit(mtprefs._interpretItem(
                                'fti_splitmodes','complete,consistent'))          # discontiguous matching modes
    _default_splitmodes = (_default_splitmodes,['complete','consistent'])         # include hardcoded in-case settings exist but are wrong
    def __init__(self
                ,usecase=None
                ,splitmatch=None
                ,splitmodes=None
                 ):
        # implementation values
        self._idx = mtutils.sdict()                                             # index
        # API updatable values
        self._update(usecase=usecase
                    ,splitmatch=splitmatch
                    ,splitmodes=splitmodes
                    )
    def _update(self
               ,usecase=None
               ,splitmatch=None
               ,splitmodes=None
                ):
        if usecase    is not None: self._setUsecase(usecase)
        if splitmatch is not None: self._setSplitmatch(splitmatch)
        if splitmodes is not None: self._setSplitmodes(splitmodes)
    def _setUsecase(self,*args):
        return mtutils._genericSetter(self,'usecase',args,m=[True,False],logical=True)
    def _getUsecase(self,default=True):
        return mtutils._genericGetter(self,'usecase',default)
    def _setSplitmatch(self,*args):
        return mtutils._genericSetter(self,'splitmatch',args,m=[True,False],logical=True)
    def _getSplitmatch(self,default=True):
        return mtutils._genericGetter(self,'splitmatch',default)
    def _setSplitmodes(self,*args):
        return mtutils._genericSetter(self,'splitmodes',args,m=['complete','consistent'],plural=True)
    def _getSplitmodes(self,default=True):
        return mtutils._genericGetter(self,'splitmodes',default)
    def _showDebug(self,
                   clas='',
                   method='',
                   note='',
                   vars=[],
                   line='',
                   level=2):
        mtdebug.Debug()._notify(clas=clas,method=method,note=note,line=line,level=level,vars=vars)
    def _genIndexes(self,s,match=False):
        xs = mtutils.slist()                                                    #     initialise new list of indexes for this fragment
        for ftir in ftire:                                                      #     using each word index generator:
            x = ftir.findall(s)
            if match: xs += [x]
            else: xs = xs._union(x)                                             #      collate all indexes for this fragment
        return xs
    def _addItem(self,s,v):
        xs = self._genIndexes(s)                                                #     list unique indexes for this fragment
        self._showDebug(clas='TripleStore',method='_addItem',note='fulltextindex',line=89,level=2,vars=[['xs',xs]])
        for x in xs:                                                            #      for each indexable word in fragment:
            ws = [x,x.lower()]                                                  #      list word formats [actual,case_insensitive]
            for c,i in enumerate(['a','i']):                                    #      instantiate each word type in matching fti type:
                if v not in self._idx[i][ws[c]]:                                #       if this stored uri isn't in this full text index
                    self._idx[i][ws[c]] += [v]                                  #        add it to this full text index
    def _deleteItem(self,s,v):
        xs = self._genIndexes(s)                                                #      list unique indexes for this fragment
        self._showDebug(clas='TripleStore',method='_deleteItem',note='fulltextindex',line=97,level=2,vars=[['xs',xs]])
        for x in xs:                                                            #      for each indexable word in fragment:
            ws = [x,x.lower()]                                                  #      list word formats [actual,case_insensitive]
            for c,i in enumerate(['a','i']):                                    #      for each word type in matching fti type:
                if v in self._idx[i][ws[c]]:                                    #        if this stored uri is in index
                    self._idx[i][ws[c]].remove(v)                               #         remove it
                    if len(self._idx[i][ws[c]]) == 0:                           #         if last stored uri gone for this word
                        del self._idx[i][ws[c]]                                 #          remove this word
    def _matchItem(self,parentFti,val,op):
        if parentFti._getSplitmatch():                                          #      if splitmatch:
            l_xs = self._genIndexes(val,match=True)                             #       list each set of match indexes for this fragment
            m = parentFti._getSplitmodes()                                      #       get split matching modes
        else:                                                                   #      else simple fti matching:
            l_xs = [[val]]                                                      #       so prepare 1 match set from the match value
            m = ['complete','consistent']                                       #       apply default matching modes
        if parentFti._getUsecase(): i = 'a'                                     #      standardise word to parentStore case setting
        else: i = 'i'                                                           #       actual or case insensitive full text index
        r = mtutils.slist()                                                     #      initialise the list of matching uris
        for xs in l_xs:                                                         #      for each set of match indexes:
            r1 = mtutils.slist()                                                #       initialise the list of matching uris for this set
            for x in xs:                                                        #       for each index in this match index set:
                if not parentFti._getUsecase():                                 #        if case insensitive matching:
                    w = x.lower()                                               #         convert index to common lowercase
                if w in self._idx[i]:                                           #        if index is in the full text index:
                    r2 = self._idx[i][w]                                        #         get matching uris for this index
                    if not r1: r1 += r2                                         #         use as is if 1st match for this set of indexes
                    else:                                                       #         else combine uris according to split modes
                        if 'complete' in m:                                     #          if complete matching:
                            r1 = r1._intersection(r2)                           #           ensure uris match all indexes in set
                        else: r1 = r1._union(r2)                                #          else: collate any unique matching uris
                        if not r1: break                                        #          if collation is empty: unmatched index set - goto next
                else: r1 = []; break                                            #        else: unmatched index set - goto next
            if r1:                                                              #       if uris match this index set: (collate with matches from other index sets)
                if not r: r += r1                                               #        use as is if 1st matching index set
                else:                                                           #        else: combine with other index set matches
                    if 'consistent' in m:                                       #         according to consistency mode (if consistent):
                        if op != '~': r = r._union(r1)                          #          if unlike: all matching uris to be excluded
                        else: r = r._intersection(r1)                           #          if like: only uris in all matching index sets
                    else:                                                       #         if inconsistent matches allowed:
                        if op == '~': r = r._union(r1)                          #          if like: any uris from matching index sets
                        else: r = r._intersection(r1)                           #          if unlike: only uris in all matching index sets to be excluded
        return r

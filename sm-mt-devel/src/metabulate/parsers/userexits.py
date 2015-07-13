'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

Created on 17 Dec 2009
userexits02.py cloned from userexits01.py 10 Mar 2010
userexits02a.py cloned from userexits02.py 16 Mar 2010
userexits.py cloned from userexits02.py 07 Jul 2010
Last Updated on 07 Jul 2010

User supplied parsing exists for clauses.

Purpose:
    Performance. Some clauses may be parsed faster direct with python particularly if these may be deeply recursed
     and subject to later sub-parsing anyway. - e.g. triples as value expressions supplied below
To use:
    1. User tests must be defined in the rhs of BNF clauses within curly brackets. e.g.
        <triples> ::- {_getTriples()}
    2. Python code for user tests must be defined as Element methods below:
        2.1. the element they test is stored in self._val
        2.2. additional method parameters can be supported and would be obtained direct from the BNF
        2.3. the method should return the parsed element if it succeeds, or False if it fails

10/03/2010 userexits02.py cloned from userexits01.py:
    adjusted to succeed with partial leading match returning smatch and bmatch

16/03/2010 userexits02a.py cloned from userexits02.py:

16/03/2010:
    re-engineered to only split top level Queries not Values in QueryExpressions
    also 100% accurate extraction of parsed component of a partial parsing

07/07/2010 userexits.py cloned from userexits02.py for SVN versioning

Notes:
    1. from parse17.py test methods must return:
        null for failure, or
        [smatch,bmatch] for success

@author: Administrator
'''
class Element:
    def __init__(self,e):
        self._val = e.strip()
    def _getTriples(self):
        r = []
        bmatch = []
        smatch = ''
        brackets = 0
        start = None
        end = None
        first = None
        getnext = True
        getsep = False
        for c,v in enumerate(self._val):
#            print ('c=',c,'v=',v,'brackets=',brackets,'first=',first,'start=',start,'end=',end)
            if v == '(':
                if not brackets and getnext:
                    if start is None: first = c
                    start = c
                    getnext = False
                brackets += 1
            elif v == ')':
                brackets -= 1
                if not brackets:
#                    print ('brackets=',brackets,'s=',self._val[start:c+1])
                    try:
                        triple = eval(self._val[start:c+1])
                        if isinstance(triple,tuple) and len(triple) == 3:
                            bmatch += [triple]
                            end = c+1
                            getsep = True
                    except: pass
            elif v == '|' and getsep:
                getnext = True
                getsep = False
            elif v != ' ' and (getnext or getsep): break
        if bmatch:
            smatch = self._val[first:end]
            r = [smatch,bmatch]
        return r

class Test:
    def __init__(self,t):
        self._test = t
    def _eval(self,s):
        return eval('s.'+self._test)

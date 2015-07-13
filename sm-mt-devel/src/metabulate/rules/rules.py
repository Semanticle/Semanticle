'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

rules13.py Created on 06 Jan 2010
rules14.py Cloned from rules13.py on 25 Jan 2010
rules15.py Cloned from rules14.py on 28 Jan 2010
rules16.py Cloned from rules15.py on 20 Feb 2010
rules17.py Cloned from rules16.py on 13 Mar 2010
rules18.py Cloned from rules17.py on 18 Mar 2010
rules19.py Cloned from rules18.py on 21 Mar 2010
rules20.py Cloned from rules19.py on 29 Mar 2010
rules21.py Cloned from rules20.py on 02 Apr 2010
rules22.py Cloned from rules21.py on 12 Apr 2010
rules23.py Cloned from rules22.py on 19 Apr 2010
rules24.py Cloned from rules23.py on 06 May 2010
rules25.py Cloned from rules24.py on 12 May 2010
rules26.py Cloned from rules25.py on 05 Jun 2010
rules27.py Cloned from rules26.py on 12 Jun 2010
rules.py Cloned from rules27.py on 07 Jul 2010
Last Updated on 03 Dec 2010

ABSTRACT:
    Variant: supports query13.py

As rules12.py with:
    supports NOT clauses in queries and rules (via negated QueryLists in QueryEquations)
     - requirs query09 and solutions16

09/01/2010:
    exploits Queryables support for automated ordering of QueryLists in an equation to handle both
     recursive rule clauses and negated clauses.
    debug outputs updated

13/01/2010:
    - Rule._mergeRhs() merges a new rhs Equation or EquationList with(out) same variables into existing rhs
       - exploited by STS._actionPredicate()
    - Rule._interpolate() inputs key lists from STS._solveQuery() or new lhs triple from Rule._mergeRhs()

16/01/2010:
    Configurable Exception Handling - exploits mterrors

25/01/2010 rules14.py cloned from rules13.py:
    - valre regex updated to:
      - extract lone values
      - avoid extracting variables as values (ie value = ? or "'?'")
    _interpolate1() due to valre update now interpolates element expressions from rule variables matched with lone query values
    _solve():
      - inputs isGenericRule parameter and
      - passes isGenericRule to mtsuss._solveEquationList()

26/01/2010:
    - valre regex further refined - excludes invalid quoting
    _solve():
      - process contributory rules
      - yield changed to triples,rules,bindings

28/01/2010 rules15.py cloned from rules14.py:
    - supporting updated stores40 handling recursive generic rules

04/02/2010:
    - supports interpolation of query variables within nested triples:
       - _interpolate2() defained to extract such query variables
       - _interpolate1() exploits interpolate2()

18/02/2010:
    _interpolate1() listed rule elements handled differently (bug fix)

19/02/2010:
    _interpolate() key collation from nlhs revised (bug fux)

20/02/2010 rules16.py cloned from rules15.py:
    - Rule._interpolate() re-defined to exploit Query._interpolate()

21/02/2010:
    - new prefs to control cardinality of embedded Rule QueryElements:
       - Queryable instantiation now passes relevant pluralOK preference

02/03/2010:
    - singleton03 exploited

13/03/2010 rules17.py cloned from rules16.py:
    - latest Stores/Queryables refactoring exploited

18/03/2010 rules18.py cloned from rules17.py:
    - exploits non-infered QueryExpression comperands

21/03/2010 rules19.py cloned from rules18.py:
    Rule._express() defined

22/03/2010: _express() further refined.

29/03/2010 rules20.py cloned from rules19.py:
    - _solve() refactoring exploited
    - Result._setEquations() also sets _equationList
    - Result._getEquationList() method added
    - Rule._solve invokes Rule._getEquationList()._solve()
    - support for choice of solution methods dropped - therefore mtsuss import dropped

02/04/2010 rules21.py cloned from rules20.py with:
    - exploits refactored mtstores for DistSimpleTripleStore support

07/04/2010 exploits mtutils._genericSetter()/_genericGetter() for just in time attribute instantiation

08/04/2010: hardcoded config and prefs also defined

09/04/2010 standardisation of getter/setter and attribution syntax: (checked nothing required)
    _get(), _set(), _update() and __init__() methods checked regarding attribution.
    General rule is to reserve getters and setters to externally accessible and decorated attributes.
    These can also be used for just in time attribution (though this isn't currently so outside of the former criteria).
    Attribute setting via _update and __init__ strictly for external accessible attributes.
    Code changed throughout to access all other undecorated attributes directly.
    Python property not currently used to map _get/_set to direct attribute access syntax.

12/04/2010 rules22.py cloned from rules21.py with:
    Rule._mergeRhs() supports optional error propogation needed for revised STS._processTriple()

14/04/2010:
    Relating to merging of rules variants accessed when querying a DSTS:
     - Rule._mergeRhs() supports input of rule to be merged as an alternative to its lhs/rhs parts
     - Rule._mergeRhs() appends clauses to rhs within a new EquationList (rather than the existing one)
        otherwise this rhs might not get expanded correctly because of the expansion cache

19/04/2010 rules23.py cloned from rules22.py with:
    - Persistent Triple Stores supported

29/04/2010 Result._exists() method defined

06/05/2010 rules24.py cloned from rules23.py with:
    - URI support exploited via updated imports

12/05/2010 support for URI transformations within rules:
    - Rule._express() now inputs additional parameters for uri expression needed plus source and target stores

12/05/2010 rules25.py cloned from rules24.py with:
    - explicit alias_ontology support (via imports)

05/06/2010 rules26.py cloned from rules25.py with:
    - supports query trace results via imports

12/06/2010 rules27.py cloned from rules26.py with:
    - folders re-configured

07/07/2010 rules.py cloned from rules27.py for SVN versioning

12/07/2010 settings support interpetation of config variables

01/08/2010 simpler query interface supported:
    - Result._setEquations() supports:
       - submitting full {lhs:rhs} query syntax with
       - lhs setting a simple mtrender.Sequence(pattern=[lhs])
    - Result._generate() output checks improved:
       - performs output checks for default display only once

02/08/2010 Result._generate():
    - generation of result termination string
    - inheritted from Facade (if not False)
    - but can be overridden by Result terminator
    - submitted if not False to Content._termination() where it may be overidden by output and/or File target specific terminators

03/08/2010 enhanced headers and footers:
    - terminator renamed as footer
    - headers added
    - both headers and footers support various optional variable substitutions

06/08/2010 ad-hoc "sticky" header footer string and variable updates supported

09/08/2010 Rule._solve() only binds query variables where equivalent rule variable is unified

18/08/2010 Queryables instantiation now exploits new auto unique classes

24/08/2010:
    - Forwards compatability updates between P2.6/7 and P3
      in handling support of keys(), iteritems(), sort(), map(), itemgetter() and has_key().
    - Equation re-ordering for recursion fails when merging rules.
      Lhs now passed in Rule._mergeRhs() call to instantiate the new EquationList being merged.
      (Note: this isn't the result of the merge.)

30/08/2010 performance enhancements:
    - Rule._solve() passes through the current Query._solve() recursion depth.

02/09/2010 for compatability with qid mismatch fix in query.py
    - Rule._solve() qkeys renamed iqkeys
    - Rule/Result Queryables instantiation calls Queryable._getUnique(object) rather than U.. Queryables class

07/09/2010 Result._generate() receives new infer paramter:
    - to turn this on/off on an ad-hoc basis.
    - required to force inference while re-generating fed forward inference data if set.

21/09/2010:

21/09/2010: Rule._solve() binds and exposes variables from inside nested Queryables:
    - passes return substitution set to Queryables so solely nested variables may be identified by a naming prefix '!*'
    - tests returned variable bindings for this naming prefix
    - if present these get bound without being in rs.

17/10/2010: Stage 2. Mixed triple ordering support: (mixed triple ordering in rules)
    - Rule._rtClone() added to support mixed triple ordering within a DistTripleStore:
        - clones self with triples re-ordered from source to target store order)
        - exploited by Query._solve() retrieved rule merging segment

19/10/2010 Stage 3. Mixed triple ordering support: (import and export)
    - Rule._express() updated:
        - orderStore paramter added.
        - store and target parameters renamed to sourceStore and targetStore
        - re-ordering exploits TripleStore._expandTriple()

20/10/2010 Compliance with mtstores refactoring, plus:
    - Rules._expandMatch() refactored to _expandRule()

22/10/2010: Stage 5:  Mixed triple ordering support: Optional re-ordering for IO:
    - Result._rtClone() clones Queryable re-reordered from ioTripleOrder to tripleOrder
    
03/12/2010: Result._generate infer parameter documentation update

@author: Administrator
'''

import re, copy, time
import metabulate.utils.utils           as mtutils
import metabulate.utils.debug           as mtdebug
import metabulate.utils.errors          as mterrors
import metabulate.singletons.singleton  as mtsingleton
import metabulate.queries.query         as mtquery
import metabulate.renderers.render      as mtrender
import metabulate.renderers.protocol    as mtprotocol
import metabulate.stores.structured     as mtstruct

mtprefs  = mtsingleton.Settings()._getItem('prefs')
apQErr = mtutils._logical(mtprefs._interpretItem('Allow_plural_QueryElement_in_ruleRHS','true'))
apQErl = mtutils._logical(mtprefs._interpretItem('Allow_plural_QueryElement_in_ruleLHS','true'))

class Result:
    _default_outputs = []
    _default_header  = None                                                     # default output header (IE. Facade header)
    _default_footer  = None                                                     # default output footer (IE. Facade footer)
    _default_author  = None                                                     # author variable for value substitution in headers and footers
    _default_title   = None                                                     # title variable for value substitution in headers and footers
    _default_request = mtquery.Queryable._getUnique(mtquery.EquationList())

    def __init__(self
                ,outputs=None
                ,request=None
                ,header=None
                ,footer=None
                ,author=None
                ,title=None
                 ):
        self._update(outputs=outputs
                    ,request=request
                    ,header=header
                    ,footer=footer
                    ,author=author
                    ,title=title
                     )
    def _update(self
               ,outputs=None
               ,request=None
               ,header=None
               ,footer=None
               ,author=None
               ,title=None
               ):
        if outputs is not None: self._setOutputs(*outputs)
        if request is not None: self._setRequest(request)
        if header  is not None: self._setHeader(header)
        if footer  is not None: self._setFooter(footer)
        if author  is not None: self._setAuthor(author)
        if title   is not None: self._setTitle(title)
    def _setOutputs(self,*args):
        return mtutils._genericSetter(self,'outputs',args,t=mtrender.Output,plural=True)
    def _getOutputs(self,default=True):
        return mtutils._genericGetter(self,'outputs',default)
    def _setRequest(self,request,ruleLHS=None):
        # usage:
        #    instantiate a result (either a Query or a Rule)
        # inputs:
        #    request - either:
        #               - an RHS or
        #               - an {LHS:RHS} pair expressed as a dict for queries only
        #    ruleLHS - LHS for rules
        # processing:
        #    ruleLHS if submitted overrides LHS submitted via request and:
        #            - gets submitted as lhs to Queryables
        #            - does NOT get submitted to self._setOutputs()
        #    LHS if submitted without ruleLHS:
        #            - gets submitted as lhs to Queryables
        #            - get submitted to self._setOutputs()
        # returns:
        #    self._equations
        # notes:
        #    only accepts single item dicts in args[0] - IE. supports single queries only
        #    multiple queries can be chained via facade.
        outputs1 = ''                                                               # default outputs1
        request1 = ''                                                               # default request1
        if request:                                                                 # if new request supplied:
            if not isinstance(request,dict): request = {'':request}                 #  standardise request to (output:equation} format
            if len(request) == 1:                                                   #  only proceed if one request pair is supplied
                for lhs,rhs in request.items():                                 #   get that lhs:rhs pair
                    if ruleLHS is not None: lhs = ruleLHS                           #   if ruleLHS supplied: use it as lhs
                    elif (lhs                                                       #   elif lhs exists
                      and (isinstance(lhs,tuple)                                    #    and (lhs is a tuple or a string)
                         or isinstance(lhs,basestring))
                          ):
                        try: outputs1 = [mtrender.Sequence(pattern=[lhs])]          #    try: instantiating lhs as a Sequence
                        except mterrors.MTerror, X:                                 #    except:
                            X._notify(c='Result',
                                      m='_setRequest()')                            #     notify MTerror
                    try:                                                            #  try:
                        request1 = mtquery.Queryable(match=rhs                      #   instantiating rhs as a Queryable
                                                    ,lhs=lhs                        #   with rhs validated against lhs
                                                    ,pOK=apQErr
                                                     )._getMatch()                  #   getting the EquationList
                    except mterrors.MTerror, X:                                     #  except:
                        X._notify(c='Result',
                                  m='_setRequest()')                                #   notify MTerror
        if request1: self._request = request1                                       # complete request setting
        if outputs1: self._setOutputs(outputs1)                                     # complete outputs setting
        return self._request
    def _getRequest(self,default=True):
        return mtutils._genericGetter(self,'request',default)
    def _setHeader(self,*args):
        return mtutils._genericSetter(self,'header',args)
    def _getHeader(self,default=True):
        return mtutils._genericGetter(self,'header',default)
    def _setFooter(self,*args):
        return mtutils._genericSetter(self,'footer',args)
    def _getFooter(self,default=True):
        return mtutils._genericGetter(self,'footer',default)
    def _setAuthor(self,*args):
        return mtutils._genericSetter(self,'author',args)
    def _getAuthor(self,default=True):
        return mtutils._genericGetter(self,'author',default)
    def _setTitle(self,*args):
        return mtutils._genericSetter(self,'title',args)
    def _getTitle(self,default=True):
        return mtutils._genericGetter(self,'title',default)
    def _showDebug(self,
                   clas='',
                   method='',
                   note='',
                   vars=[],
                   line='',
                   level=2):
        mtdebug.Debug()._notify(clas=clas,method=method,note=note,line=line,level=level,vars=vars)
    def _generate(self
                 ,store
                 ,request=None
                 ,outputs=None
                 ,header=None
                 ,footer=None
                 ,author=None
                 ,title=None
                 ,bound=mtutils.sdict()
                 ,facade=None
                 ,infer=None
                  ):
        # usage:
        #    generate outputs from semantic web queries
        #    supports variety of OutputPatterns or renderings (triples|relations) and OutputProtocols (text|CSV|Relational)
        #    so its its the basic driver for plug and play query driven export
        # inputs:
        #    store   - triple store to query
        #    request - generate|export|instantiate
        #    outputs - targets (content objects to generate or stores/files to instantiate)
        #    header  - updated Result header string or False (if any)
        #    footer  - updated Result footer string or False (if any)
        #    author  - updated Result author string (if any)
        #    title   - updated Result title string (if any)
        #    bound   - variables constrained from start - input from import or a parent query process
        #    facade  - facde invoking object if any
        #    infer   - use inference to solve [True|False|None|'ffi'] - overrides local or preference settings
        def defaultheadfoot(role,hfstring,hfvars):
            if hfstring is not False:
                if not outputs:
                    hfstring = hfvars._doSubs(hfstring)
                    print hfstring
                else:
                    for output in outputs:
                        output._defaultheadfooter(role
                                                 ,hfstring
                                                 ,hfvars
                                                  )
        self._update(request=request                                                # instantiate ad-hoc Result instance variables
                    ,outputs=outputs                                                #  as "sticky" updates
                    ,header=header
                    ,footer=footer
                    ,author=author
                    ,title=title
                     )
        self._showDebug(clas='Result',method='_generate',note='inputs',line=385,level=0,vars=[['store',store],['request',request],['outputs',outputs],['bound',bound]])
        display = False                                                             # default no display
        outputs = self._getOutputs()                                                # check outputs or default to display
        for output in outputs:                                                      # for each output (if any):
            if 'display' in output._getTargets():                                   #  if display is a target:
                display = True                                                      #   set display on
                break                                                               #   quit check
        for output in outputs:                                                      # for each output (if any):
            if not (display or output._getTargets()):                               #   if no supplied target or no display
                output._setTargets('display')                                       #    set target to display
        if facade is not None:                                                      # if facade not None: default to its variables for
            header = facade._getHeader()                                            #  header
            footer = facade._getFooter()                                            #  footer
            author = facade._getAuthor()                                            #  author
            title  = facade._getTitle()                                             #  title
        if header is not False:                                                     # attempt overriding Facade header if not False
            header1 = self._getHeader()                                             #  with Result header
            if header1 is not None: header = header1                                #  if not None
        if footer is not False:                                                     # attempt overriding Facade footer if not False
            footer1 = self._getFooter()                                             #  with Result footer
            if footer1 is not None: footer = footer1                                #  if not None
        author1 = self._getAuthor()                                                 # attempt overriding Facade author
        if author1 is not None: author = author1                                    #  with Result author if not None
        title1 = self._getTitle()                                                   # attempt overriding Facade title
        if title1 is not None: title = title1                                       #  with Result title if not None
        hfvars = mtutils.sdict()                                                    # header/footer variables dict
        hfvars['author'] = author                                                   # set author variable
        hfvars['title'] = title                                                     # set title variable
        start = time.time()                                                         # get start time
        hfvars['start'] = time.ctime()                                              # set formatted start time
        defaultheadfoot('header',header,hfvars)                                     # output header
        for i,t1 in enumerate(self._getRequest()._solve(store                       # for each enumerated solution:
                                                       ,bound=bound
                                                       ,mode='results'
                                                       ,infer=infer
                                                        )):
            self._showDebug(clas='Result',method='_generate',line=421,level=2,vars=[['t1',t1],['outputs',outputs]])
            if not outputs:                                                         #  if no outputs:
                v = [store._expandTriple(t) for t in t1['!triples']]                #   default to display of matching triples
                print mtprotocol.CsvProtocol()._translate(v,endline='no')
            else:                                                                   # generate specified outputs
                for output in outputs:                                              #  for each output:
                    output._generate(bound=t1                                       #   generate the output
                                    ,instance=i
                                    ,store=store
                                     )
        duration = time.time()-start                                                # get duration
        hfvars['end'] = time.ctime()                                                # set formatted end time
        hfvars['duration'] = str(round(duration*100)/100)+' seconds'                # set rounded duration string
        defaultheadfoot('footer',footer,hfvars)                                     # output footer
    def _exists(self
                 ,store
                 ,request=None
                 ,bound=mtutils.sdict()
                  ):
        # usage:
        #    checks if solutions exist to semantic web queries
        # inputs:
        #    store   - triple store to query
        #    request - generate|export|instantiate
        #    bound   - variables constrained from start - input from import or a parent query process
        # returns:
        #    exists  - True|False
        self._update(request=request)
        self._showDebug(clas='Result',method='_generate',note='inputs',line=449,level=0,vars=[['store',store],['request',request],['bound',bound]])
        exists = False
        for t1 in self._getRequest()._solve(store,bound=bound,mode='results'):
            exists = True
            break
        return exists
    def _rtClone(self,source,target,new=False):
        # usage:
        #    instantiates and returns a clone of self
        #    with RHS triple elements re-ordered from source to target store
        # inputs:
        #    source - source Store - assumes triples in RHS are ordered according to this store
        #    target - target Store - re-orders triples in RHS from source to target Store
        #    new    - always return a new Rule [True|False]. If False and RHS unchanged then self is returned
        # returns:
        #    rule with re-ordered triple elements in RHS (if applicable).
        if (target                                                                  # if a target store is supplied
        and source != target                                                        #  and its not the source store
        and source._getTripleOrder() != target._getTripleOrder()                    #  and they have different triple orders
            ):                                                                      #  : clone this rule for target
            clone = Result(request=self._getRequest()._expandMatch(sourceStore=source,targetStore=target)
                          ,outputs=self._getOutputs()
                          ,header=self._getHeader()
                          ,footer=self._getFooter()
                          ,author=self._getAuthor()
                          ,title=self._getTitle()
                           )                                                        #   reordering lhs and rhs triples.
        else:                                                                       # else rule is ok as is: but check if a copy is requested
            if new: clone = copy.deepcopy(self)                                     #  copy requested: make one
            else: clone = self                                                      #  else no copy: use self
        return clone                                                                # return (new) rule

class Rule(Result):
    def __init__(self
                ,lhs=None
                ,rhs=None
                ):
        Result.__init__(self)
        self._update(lhs=lhs,rhs=rhs)
    def _update(self
               ,outputs=None
               ,request=None
               ,header=None
               ,footer=None
               ,author=None
               ,title=None
               ,lhs=None
               ,rhs=None
               ,inferred=None
                ):
        if outputs is not None: self._setOutputs(outputs)
        if request is not None: self._setRequest(request)
        if header  is not None: self._setHeader(header)
        if footer  is not None: self._setFooter(footer)
        if author  is not None: self._setAuthor(author)
        if title   is not None: self._setTitle(title)
        if lhs     is not None: self._setLhs(lhs)
        if rhs     is not None: self._setRhs(rhs)
    def _setLhs(self, lhs):
        # usage:
        #    sets lhs via Result._outputs ensuring its a Sequence
        #     and optionally allowing the Sequence._outputs to be
        #     set to the inferred Store
        #     (ie. the slave store of the query store instantiating the rule)
        lhso = ''
        if isinstance(lhs,list) or isinstance(lhs,tuple):
            lhso = mtrender.Sequence()
            if not lhso._setPattern(pattern=[lhs]): lhso = ''; lhs = ''
        elif isinstance(lhs,mtrender.Sequence): lhso = lhs
        try:
            self._query = mtquery.Queryable._getUnique(mtquery.Query(match=tuple(lhs),pOK=apQErl))
            self._setOutputs(lhso)
        except mterrors.QueryExpressionError, X:
            X._notify(c='Rule',
                      m='_setLhs()')                                                # notify QueryExpressionError
        return lhs
    def _getLhs(self):
        # usage:
        #    return the fully expanded lhs pattern
        # note:
        #    uses 1st of listed _getOutputs()
        #    if all output Sequences are needed use self._getOutputs()
        return self._getOutputs()[0]._getPattern()
    def _setRhs(self, rhs):
        # usage:
        #    wrapper for Result._setEquations() also passing the lhs
        #     since the rhs of a rule is Queryable object which seperately stores the lhs using to check for recursion
        # inputs:
        #    rhs      - Queryables match value either a list or a pre-instantiated Queryable
        # returns:
        #    if set: instantiated Queryable._getMatch()
        #    else:   False
        return self._setRequest(rhs,ruleLHS=self._getLhs())
    def _getQuery(self): return self._query
    def _getRhs(self): return self._getRequest()
    def _express(self
                ,ordered=False
                ,thin=True
                ,asTriple=False
                ,errors=True
                ,uri=None
                ,sourceStore=None
                ,targetStore=None
                ,orderStore=None
                ,orderToSelf=False
                 ):
        # usage:
        #    expresses rule as a string suitable for export
        #    also wrapped by _expandMatch() for Queryables compatibility
        #    supports URI transformations
        # inputs:
        #    ordered  - reorders rhs clauses so they can be solved.
        #    thin     - eliminates expression of QueryElements as lists if they contain only one QueryExpression
        #    asTriple - represent as a triple ((lhs),':-',[rhs])
        #    errors   - what to do if rhs contains errors:
        #               False - omit eroneous clauses
        #               True  - comment eroneous clauses
        #               'ok'  - include eroneous clauses
        #    uri      - target URI format if transformation needed [export|native|forcenative|nativealias] see mtstores._expandTriple()
        #    sourceStore - source store for URI transformations
        #    targetStore - target store for URI transformations
        #    orderStore  - store on which triple ordering should be based (typically sourceStore, targetStore or None to ignore)
        # returns:
        #    if error - rule as a string
        #    if ok    - rule as a dict
        self._showDebug(clas='Rule',method='_express',note='inputs',line=549,level=0,vars=[['ordered',ordered],['thin',thin],['asTriple',asTriple],['errors',errors],['uri',uri]])
        self._showDebug(clas='Rule',method='_express',note='inputs',line=550,level=0,vars=[['sourceStore',sourceStore]])
        self._showDebug(clas='Rule',method='_express',note='inputs',line=551,level=0,vars=[['targetStore',targetStore]])
        self._showDebug(clas='Rule',method='_express',note='inputs',line=552,level=0,vars=[['orderStore',orderStore]])
        lhs = self._getLhs()[0]                                                     # get rule's full lhs
        equationList = self._getRhs()                                               # get rule's rhs as an EquationList
        self._showDebug(clas='Rule',method='_express',line=555,level=1,vars=[['lhs',lhs]])
        self._showDebug(clas='Rule',method='_express',line=556,level=1,vars=[['equationList',equationList]])
        suffix = prefix = ''                                                        # initialise null prefix and suffix
        rhs = equationList._expandMatch(thin=True)                                           # rhs = expanded validated Equation
        if not rhs and errors:                                                      # if rhs invalid but errors permitted:
            rhs = equationList._expandMatch(ordered=False,thin=True)                #  get invalid rhs (ie. without ordering)
            if errors is True:                                                      #  if errors to be commented
                prefix = '# '                                                       #   apply prefix and suffix comments
                suffix = ' # rhs missing at least one positive non recursive QueryList'
        self._showDebug(clas='Rule',method='_express',line=564,level=1,vars=[['rhs',rhs]])
        if rhs:                                                                     # if rhs not null: (this retest is needed)
            if (sourceStore is not None                                             #  if sourceStore specified
            and ((uri is not None and targetStore is not None)                      #   and URI might need re-expressing
              or (orderStore is not None and orderStore != sourceStore)             #   or triple elements re-ordering
                )):                                                                 #   : re-express lhs/rhs URIs and/or triple element ordering
                lhs = sourceStore._expandTriple(lhs,uri=uri,target=targetStore,order=orderStore,orderToSelf=orderToSelf)
                rhs = sourceStore._expandTriple(rhs,uri=uri,target=targetStore,order=orderStore,orderToSelf=orderToSelf)
                self._showDebug(clas='Rule',method='_express',line=572,level=2,vars=[['lhs',lhs]])
                self._showDebug(clas='Rule',method='_express',line=573,level=2,vars=[['rhs',rhs]])
            if asTriple:                                                            #  if rules to be expressed as triples:
                rule = (lhs,':-',rhs)                                               #   express as a triple
                if orderStore is not None: rule = orderStore._rt(rule)              #   if orderStore is not None: reorder the triple
            else: rule = {lhs:rhs}                                                  #  else: express as a lhs:rhs pair
            if prefix: rule = prefix+str(rule)+suffix                               #  if commented rhs error: express rule as a string with comments
            self._showDebug(clas='Rule',method='_express',note='returns',line=579,level=0,vars=[['rule',rule]])
            return rule                                                             #  return rule string (with linefeed)
    def _expandRule(self,ordered=False,thin=True,asTriple=False,errors='ok'):
        return self._express(ordered=ordered,thin=thin,asTriple=asTriple,errors=errors)
    def _mergeRhs(self,nlhs=None,nrhs=None,nrule=None,propogateErrors=False):
        # usage:
        #    merges new rhs into existing rhs
        #     automatically variable consistency between new and old
        #     comparing the new lhs with the existing and switching
        #     different new lhs variables to their equivalent existing ones within the merged rhs
        #    also protects unswapped local variables from potential clashes with swapped variables (by Query._setMatch())
        # inputs:
        #    nlhs            - tuple representing new lhs triple (required to match variables)
        #    nrhs            - python structure representing the new rhs (either an EquationList or Equation) expanded or compact
        #    propogateErrors - pass errors received onto to calling method [True|false].
        # returns:
        #    merged and instantiated rhs
        self._showDebug(clas='Rule',method='_mergeRhs',line=596,level=1,vars=[['nlhs',nlhs],['nrhs',nrhs]])
        rhs = self._getRhs()                                                        # get existing rhs
        lhs = self._getQuery()                                                      # get existing lhs as a Query
        self._showDebug(clas='Rule',method='_mergeRhs',line=599,level=1,vars=[['lhs',lhs],['rhs',rhs]])
        if nrule and isinstance(nrule,Rule):
            vs,rs,bd = nrule._interpolate(lhs)
            nrhs = nrule._getRhs()._expandMatch(thin=True)
        elif nlhs is not None and nrhs is not None:
            vs,rs,bd = Rule(lhs=nlhs)._interpolate(lhs)                             # get rs - dict of new to existing variable swaps
        self._showDebug(clas='Rule',method='_mergeRhs',line=605,level=1,vars=[['rs',rs]])
        try:                                                                        # try:
            self._showDebug(clas='Rule',method='_mergeRhs',line=607,note='summary',level=1,vars=[['   lhs',lhs._expandMatch()]])
            equations=mtquery.Queryable(match=nrhs
                                       ,rs=rs
                                       ,lhs=self._getLhs()
                                       ,pOK=apQErr
                                        )._getMatch()                               #  get constructed EquationList for new rhs
            self._showDebug(clas='Rule',method='_mergeRhs',line=613,note='summary',level=1,vars=[['   rhs',rhs._expandMatch()]])
            self._showDebug(clas='Rule',method='_mergeRhs',line=614,note='summary',level=1,vars=[[' + rhs',equations._expandMatch()]])
        except mterrors.MTerror, X:
            X._notify(c='Rule',
                      m='_mergeRhs()')                                              #  notify MTerror
            if propogateErrors: raise mterrors.MTerror()                            #   if propogate Errors: re-raise as an MTerror
        else:                                                                       # ok: proceed..
            for equation in equations._getMatch():                                  #  for each Equation in EquationList:
                self._showDebug(clas='Rule',method='_mergeRhs',line=621,level=2,vars=[['rhs',rhs],['equation',equation]])
                self._showDebug(clas='Rule',method='_mergeRhs',line=622,level=2,vars=[['equation._expandMatch(thin=True)',equation._expandMatch(thin=True)],['rhs._expandMatch(thin=True)',rhs._expandMatch(thin=True)]])
#                if equation._expandMatch() not in rhs._expandMatch():               #   if expanded Equation new to current rhs:
                if equation not in rhs._getMatch():                                 #   if Equation new to current rhs:
                    self._showDebug(clas='Rule',method='_mergeRhs',line=625,level=2,vars=[['rhs._getMatch()+[equation]',rhs._getMatch()+[equation]]])
                    try:                                                            #    try setting updated rhs:
                        rhs = mtquery.Queryable._getUnique(mtquery.EquationList(match=rhs._getMatch()+[equation])
                                                           )                        #   append Equation to rhs EquationList for new rhs
                        self._setRhs(rhs)                                           #     and reset as rule's updated rhs
                        self._showDebug(clas='Rule',method='_mergeRhs',line=630,note='summary',level=1,vars=[[' = rhs',rhs._expandMatch()]])
                    except mterrors.QueryableError, X:                              #    except rhs error:
                        X._notify(c='Rule',
                                  m='_mergeRhs()')                                  #     notify QueryableError
                        if propogateErrors: raise mterrors.MTerror()                #     if propogate Errors: re-raise as an MTerror
        return self._getRhs()                                                       # return the updated rhs
    def _rtClone(self,source,target,new=False):
        # usage:
        #    instantiates and returns a clone of self
        #    with RHS triple elements re-ordered from source to target store
        # inputs:
        #    source - source Store - assumes triples in RHS are ordered according to this store
        #    target - target Store - re-orders triples in RHS from source to target Store
        #    new    - always return a new Rule [True|False]. If False and RHS unchanged then self is returned
        # returns:
        #    rule with re-ordered triple elements in RHS (if applicable).
        if (target                                                                  # if a target store is supplied
        and source != target                                                        #  and its not the source store
        and source._getTripleOrder() != target._getTripleOrder()                    #  and they have different triple orders
            ):                                                                      #  : clone this rule for target
            clone = Rule(lhs=self._getQuery()._expandMatch(sourceStore=source,targetStore=target,thin=True)
                        ,rhs=self._getRhs()._expandMatch(sourceStore=source,targetStore=target)
                         )                                                          #   reordering lhs and rhs triples.
        else:                                                                       # else rule is ok as is: but check if a copy is requested
            if new: clone = copy.deepcopy(self)                                     #  copy requested: make one
            else: clone = self                                                      #  else no copy: use self
        return clone                                                                # return (new) rule
    def _interpolate(self,query):
        # usage:
        #    passes query values between calling Query variables and implementing Rule variables
        #    wrapper for Query._interpolate()
        # inputs:
        #    self  - implementing (invoked) Rule
        #    query - calling (invoking) Query or query variables as triple
        # returns:
        #    vs    - variable substitution dict {solving_var1:[querying Qexp1.1_with_solving_var1,..,querying Qexp1.n_with_solving_var1],..}
        #    rs    - return substitutions dict  {solving_var1:[querying_var1.1,..querying_var1.n],..,solving_varN:[querying_varsN]}
        #            i.e. dict of local (not nested) querying variables indexed by solving variables
        #    bd    - dict of bindings detected from interpolation ie. {'qvarname1':'val1',...}
        #            (typically where the rule predicate equates with a query variable)
        self._showDebug(clas='Rule',method='_interpolate',note='inputs',line=670,level=0,vars=[['query',query]])
        vs,rs,bd = self._getQuery()._interpolate(query)
        self._showDebug(clas='Rule',method='_interpolate',note='returns',line=672,level=0,vars=[['vs',vs],['rs',rs],['bd',bd]])
        return vs,rs,bd
    def _solve(self,query,gr=None,rikeys=None,store=None,rd=None,infer=None):
        # usage:
        #    for solving rules within Query objects
        #    ie. "private" method called by TripleStore._solveQuery()
        # method:
        #    interpolates (passes values between) Rule variables from Query variables
        #     (remember the rule is defined with its own local variables)
        #    invoke Solution._solveEquationList() against the rule
        #     (remember the rule lhs is an EquationList (and rhs a Rendering Sequence))
        #    unifies resulting values with original query variables
        #    clears unwanted rule variable bindings
        # inputs:
        #    query    - query values as a Query object, or Query object match
        #    gr       - generic rule identifier (if applicable)
        #    rikeys   - recursed infered keys - tracing recursive inference
        #    store    - query TripleStore
        #    rd       - recursion depth
        #    infer   - use inference to solve [True|False|None|'->ffi'|'<-ffi'] - overrides local or preference settings
        # yields:
        #    triples  - list of contributory triples (as tuples)
        #    rules    - list of contributory rules (as rules)
        #    bindings - solving query values indexed by query variables (note returns query not rule variables)
        self._showDebug(clas='Rule',method='_solve',note='inputs',line=696,level=0,vars=[['query',query],['gr',gr],['store',store]])
        if (store is not None
        and isinstance(store,mtstruct.A_TripleStore)):                              # no point continuing if store invalid
            vs,rs,bd = self._getQuery()._interpolate(query)                         #  get value/variable + return substitution indexes
            self._showDebug(clas='Rule',method='_solve',line=700,level=1,vars=[['mtquery._expandVS(vs)',mtquery._expandVS(vs)],['vs',vs]])
            self._showDebug(clas='Rule',method='_solve',line=701,level=1,vars=[['rs',rs],['bd',bd]])
            for [triples,rules,bindings] in self._getRequest()._solve(store
                                                                     ,vs=vs
                                                                     ,rs=rs
                                                                     ,bound=bd
                                                                     ,mode='rule'
                                                                     ,gr=gr
                                                                     ,rikeys=rikeys
                                                                     ,rd=rd
                                                                     ,infer=infer
                                                                      ):            #  for each rule solution get enumerated results
                self._showDebug(clas='Rule',method='_solve',note='>>  ',line=712,level=2,vars=[['mtquery._expandVS(vs)',mtquery._expandVS(vs)],['vs',vs]])
                self._showDebug(clas='Rule',method='_solve',note='>>  ',line=713,level=2,vars=[['rs',rs]])
                self._showDebug(clas='Rule',method='_solve',note='>>  ',line=714,level=2,vars=[['bindings',bindings]])
                self._showDebug(clas='Rule',method='_solve',note='summary',line=715,level=1,vars=[['local variables',rs]])
                self._showDebug(clas='Rule',method='_solve',note='summary',line=716,level=1,vars=[['  curr bindings',bd]])
                self._showDebug(clas='Rule',method='_solve',note='summary',line=717,level=1,vars=[[' local bindings',bindings]])
                if rs:                                                              #   if return substitutions:
                    b = copy.deepcopy(bd)                                           #    if bindings to be substituted:
                    self._showDebug(clas='Rule',method='_solve',note='>>> ',line=720,level=2,vars=[['b',b]])
                    for rvarname in rs:                                             #    for each rule variable:
                        if rvarname in bindings:                                    #     if rule variable is unified:
                            for qvarname in rs[rvarname]:                           #      for each associated query variable:
                                b[qvarname] = bindings[rvarname]                    #       unify query variable to rule variable value
                    for rvarname in bindings:                                       #    expose extra pre-solved variables (not in rs)
                        if rvarname[:2] == '!*':                                    #     for each extra variable:
                            b._matchUnion({rvarname[2:]:bindings[rvarname]})        #     union its actual varname with the new bindings
                    self._showDebug(clas='Rule',method='_solve',note='>>> ',line=728,level=2,vars=[['b',b]])
                    self._showDebug(clas='Rule',method='_solve',note='summary',line=729,level=1,vars=[['  new bindings',bindings]])
                    self._showDebug(clas='Rule',method='_solve',note='yields',line=730,level=0,vars=[['triples',triples],['rules',rules],['b',b]])
                    yield triples,rules,b                                           #    yield results (named for scope of query)

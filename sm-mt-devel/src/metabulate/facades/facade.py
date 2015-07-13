'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

facade33.py Created on 06 Jan 2010
facade34.py Cloned from facade33.py on 25 Jan 2010
facade35.py Cloned from facade34.py on 28 Jan 2010
facade36.py Cloned from facade35.py on 04 Feb 2010
facade37.py Cloned from facade36.py on 26 Feb 2010
facade38.py Cloned from facade37.py on 13 Mar 2010
facade39.py Cloned from facade38.py on 18 Mar 2010
facade40.py Cloned from facade39.py on 24 Mar 2010
facade41.py Cloned from facade40.py on 29 Mar 2010
facade42.py Cloned from facade41.py on 02 Apr 2010
facade43.py Cloned from facade42.py on 14 Apr 2010
facade44.py Cloned from facade43.py on 19 Apr 2010
facade45.py Cloned from facade44.py on 05 May 2010
facade46.py Cloned from facade45.py on 13 May 2010
facade47.py Cloned from facade46.py on 06 Jun 2010
facade48.py Cloned from facade47.py on 12 Jun 2010
facade.py Cloned from facade48.py on 07 Jul 2010
Last Updated on 03 Dec 2010

As facade32.py with:
    supports NOT clauses in queries and rules (via negated QueryLists in QueryEquations)

25/01/2010 facade34.py cloned from facade33.py:
    support testing of fully generic rules (test20r-16.py)

28/01/2010 facade35.py cloned from facade34.py:
    support extended testing of fully generic rules (test20r-17.py)

04/02/2010 facade36.py cloned from facade35.py:
    to support stores41.py

07/02/2010:
    several more metrics reported

09/02/2010:
    metrics reported for boolean queries:
     - total boolean queries,
     - successful boolean queries and
     - unique successful boolean queries

14/02/2010:
    metrics reported for successful non boolean queries

26/02/2010 facade37.py cloned from facade36.py:
    - exploits refactored Queryables

13/03/2010 facade38.py cloned from facade37.py:
    - latest Stores/Queryables refactoring exploited

18/03/2010 facade39.py cloned from facade38.py:
    - exploits non-infered QueryExpression comperands

24/03/2010 facade40.py cloned from facade39.py:
    - exploits nested rules within triples and round tripping of !triples/!rules outputs

29/03/2010 facade41.py cloned from facade40.py:
    - _solve() refactoring exploited
    - _generate() final metrics debug line moved to EquationList._solve()
    - support for choice of solution methods dropped - therefore mtsuss import dropped

02/04/2010 facade42.py cloned from facade41.py with:
    - exploits refactored mtstores for DistSimpleTripleStore support

07/04/2010 exploits mtutils._genericSetter()/_genericGetter() for just in time attribute instantiation

09/04/2010 standardisation of getter/setter and attribution syntax: (checked nothing required)
    _get(), _set(), _update() and __init__() methods checked regarding attribution.
    General rule is to reserve getters and setters to externally accessible and decorated attributes.
    These can also be used for just in time attribution (though this isn't currently so outside of the former criteria).
    Attribute setting via _update and __init__ strictly for external accessible attributes.
    Code changed throughout to access all other undecorated attributes directly.
    Python property not currently used to map _get/_set to direct attribute access syntax.

14/04/2010 facade43.py cloned from facade42.py with:
    - exploits merged queried rules support.

19/04/2010 facade44.py cloned from facade43.py with:
    - Persistent Triple Stores supported

05/05/2010 facade45.py cloned from facade44.py with:
    - URI support added

13/05/2010 facade46.py cloned from facade45.py with:
    - explicit alias_ontology support (via imports)

06/06/2010 facade47.py cloned from facade46.py with:
    - supports query trace results via imports

12/06/2010 facade48.py cloned from facade47.py with:
    - folders re-configured

07/07/2010 facade.py cloned from facade48.py for SVN versioning

02/08/2010 simpler interface extensions:
    - _setResults() supports:
       - mix and match Results Objects with ad-hoc results requests
       - automatically instantiates ad-hoc results requests as Results objects
    - _generate() supports output terminator settings from:
       - default ResultsTerminator pref or
       - generate call specific terminator param setting (if default is not False)

03/08/2010 enhanced headers and footers:
    - terminator renamed as footer
    - headers added
    - both headers and footers support various optional variable substitutions

06/08/2010 ad-hoc "sticky" header footer string and variable updates supported in Results via call from Facade._generate()

07/09/2010 _generate() receives new infer paramter to turn this off on an ad-hoc basis

22/10/2010: Stage 5:  Mixed triple ordering support: Optional re-ordering for IO:
    - Facade order setting supported represents the Facade ioTripleOrder
    - i.e. the order of triples expressed in Queryables thru the facade
    - Facade_generate() re-orders Result requests from ioTripleOrder to store TripleOrder

23/10/2010: Stage 5:  Mixed triple ordering support: Optional re-ordering for IO bug fixes:
    - Facade _setOrder()/_getOrder() bespoke coded:
        - generic setters/getters don't handle list parameters.
        - validates order before setting.

23/10/2010: _setObject() order parameter is optional.

03/12/2010: _generate updates:
    - update parameter added: optional sticky attribute updates
    - documentation updates

@author: Administrator
'''
import copy
import metabulate.stores.stores         as mtstores
import metabulate.rules.rules           as mtrules
import metabulate.utils.utils           as mtutils
import metabulate.utils.debug           as mtdebug
import metabulate.singletons.singleton  as mtsingleton

mtprefs  = mtsingleton.Settings()._getItem('prefs')

class Facade:
    _default_input   = ''
    _default_store   = ''
    _default_results = ''
    _default_header  = mtutils._logical(mtprefs._interpretItem('ResultsHeader','None')) # Default file output header
    _default_footer  = mtutils._logical(mtprefs._interpretItem('ResultsFooter','None')) # Default file output footer
    _default_author  = None
    _default_title   = None
    _default_order   = None

    def __init__(self
                ,input=None                             # input (import) Content object
                ,store=None                             # store object
                ,results=None                           # list of Result/Rule objects to process, may also include one or more dicts
                                                        # each specifying one or more extra Result objects to instantiate and process
                ,header=None                            # result header output (indicates a result request is completed in outputs)
                ,footer=None                            # result footer output (indicates a result request is completed in outputs)
                ,author=None                            # author variable for value substitution in headers and footers
                ,title=None                             # title variable for value substitution in headers and footers
                ,order=None                             # order of Triples submitted thru this facade (overrides store._ioTripleOrder)
                 ):
        self._update(input=input
                    ,store=store
                    ,results=results
                    ,header=header
                    ,footer=footer
                    ,author=author
                    ,title=title
                    ,order=order
                    )
    def _update(self
               ,input=None                              # input (import) Content object
               ,store=None                              # query store object
               ,results=None                            # list of Result/Rule objects to process
               ,header=None
               ,footer=None
               ,author=None
               ,title=None
               ,order=None
                ):
        # set any or all of the following instance and aggregated instance variables simultaneously
        #    from any method calling this including the constructor
        if input   is not None: self._setInput(input)
        if store   is not None: self._setStore(store)
        if results is not None: self._setResults(results)
        if header  is not None: self._setHeader(header)
        if footer  is not None: self._setFooter(footer)
        if author  is not None: self._setAuthor(author)
        if title   is not None: self._setTitle(title)
        if order   is not None: self._setOrder(order)
    def _setInput(self,*args):
        return mtutils._genericSetter(self,'input',args,t=mtrender.Input)
    def _getInput(self,default=True):
        return mtutils._genericGetter(self,'input',default)
    def _setStore(self,*args):
        return mtutils._genericSetter(self,'store',args,t=mtstores.TripleStore)
    def _getStore(self,default=True):
        return mtutils._genericGetter(self,'store',default)
    def _setResults(self,*args):
        # usage:
        #   sets results list from a mixed list of:
        #     - pre instantiated Results objects and/or
        #     - dicts of result requests to be instantiated as Result objects and adding to final Results set
        # inputs:
        #    args    - one or more mixed Result objects or result request dictionaries
        #              each of which may specify one or more Result objects for instantiation
        # returns:
        #    results - list of instantiated results objects
        def addResults(arg):
            results = []
            if isinstance(arg,list):
                for arg1 in arg: results += addResults(arg1)
            if isinstance(arg,dict):
                for lhs,rhs in arg.items():
                    try: results += [mtrules.Result(request={lhs:rhs})]
                    except mterrors.MTerror, X:                                     #  except:
                        X._notify(c='Facade',
                                  m='_setRequests()')                               #   notify MTerror
            elif isinstance(arg,mtrules.Result): results = [arg]
            return results
        results = []
        for arg in args: results += addResults(arg)
        return mtutils._genericSetter(self,'results',tuple(results),t=mtrules.Result,plural=True)
    def _getResults(self,default=True):
        return mtutils._genericGetter(self,'results',default)
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
    def _setOrder(self,order=None):
        if order and not mtstores.TripleStore()._testTorder(order): order = None
        self._order = order
        return order
    def _getOrder(self,default=True):
        try: return self._order
        except AttributeError: return self._setOrder()
    def _showDebug(self
                  ,clas=''
                  ,method=''
                  ,note=''
                  ,vars=[]
                  ,line=''
                  ,level=2
                   ):
        mtdebug.Debug()._notify(clas=clas,method=method,note=note,line=line,level=level,vars=vars)

    def _generate(self
                 ,store=None
                 ,results=None
                 ,header=None
                 ,footer=None
                 ,author=None
                 ,title=None
                 ,bound=mtutils.sdict()
                 ,infer=None
                 ,order=None
                 ,update=True
                  ):
        # generate outputs from semantic web queries
        # supports variety of OutputPatterns or renderings (triples|relations) and OutputProtocols (text|CSV|Relational)
        # so its its the basic driver for plug and play query driven export
        # usage:
        #    inputs:
        #        store      - triple store to query
        #        outputs    - outputs to generate
        #        header     - result output heading string or [None|False]
        #                      None  - not specified, try default, or try overiding with result or output specific headers
        #                      False - turns termination off overiding result or output specific headers
        #        footer     - result output footing string or [None|False]
        #                      None  - not specified, try default, or try overiding with result or output specific footers
        #                      False - turns termination off overiding result or output specific footers
        #        author     - run author variable for value substitution in headers and footers
        #        title      - run title variable for value substitution in headers and footers
        #        bound      - bound values to input
        #        infer      - inference setting [True|False|None|'ffi]
        #        order      - Triple Ordering for IO expressed as a sequence of 's','p' and 'o' characters.
        #        update     - update default store, results, header, footer, author, title and order object settings [True|False]
        #
        if update: self._update(store=store                                         # instantiate ad-hoc Content instance variables
                               ,results=results                                     #  as "sticky" updates
                               ,header=header
                               ,footer=footer
                               ,author=author
                               ,title=title
                               ,order=order
                                )
        self._showDebug(clas='Facade',method='_generate',note='inputs',line=264,level=0,vars=[['store',store],['results',results],['bound',bound]])
        if self._default_header is False: header = False                            # only use Facade specific header if default not False
        elif header is None: header = self._getHeader()
        if self._default_footer is False: footer = False                            # only use Facade specific footer if default not False
        elif footer is None: footer = self._getFooter()
        if author is None: author = self._getAuthor()
        if title  is None: title  = self._getTitle()
        store = self._getStore()
        order = self._getOrder()                                                    # get Facade triple order setting
        if not order: order = store._getIoTripleOrder()                             # otherwise get store ioTripleOrder setting (if any)
        if order: order = mtstores.TripleStore(tripleOrder=order)                   # if order setting found: express as a TripleStore
        for r in self._getResults():                                                # for each result request:
            if order: r = r._rtClone(order,store)                                   #  if re-ordering: do from (io)order to (store)order
            r._generate(store                                                       #  generate the results for re-ordered request
                       ,bound=bound
                       ,header=header
                       ,footer=footer
                       ,author=author
                       ,title=title
                       ,facade=self
                       ,infer=infer
                        )

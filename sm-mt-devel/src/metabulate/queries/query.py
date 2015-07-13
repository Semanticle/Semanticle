'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

supports splitting query keys into exact and inferred with handling of ambiguous keys
no longer calls on inference if ffi available and not being built - ie if its already built
NOTE: requires stores_splitkeys_06.py

Created on 05 Jan 2009
query10.py  Cloned from query09.py on 17 Feb 2010
query10a.py Cloned from query10.py on 19 Feb 2010
query10b.py Cloned from query10.py on 07 Mar 2010
query11.py  Cloned from query10.py on 13 Mar 2010
query11a.py Cloned from query11.py on 14 Mar 2010
query11b.py Cloned from query11.py on 14 Mar 2010
query12.py  Cloned from query11.py on 18 Mar 2010
query13.py  Cloned from query12.py on 28 Mar 2010
query14.py  Cloned from query13.py on 02 Apr 2010
query15.py  Cloned from query14.py on 14 Apr 2010
query16.py  Cloned from query15.py on 19 Apr 2010
query17.py  Cloned from query16.py on 01 May 2010
query18.py  Cloned from query17.py on 13 May 2010
query19.py  Cloned from query18.py on 05 Jun 2010
query20.py  Cloned from query19.py on 12 Jun 2010
query.py  Cloned from query20.py on 07 Jul 2010
Last Updated on 20 Oct 2010

As query08.py but:
    Supports NOT QueryLists as follows:
     - QueryList._setMatch() detects optional polarity indicator prefixing QueryList Queries
       supported by QueryList._setPolarity()/_getPolarity() methods
     - Equation._getMatch(ordered=True) returns lists of QueryLists with all EQ polarities first

09/01/2010:
    - Equation._getMatch() ordered defaults to True
    - Source Documentation and debug outputs updated
    - Equation._getMatch(ordered=True) also checks validity of recursive rules. Returning an empty equation if invalid.

01/01/2010:
    - Queryable._expandMatch() inputs ordered for detecting and handling rhs errors
    - Query._expandMatch() defines optional ordered parameter for compliance with Queryable - which gets ignored

11/01/2010:
    QueryList._getMatch() supports ordering by default to ensure what it returns may be consistently compared

13/01/2010:
    Query._setMatch().doSwap():
     - handles lists of replacement variables. ie. any one existing may be swapped for multiple replacements
     - ensures unswapped local variables won't clash with swapped replacements

16/01/2010:
    Configurable Exception Handling - exploits mterrors

17/02/2010 query10.py cloned from query09.py:
    QueryElement class defined as further subclass of Queryable
    QueryElement._setMatch() method defined exploiting parser

18/02/2010:
    - _expandVars() re-engineered to handle Query Expressions and Listed QueryElements in Query
    - Query._setrMatch.doSwap() refactored to QueryElement._swapMatch()
    - rrs parameter passed and input to all _setMatch() methods because:
       - QueryElement may nest QueryList in its value expression (stored in self._triples)
       - QueryElement may later nest higher Queryables, so rrs may be need to be generally passed around

19/02/2010:
    - _collateVars() method:
      - collates all unique query varnames in any Queryable object
      - defined for Queryable and overridden by QueryElement
    - 1st cut Query._interpolate() defined

19/02/2010 query10a.py cloned from query10.py

19/02/2010 further updates:
    - QueryElement class renamed QueryExpression
    - New QueryElement class defined which comprises one or more QueryExpressions
    - Query._setMatch() redefined

20/02/2010:
    - Query._interpolate() re-defined
    - QueryElement._interpolate() defined:
       - handles nested Queries even within QueryExpression value clauses
       - handles plural/mismatched query/local parameters
       - new errors detected

21/02/2010:
    - new prefs to control cardinality of embedded QueryElements:
       - Query._setMatch() enforces p(lural)OK parameter
       - pOK passed around within all Queryables
       - new error generated and trapped for pOK failure

22/02/2010:
    - QueryElement:
       - _setMatch() collates embedded Queries into a single QueryList
       - _collateExps() defined to collate QueryExpressions
       - _collateExps() value filtering according to Overlapping_QueryExpression_value_filter preference setting
    - QueryExpression:
       - _setMatch() optionally avoids parsing to instantiate directly (called from _collateExps())
       - __str__() defined for unique indexing of QEs
       - _setCvars() for setting replacement current variables for _solveQuery()
       - _cloneCvars() for default cvars setting

02/03/2010:
    - updated singleton Index exploited

10/03/2010:
    - wide ranging updates resulting in partially working refactored design

11/03/2010:
    - changedVarsClone() method for QueryList and QueryExpression clones either but with changed query variables
    - QueryElement._interpolate() handling of nested triples in Queries fixed

12/03/2010:
    - QueryValueExpression._setTriples():
       - enhanced flexibility
       - QueryList instantiation refactored from QueryExpression
    - Remaining Bugs fixed to support nested Triples within QueryValueExpressions
    - QueryElement._collateMatch() now skips collation when not needed

13/03/2010 query11.py cloned from query10.py:
    - expanded matches cached as Queryable ids indexed by ordered and thin parameter values
    - unique instantiation caches defined and exploited for:
       QueryValueExpression, QueryExpression, QueryElement, Query, QueryList and Equation objects

14/03/2010:
    - further slimming:
        - unecessary uniqueness indexes removed
          now that all Queryables are unique, the simpler list present in list check suffices for:
           - uexps in QueryElement._setMatch()/_collateVars(): QueryExpressions within a QueryElement
           - uexps in Query._interpolate.setVSvars(): QueryExpressions within a VS value list
        - therefore mtindex import no longer needed and removed
    - _swapMatch():
        - no longer operates on match but on vars directly
        - therefore:
           - renamed from _swapMatch() to _swapVars()
           - regex usage not needed. re import removed
           - QueryExpression._setMatch() exploitation adapted to swap vars and if needed reform match

15/03/2010:
    - QueryExpression: Handles nested lists or triples within triples nested inside QueryExpressions
      - _changedVarsClone() now handles cloning unset attributes
      - _setMatch() - also reforms match after parsing if nested triples inside the QueryValueExpression.
                      (this because the QueryElements within the nested triples may have had their QueryExpressions collated)

18/03/2010 query12.py cloned from query11.py:
    - exploits non-infered QueryExpression comperands

19/03/2010 further to exploiting non-infered QueryExpression comperands:
    - changes in QueryElement._collateMatch()
       - logic for preventing generation of rule search keys tightened and simplified
       - rule keys only generated if a list QueryExpressions contain QueryValueExpressions which are neither exact or '=' reserved predicates
       - also returns:
           - list of QueryExpression values for exclusively exact searches
           - global collated match and qkey (inferable and exact)
           - inferable only collated match and key
    - Query._makeKey() returns to Store._solveQuery() additional:
       - list of QueryExpression values for exclusively exact searches (one for each query element)
       - inferable query (instead of the previous query containing inferable and exact elements)
       - 2 query keys:
           - qkey (the previous qkey collating inferable and exact QueryExpression opmatches)
           - iqkey (containing only inferable QueryExpression opmatches)

28/03/2010 query13.py cloned from query12.py:
    - _solve() refactored:
      - moved from mtstores and mtsuss to here for EquationList, Equation, QueryList and Query classes

29/03/2010:
    - further to _solve() refactoring:
       - _getCache() function defined:
          - initialises caches
          - caches for filter and metrics implimented as nested dictionaries
          - passed between methods

02/04/2010 query14.py cloned from query13.py with:
    - exploits refactored mtstores for DistSimpleTripleStore support

04/04/2010 DSTS support:
    - in Query._solve():
       - mtstore._solveTriple() yields source store along with triples and bindings
       - rules managed in terms of their STS and DSTS ids
       - duplicate rules detected according to unique DSTS._resultStore id

05/04/2010 DSTS support:
    - in Query._solve():
       - inorder to report rules whether inferred or not its necessary to detect matched rules and
         instantiate them in DSTS._resultStore (seperate that is from detection of inferable rules)

08/04/2010:
    - hardcoded config and prefs also defined
    - stores._metrics exploited:
      - incMetric() and _setMetric() methods invoked
      - showMetrics() replaces debug metric lines

09/04/2010 standardisation of getter/setter and attribution syntax: (mtutils._genericGetter/_genericSetter not used here)
    _get(), _set(), _update() and __init__() methods checked regarding attribution.
    General rule is to reserve getters and setters to externally accessible and decorated attributes.
    These can also be used for just in time attribution (though this isn't currently so outside of the former criteria).
    Attribute setting via _update and __init__ strictly for external accessible attributes.
    Code changed throughout to access all other undecorated attributes directly.
    Python property not currently used to map _get/_set to direct attribute access syntax.

14/04/2010 query15.py cloned from query14.py with:
    Query._solve() handling relating to merging of rules variants accessed when querying a DSTS

19/04/2010 query16.py cloned from query15.py with:
    - Persistent Triple Stores supported:
    - Query._solve() uses of store._id_to_rules refactored to store._db['i>r']
    - imports updated

21/04/2010: Query._solve() supports optionally persistent DTS._resultStores
    - ie. DTS._resultStore re-expressed as DTS._db['rs']

27/04/2010: passes t rather than *t to mtstores._getIDfromTriple()

01/05/2010 query17.py cloned from query16.py with URI support implemented:
    - global astore initialised for pre-query URI interpretation
    - QueryValueExpression._setVals() passes vals thru astore._parseURI() and sets val to resultant 'has_uri' value

01/05/2010 query18.py cloned from query17.py with:
    - explicit alias_ontology support (via imports)

05/06/2010:
    - QueryElement._collate():
       - bug fixes to differentiation of inferable and non-inferable QueryExpressions
       - updated documentation
    - Query documentation updates:
       - _makeKey()
       - _solve()

05/06/2010 query19.py cloned from query18.py with:
    - Query and EquationList._solve() methods collate traced queries in results

12/06/2010 query20.py cloned from query19.py with:
    - folders re-configured

07/07/2010 query.py cloned from query20.py for SVN versioning

12/07/2010 settings support interpetation of config variables

08/08/2010:
    - supports generic representation of recursive relationships via more precise generic rule filter:
        - Query._solve():
            - inputs hierarchy of parent objects; QueryList, Equation and EquationList
            - generic rule filter only on full rule + QueryList
            - no more triple element ordering assumtions
        - QueryList._solve():
            - inputs hierarchy of parent objects; Equation and EquationList
            - passes to Query._solve() hierarchy of parent objects; QueryList, Equation and EquationList
        - Equation._solve():
            - inputs parent object; EquationList
            - passes to QueryList._solve() hierarchy of parent objects; Equation and EquationList
        - EquationList._solve():
            - passes to Equation._solve() parent object; EquationList
    - Queryable._setMatch() bug fix:
        - len(mixedTypes) == 1 rather than < 2, otherwise m2 below test may not be defined.
    - QueryElement._collateMatch() only set inferable match (imatch) if its exists.

13/08/2010 queries passed to Query objects are logically ANDed to derive the actual QueryElements:
    - Query._makeKey.applyVS():
        - refactored to QueryElement._applyVS()
        - calls QueryExpression._AND() to unify QueryElements of input with itself
    - QueryElement._applyVS() added as above.
    - QueryValueExpression():
        - _getXxx() all handle uninstantiated variables.
    - QueryExpression():
        - _getAll() gets all variables needed to re-instate a QueryExpression
        - _changedVarsClone() exploits _getAll()
        - _AND() added:
            - handles logical ANDing of an input QueryExpression with self
            - exploits _getAll()

14/08/2010 refined logical ANDing of parameters for Query unification:
    - QueryExpression._AND()
    - QueryElement._applyVS()
        - raises interpolation error where logical ANDing fails
        - error reported by Query._makeKey()
        - error propogated back to Query._solve() causing query instance to fail - correctly

18/08/2010 stricter Queryable uniqueness:
    - uniqueness now encapsulated within new UEquationList, UEquation, UQueryList, UQuery, UQueryElement,
      UQueryExpression and UQueryValueExpression classes.
    - QueryExpression._swapVars() now returns sorted vars which...
    - QueryExpression._setMatch() equates to sorted input vars and instantiates sorted.
    - QueryValueExpression._opMatch() checked and is already sorted.
    - QueryElement._getMatch() added to sort QueryExpressions by their Qid for broader uniqueness.
       - '?' QueryExpressions get ranked last within an order QueryElement to preserve the existing
         convention although this seems to have no impact - as indeed logically it should not.
    - EquationList._getMatch() added to sort Equations by their Qid.
       - EquationList._solve() requests these unordered for inference as
         Higher order Equation order is still significant.

20/08/2010 logical ANDing of QueryExpressions and QueryValueExpressions uses pre-defined maps
    - clearer logic
    - better control over prioritising settings for each factor
    - further abstraction of factors
    - still more comprehensive and consistent
    - more efficient as maps are created once at compile time

24/08/2010:
    - Compatibility checked between rbtree/dict or srbtree/sdict.
    - Forwards compatability updates between P2.6/7 and P3
      in handling support of keys(), iteritems(), sort(), map(), itemgetter() and has_key().

25/08/2010: fix
    - Query._solve() fqcache and sqkeycache need to be keyed by qkey + querylist._getUID()
      to avoid variations of the same queries within QueryLists being wrongly cached - causing
      results to be dependent on triple/rule/query sequencing.

28/08/2010:
    - inference cache initialisation updated for efficiency and consistency:
        - sqkeycache renamed to sqcache.
        - fqk cache key renamed to qkc
    - fix bdrs metric now uses store._incMetric()
    - determination of prefered TripleStore index for a Query enhanced:
        - QueryElement._collateMatch() now identifies index types prefered for a QueryElement
        - Query._makeKey() picks the prefered index by ranks elements according to index type

30/08/2010 performance enhancements to Query._solve():
    - 2 caches for queries and rules maintained:
        - intermeadiate results/failures keyed logically+physically by (i)qkey+qid and
        - final results/failures keyed logically by (i)qkey
    - Query._solve() recursion depth tracked through Queryables and Rule _solve() methods
    - 2 progress caches maintained to record query or rule invocation recursion depth plus keys for intermeadiate results:
        - final results determined when current recursion depth returns to invocation recursion depth
          stored in the progress cache which may also be consulted for its record of intermeadiate results or failures
          which may now be removed from the caches to be replaced by the final results.

31/08/2010 performance enhancements to Query._solve():
    - optional performance caching based on a preference setting

01/09/2010 bug fix missing results in some tests:
    - Query._solve()/_makeKey() refactored to represent roles of qkeys, queries etc

02/09/2010 bug fix missing results in some tests:
    - Queryables uniqueness reworked:
        - _getUnique() manages its own caches - detecting one to use from the object being cached
        - all unique Queryables calls Queryable._getUnique(object)
        - ids counted from a seperate counter not the index length
        - QueryElement takes new force parameter to set match without collation
            - refactoring of old _forceMatch()
            - now supported by constructor

05/09/2010 bug fix missing results in some tests plus enhanced inference caching:
    - Major enhancements to Query inference caching:
        - queries: (updatable pre-emptive caching)
            - logically keyed.
            - pre-emptively cached - 1st completed results adds to cache.
            - updatable:
                - if subsequent results (from similar queries already in process) add to this the cache is updated.
                - past failed queries can switch to successful ones if they later return results.
        - rules: (recursion bound caching of finalised logical keys and intermediate physical keys)
            - logically keyed for full final rule outcomes.
            - physically keyed for intermediate rule outcomes.
            - successes cached now - rule successes apply more generally than query successes.
            - failures cached (as before)
    - substantive refactoring to clarify more complex algorithm

05/09/2010 new persistent inference caches supported.
    - initial support only to prove concept
    - does NOT yet support:
        - auto reset on triple store changes rendering caches useless              (done 06/09/2010)
        - manual reset                                                             (done 06/09/2010)
        - preference setting to turn on/off                                        (determined not needed 06/09/2010)
        - seperation of physically keyed rule outcome caches from persistent cache (done 06/09/2010)
    - updatable pre-emptive caching done incrementally as results are produced:
        - new Query._solve.cunion()
        - saves seperate union processing

06/09/2010 persistent inference caches now transaction safe:
    - seperate caches used for logical and physical infered outcomes
    - with only logically keyed caches persisting between sessions

08/09/2010 Query key handling:
    - QueryElement._collateMatch() now generates logical keys which are sensitive to inference operators

11/09/2010 Enhanced Query and FFI handling:
    - Query Keys now made according to whether Queries are exact or inferable
    - FFI index rebuild test according to preference settings
    - Query._solve():
       - submits triple queries grouped by type [exact|inferable|aggregate]
       - handles FFI based inference accordingly so can support exact queries even with FFI
       - optionally skips inference on inferable queries if full FFI index available
    - source documentation fully updated

13/09/2010 Query._solve() supports inference at individual match value granularity:
    - inference returned together with match values by TripleStore._solveTriple()
    - therefore the following inference controls no longer needed and removed:
       - by split keys - inference by grouped Queries
       - by elvals - set of exact match values for a Query
       - by seekInfered - inference by triple column
    - means simplified _collateMatch() and _matchKeys()
    - _collateMatch() tests to generate '?' inference key more sensitive to whether existing keys will match these already.

14/09/2010 QueryElement._collateMatch():
    - variable refactoring for improved clarity
    - more rigorous '?' rule key generation:
      - only if absolutely not present - improves performance
      - only if op is inferable - more robust

18/09/2010 Enhanced Nested Queries support (Queries within Queries):
    - QueryValueExpression:
      - getIsTripleID - returns True if value is the id of a nested Triple
      - getAllQueryList - returns True if all values are QueryLists
    - QueryExpression:
      - _set/_getBindings - supports storage of pre-solved bindings
      - _getAll - includes bindings
      - _modifiedClone - refactored generalised version of _changedVarsClone supports setting of one or more changed vars
      - _AND:
        - detects attempted binding of a triple id to a nested Query structure
        - in which case it pre-solves the nested Query structure
        - in an attempt to complete the binding
        - if so the bindings get fed forward to query resolution
    - QueryElement:
      - _applyVS - calls _AND with extra params needed to support nested Query evaluation
      - _collateMatch - pre-solved nested queries aren't collated
    - Query:
      - _makeKey:
        - extra params passed to applyVs for nested Query evaluation
        - pre-solved nested query bindings flipped to their logical equivalents.
      - _solve:
        - changed results uniqueness handling - more targetted.
        - failed results cache cannot be set if query has already succeeded
    - QueryList:
      - _getTIDB:
        - new method to get triple IDs for nested QueryLists.
        - handles optional external variable bindings
        - as well as internal bindings
        - automatically introduces system selection variables one for each QueryElement in each contained QueryExpression.
        - and removes the same from returned bindings once their usage is done

19/09/2010 TripleStore matchingbinding done with physical not logical solving variables:
    - logical variables are unique per collated solving QueryExpression, NOT per physical variable
    - therefore cannot be used to ensure each physical variable is uniquely and consistently unified
    - therefore:
       - Query._makeKey() simpliefied as it no longer needs to generate logical TripleStore keys
       - Query._solve():
          - invokes triple store index search TS._solveTriple() with physical key set
          - converts returned bindings to logical equivalents for consistent caching

20/09/2010: Query._makeKey() issue of interoplation error notifications now subject to new notifyInterpolationErrors pref setting

21/09/2010:
    - supports nested Queryables variable identification:
       - supports the later identification by Rule._solve() of variables deriving solely from nested Queryables
       - needed for binding and exposing externally.
       - passes these variables through to QueryList._getTIDB()
    - Optionally persistent Nested Queryables cache supported
    - key munging minimised - and new _mungeKey() exploited
    - nested queryable results aren't cached in Query._solve() as the key is not necessarilly unique to the results

22/09/2010: QueryList._getTIDB() persistent nested QueryList cache removed:
    - Won't work accross sessions unless each sets up queryables consistently - which cannot be guaranteed.
    - Reverted back to caching within the QueryList via an optional instance variable.

23/09/2010: Refactored generation of explicit logical keys associated with QueryExpressions:
    - moved from Query._makeKey.makeLVS
    - to QueryElement._collateMatch():
       - consistent ordered relationship with variable independent keys gauranteed.
       - for use within Query._makeKeys() now also returns:
           - extra bindings [True|False] found within the QueryElement (whole and inferable subset)
           - collated QueryExpressions pre-instantiated as QueryElement (whole and inferable subset)
    - Query._makeKey():
       - makeLVS() no longer needed. calling code simplified - more results returned by QueryElement._collateMatch()
       - Explicit keys unaffected by the keys for extra bindings - which are now generated afterwards

06/09/2010 Further to missing results issue:
    - QueryElement._collateMatch() cache commented out. Potential issue here as NOT queries return less results with cache supported.
    - Query:
        - _makeKey() call to collateMatch gets results in uncached format
        - _solve():
            - results cache access and initialisation changed - pre-emptive access from cache allowed unless a generic rule
            - inference cache keys by [generic|non-generic rule]*[success|failur]*[logical|physical]

12/10/2010 Stage 0. Mixed Triple ordering support. Any single order support - ensure system triples are generated in same order as user supplied triples.
    - A_TripleStore._rt() exploited
    - Query._makeKey(): attempts to build match keys predicate first for effeciency based on store/pref/default setting for this.

15/10/2010 Stage 1. Mixed triple ordering support: (triple data re-ordered, store specific search keys derived)
    - Query._makeKey():
        - search generation moved from here to Store._solveTriple() so keys may reflect specific ordering of stores queried.
        - los derivation also delayed till Store._solveTriple()
        - returns useIndex for Query._solve() to pass to Store._solveTriple() for above.
    - Query._solve():
        - passes useIndex from _makeKey() to Store._solveTriple() which:
            - tailors search keys according to individual store triple ordering
            - returns triples pre-ordered for parentStore
        - no longer needs to re-order triples from index order to data order

17/10/2010 Stage 2. Mixed triple ordering support: (mixed triple ordering in rules)
    - Queryable._expandMatch.expandMatch() elevated to Queryable._expandMatch1() so it can be exploited by new Query._expandMatch()
    - Query._expandMatch():
        - defined with optional sourceStore and targetStore paramters supporting triple re-ordering.
        - lower level expansion exploits elevated Queryable._expandMatch1()
    - Query._solve():
        - exploits Rule._rtClone() to ensure rule lhs/rhs match parentStore when merged and prepared for inference.

20/10/2010 Compliance with mtstores/mtrules refactoring

@author: Administrator
'''

from operator import itemgetter
import copy, weakref
import metabulate.utils.utils           as mtutils
import metabulate.utils.debug           as mtdebug
import metabulate.utils.errors          as mterrors
import metabulate.utils.index           as mtindex
import metabulate.singletons.singleton  as mtsingleton
import metabulate.parsers.parse         as mtparse
import metabulate.stores.structured     as mtstruct

l_ne = ['!','not','ne']
l_eq = ['=','eq']
mtconfig = mtsingleton.Settings()._getItem('config')
mtprefs  = mtsingleton.Settings()._getItem('prefs')
parser   = mtparse.Parser(filename=mtconfig._interpretItem('parserfile_name_query','eexp_test')
                         ,select=['<vop>','<var>','<val>','<sval>','<eop>','<op>','<valexp>','<triples>','<top>']
                         )                                                          # create value expression Parser object
QEfilter = mtutils._logical(mtprefs._interpretItem('Overlapping_QueryExpression_value_filter','generalise'))
QEierror = mtutils._logical(mtprefs._interpretItem('notifyInterpolationErrors','False'))
rpreds   = mtutils._stripsplit(mtprefs._interpretItem('stores_reserved_predicates','antonym_of,synonym_of'))
rpreds._union(['antonym_of,synonym_of'])
astore   = mtstruct.A_TripleStore()
qtrace   = mtindex.Index()                                                          # singelton for tracing queries orthogonally to recursion
# Note: rankop 8: regex or mixed ops; 9: wild card
rankop   = {'=':2,'!=':3,'>':4,'<':4,'>=':4,'<=':4,'~':6,'!~':7}                    # prefered match order by comperand
# get inference outcome cache behaviour
try: mtoc = int(mtprefs._interpretItem('inferenceCacheCount','3'))                  # try getting int count of inference caches to use
except ValueError: mtoc = 3                                                         # else: assume 2 (maximum)

# Logical AND meta-data
cNops = {'<=':['<','='],'>=':['>','='],'~':['=']}                                   # compatible Nops dict
qexp_AND_map =  {('equal','equal','equal'):'self'                                   # map for ANDing QueryExpressions (nop,lvals,infer):outcome
                ,('equal','equal','self'): 'self'
                ,('equal','equal','qexp'): 'qexp'
                ,('equal','self','equal'): 'self'
                ,('equal','self','qexp'):  0
                ,('equal','self','self'):  'self'
                ,('equal','qexp','equal'): 'qexp'
                ,('equal','qexp','self'):  1
                ,('equal','qexp','qexp'):  'qexp'
                ,('self','equal','equal'): 'self'
                ,('self','equal','self'):  'self'
                ,('self','equal','qexp'):  0
                ,('self','self','equal'): 'self'
                ,('self','self','self'):  'self'
                ,('self','self','qexp'):  0
                ,('qexp','equal','equal'): 'qexp'
                ,('qexp','equal','qexp'):  'qexp'
                ,('qexp','equal','qexp'):  1
                ,('qexp','qexp','equal'): 'qexp'
                ,('qexp','qexp','qexp'):  'qexp'
                ,('qexp','qexp','qexp'):  1
                ,('equal','*self','equal'): 'qexp'
                ,('equal','*self','self'): 'self'                                   # NOTE: special interpretation not 1
                ,('equal','*self','qexp'): 'qexp'
                ,('self','*self','equal'): 'qexp'
                ,('self','*self','self'): 'self'                                    # NOTE: special interpretation not 1
                ,('self','*self','qexp'): 'qexp'
                ,('qexp','*self','equal'): 'qexp'
                ,('qexp','*self','self'): 'self'                                    # NOTE: special interpretation not 1
                ,('qexp','*self','qexp'): 'qexp'
                ,('equal','*qexp','equal'): 'self'
                ,('equal','*qexp','qexp'): 'qexp'                                   # NOTE: special interpretation not 0
                ,('equal','*qexp','self'): 'self'
                ,('self','*qexp','equal'): 'self'
                ,('self','*qexp','qexp'): 'qexp'                                    # NOTE: special interpretation not 0
                ,('self','*qexp','self'): 'self'
                ,('qexp','*qexp','equal'): 'self'
                ,('qexp','*qexp','qexp'): 'qexp'                                    # NOTE: special interpretation not 0
                ,('qexp','*self','self'): 'self'
                ,('qexp','?self','self'): 1
                ,('qexp','?self','equal'): 'qexp'
                ,('self','?qexp','qexp'): 0
                ,('self','?qexp','equal'): 'self'
                }
qvexp_AND_map = {('equal','equal'): 'self'                                          # map for ANDing QueryValueExpressions
                ,('equal','self'): 'self'
                ,('equal','qexp'): 'qexp'
                ,('self','equal'): 'self'
                ,('self','self'): 'self'
                ,('self','qexp'): 0
                ,('qexp','equal'): 'qexp'
                ,('qexp','qexp'): 'qexp'
                ,('qexp','self'): 1
                ,('*self','equal'): 'qexp'
                ,('*self','self'): 'self'                                           # NOTE: special interpretation not 1
                ,('*self','qexp'): 'qexp'
                ,('*qexp','equal'): 'self'
                ,('*qexp','qexp'): 'qexp'                                           # NOTE: special interpretation not 0
                ,('*qexp','self'): 'self'
                ,('?self','equal'): 'qexp'
                ,('?self','self'): 1
                ,('?qexp','equal'): 'self'
                ,('?qexp','self'): 0
                }

def _expandVS(vs):
    evs = mtutils.sdict()
    for k in vs:
        v = []
        for qexp in vs[k]: v += [qexp._expandMatch()]
        evs[k] = v
    return evs
def _expandKeys(keys):
    eky = []
    for key in keys:
        if isinstance(key,list):
            exps = []
            for exp in key: exps += [exp._expandMatch()]
        else: exps = key
        eky += [exps]
    return eky

class SuperQueryable(object):
    _caches = {'QueryValueExpression':{}
              ,'QueryExpression':{}
              ,'QueryElement':{}
              ,'Query':{}
              ,'QueryList':{}
              ,'Equation':{}
              ,'EquationList':{}
               }
    _indexs = {'QueryValueExpression':{}
              ,'QueryExpression':{}
              ,'QueryElement':{}
              ,'Query':{}
              ,'QueryList':{}
              ,'Equation':{}
              ,'EquationList':{}
               }
    _ids = 0
    def _getUnique(i1):
        # usage:
        #    tests if the supplied object duplicates one already in the specified index
        #    if it does then the one indexed is returned and duplicate deleted
        #    otherwise:
        #        the new object is added to the index
        #        the position in this index is set as the objects Queryable id
        #        the supplied object (self) is returned
        # inputs:
        #    index - type specific index. Typiucally a dictionary which can be WeakValueDictionary
        #    i1    - new candidate instance
        # returns:
        #    i1    - unique instance which may be new or a previously instantiated duplicate
        # notes:
        #    standard flyweight pattern won't work because that assumes uniqueness can be tested before the object is instantiated.
        #    being very complex compound objects, the objects know best how to identify themselves. This means objects are
        #    first instantiated then tested for uniqueness - if a duplicate the original is used and the test discarded.
        #    While pre-instantiated flyweights are possible with __new__ they aren't compatible with copy.deepcopy().
        try:
            cache = SuperQueryable._caches[mtutils._getClass(i1)]
            key1 = i1._expandMatch(thin=True)                                       # expand Queryable
            if isinstance(i1,QueryExpression):
                keyb = i1._getBindings()
                if keyb is not None: key1 = (key1,keyb)
            key2 = mtutils._mungeKey(key1)                                          # convert into a valid key
            if key2 in cache:
                del i1                                                              #  no need to keep the duplicate Queryable
                i1 = cache[key2]                                                    #  if not unique use existing Queryable instead
            else:                                                                   # else new Queryable: (cache and id it)
                cache[key2] = i1                                                    #  add it to type specific cache
                i1._setQid(SuperQueryable._ids)                                     #  set Queryable id to type specific cache size
                SuperQueryable._ids += 1
#                if mtutils._getClass(i1) == 'Query': print ('setUnique: i1=',i1._getQid(),'key2=',key2)
        except AttributeError: pass
        return i1
    def _validateCaches(self):
        caches = SuperQueryable._caches
        mismatches = 0
        for cache in caches.values():
            for k,v in cache.items():
                if k != mtutils._mungeKey(v._expandMatch(thin=True)):
                    mismatches += 1
                    print ('changed Quearyable:',mismatches,'orig',k,'now',mtutils._mungeKey(v._expandMatch(thin=True)))
        print ('mismatches=',mismatches)
    def _showDebug(self,
                   clas='',
                   method='',
                   note='',
                   vars=[],
                   line='',
                   level=2):
        mtdebug.Debug()._notify(clas=clas,method=method,note=note,line=line,level=level,vars=vars)

class QueryKey(SuperQueryable):
    def __init__(self,match): self._update(match)
    def _update(self,match): self._setMatch(match)
    def _setMatch(self,match):
        self._showDebug(clas='QueryKey',method='_setMatch',note='inputs',line=688,level=0,vars=[['match',match]])
        self._match = match
        l = []
        for m in match:
            self._showDebug(clas='QueryKey',method='_setMatch',line=692,level=1,vars=[['m',m]])
            l1 = []
            for qve in m:
                self._showDebug(clas='QueryKey',method='_setMatch',line=695,level=1,vars=[['qve',qve]])
                s = ''
                if qve is not None:
                    lop = qve._getLop()
                    vals = qve._getVals()
                    triples = qve._getTriples()
                    valexp = qve._getValexp()
                    if lop and lop != '=': s += lop
                    if vals:
                        if len(vals) > 1: s += '"'+'"|"'.join(vals)+'"'
                        else: s += vals[0]
                    if triples:
                        for t in triples._getMatch(): s += str(t._expandMatch(thin=True))+'|'
                        s = s[:-1]
                    if valexp: s += str(valexp)
                l1 += [s]
            if len(l1) == 1: l1 = l1[0]
            l += [l1]
        self._em = tuple(l)
        self._showDebug(clas='QueryKey',method='_setMatch',line=714,level=1,vars=[['self._em',self._em]])
    def _expandMatch(self): return self._em

class Queryable(SuperQueryable):
    def __init__(self
                ,lhs=''
                ,match=[[[('*','*','*')]]]
                ,force=None
                ,rs=None
                ,rrs=None
                ,pOK=True
                ,vars=None
                ,vals=None
                ,op=None
                ,top=None
                ,vop=None
                ,eop=None
                ,sval=None
                ,triples=None
                ,bindings=None
                 ):
        self._em = mtutils.sdict()                                                  # expanded match cache
        self._default_lhs = ''
        self._update(lhs=lhs,match=match,force=force,rs=rs,rrs=rrs,pOK=pOK,vars=vars,vals=vals,op=op,top=top,vop=vop,eop=eop,sval=sval,triples=triples,bindings=bindings)
    def _update(self,lhs=None,match=None,force=None,rs=None,rrs=None,pOK=True,vars=None,vals=None,op=None,top=None,vop=None,eop=None,sval=None,triples=None,bindings=None):
        self._showDebug(clas='Queryable',method='_update',note='inputs',line=739,level=0,vars=[['match',match],['rs',rs],['rrs',rrs],['pOK',pOK]])
        if lhs   is not None: self._setLhs(lhs)
        if vars  is not None: self._setVars(vars)
        if force is not None: match = None; self._force(force)
        if match is not None: self._setMatch(match,rs=rs,rrs=rrs,pOK=pOK)
    def _setLhs(self,lhs):
        # usage:
        #    sets the templated version of lhs (if it exists)
        #    so it can be compared with match QueryLists to detect recursive clauses
        self._showDebug(clas='Queryable',method='_setLhs',note='inputs',line=748,level=0,vars=[['lhs',lhs]])
        if not lhs: self._lhs = self._default_lhs
        else: self._lhs = self._reduceVars(lhs)
        self._showDebug(clas='Queryable',method='_setLhs',note='returns',line=751,level=0,vars=[['self._lhs',self._lhs]])
        return self._lhs
    def _getLhs(self): return self._lhs
    def _reduceVars(self,clause):
        # usage:
        #    strips (an lhs) clause of all but its identifying keys
        #    reducing it to a form which allows recursive rhs clauses to be detected by matching with the lhs
        # inputs:
        #    clause - triple expressed as a tuple
        # returns:
        #    t      - if input valid: a stripped triple
        #           - else:           an empty list
        self._showDebug(clas='Queryable',method='_reduceVars',note='inputs',line=763,level=0,vars=[['clause',clause]])
        t = []
        if (isinstance(clause,list) and
            len(clause) == 1 and
            isinstance(clause[0],tuple) and
            len(clause[0]) == 3):
            for e in clause[0]:
                if (isinstance(e,list)
                and len(e) == 1): e = e[0]
                e = mtutils._stripString(e)
                if (not isinstance(e,basestring) or
                    e[0] == '?'): e = '?'
                t += [e]
            if t: t = tuple(t)
        self._showDebug(clas='Queryable',method='_reduceVars',note='returns',line=777,level=0,vars=[['t',t]])
        return t
    def _setMatch(self,match=None,rs=None,rrs=None,pOK=True,level=0):
        # sets Equations for query
        # instantiates all subclasses of Query comprising the query elements
        # autovivication supports short form query expressions for simple queries, automatically
        #    instantiating missing elements. For example submit match=('?s','*','*') which comprises
        #    just a QueryWeb, and QueryWebs, QueryEquation plus QueryEquations are also instantiated
        if match is None: match = [[[('*','*','*')]]]                               # set default match if None
        self._showDebug(clas='Queryable',method='_setMatch',note='inputs',line=786,level=0,vars=[['match',match],['rs',rs],['pOK',pOK],['level',level]])
        match1 = 0
        if isinstance(match,EquationList):                                          # default resolved match supplied
            match1 = match
        elif isinstance(match,tuple):                                               # leaf found. Instantiate QueryWeb
            match1 = Queryable._getUnique(Query(match=match,rs=rs,rrs=rrs,pOK=pOK))
        elif isinstance(match,list):                                                # still a branch
            m = mtutils.slist()
            mixedTypes = mtutils.slist()
            for m1 in match:                                                        # for each sub-branch of branch
                if isinstance(m1,basestring): m1 = m1.lower()
                if m1 in l_ne: m += [m1]
                elif m1 not in l_eq:
                    m2 = self._setMatch(match=m1
                                       ,rs=rs
                                       ,rrs=rrs
                                       ,pOK=pOK
                                       ,level=level+1
                                        )                                           #    instantiate the sub-branch
                    self._showDebug(clas='Queryable',method='_setMatch',line=805,level=2,vars=[['m1',m1],['m2',m2],['type(m2)',type(m2)]])
                    if type(m2) not in mixedTypes: mixedTypes += [type(m2)]         #    collect sub-branch types
                    if len(mixedTypes) < 2: m += [m2]                               #    if only one sub-branch type, save the sub-branch
            if len(mixedTypes) == 1:                                                # if only one sub-branch type instantiate this branch
                if isinstance(m2,Query):
                    match1 = Queryable._getUnique(QueryList(match=m,lhs=self._getLhs(),rs=rs,rrs=rrs,pOK=pOK))
                elif isinstance(m2,QueryList):
                    match1 = Queryable._getUnique(Equation(match=m,rs=rs,rrs=rrs,pOK=pOK))
                elif isinstance(m2,Equation):
                    match1 = Queryable._getUnique(EquationList(match=m,rs=rs,rrs=rrs,pOK=pOK))
            else:                                                                   # else raise inconsistent clauses exception
                self._showDebug(clas='Queryable',method='_setMatch',note='error',line=816,level=0,vars=[['match',match],['mixedTypes',mixedTypes._contents(ending='',quotes='"')]])
                raise mterrors.EquationListTypesError(mixedTypes._contents(ending='',quotes='"'))
        if match1 and not level:                                                    # if ok and top level instantiate missing parents
            m = None                                                    # if ok and top level instantiate missing parents
            if isinstance(match1,Query): m = [[[match1]]]
            elif isinstance(match1,QueryList): m = [[match1]]
            elif isinstance(match1,Equation): m = [match1]
            if m is not None: match1 = Queryable._getUnique(EquationList(match=m,pOK=pOK))
            self._match = match1
        self._showDebug(clas='Queryable',method='_setMatch',note='returns',line=825,level=0,vars=[['match1',match1]])
        return match1
    def _getMatch(self,ordered=None):
        # usage:
        #    gets matches for all Queryables where ordered is ignored
        #    that is all Queryables except Equation
        return self._match
    def _expandMatch(self,ordered=True,thin=False,sourceStore=None,targetStore=None):
        # usage:
        #    gets a match expressed in terms of Query Language Syntax
        #    expansions are cached for subsequent retrieval
        #    optionally re-orders triples from sourceStore to targetStore
        # inputs:
        #    ordered     - optional setting to validate and sort QueryLists within each Equation
        #    thin        - optional set to True to eliminate 1 string item leaf collections - for improved legability
        #    sourceStore - store originating this Queryable - for input  Query triple ordering
        #    targetStore - store exploiting this Queryable  - for output Query triple ordering
        # returns:
        #    match       - expanded match. null if invalid.
        self._showDebug(clas='Queryable',method='_expandMatch',note='inputs',line=844,level=0,vars=[['self',self],['ordered',ordered],['thin',thin]])
        if (ordered,thin,sourceStore,targetStore) in self._em:                      # if this expanded match is cached:
            match = self._em[(ordered,thin,sourceStore,targetStore)]                #  get it
        else:                                                                       # else:
            match = self._expandMatch1(self._getMatch(ordered=ordered)
                                      ,ordered
                                      ,thin
                                      ,sourceStore
                                      ,targetStore
                                       )                                            #  derive the expanded match
            self._em[(ordered,thin,sourceStore,targetStore)] = match                #  and cache it (in the expanded match cache)
        self._showDebug(clas='Queryable',method='_expandMatch',note='returns',line=855,level=0,vars=[['match',match]])
        return match
    def _expandMatch1(self,match,ordered,thin,s,t):
        # usage:
        #    common helper method for _expandMatch()
        #    supports recursive expansion of nested Queryable structures
        # inputs:
        #    match   - current Queryable structure requiring expansion.
        #    ordered - optional setting to validate and sort QueryLists within each Equation
        #    thin    - optional set to True to eliminate 1 string item leaf collections - for improved legability
        #    s       - source store originating this Queryable - for input  Query triple ordering
        #    t       - target store exploiting this Queryable  - for output Query triple ordering
        # returns:
        #    match1  - expanded match. null if invalid.
        self._showDebug(clas='Queryable',method='_expandMatch1',note='inputs',line=869,level=0,vars=[['match',match],['ordered',ordered],['thin',thin]])
        if isinstance(match,basestring): return match
        match1 = []
        for m in match:
            self._showDebug(clas='Queryable',method='_expandMatch1',line=873,level=2,vars=[['m',m]])
            if isinstance(m,list) or isinstance(m,tuple):
                match1 += [self._expandMatch1(m,ordered,thin,s,t)]
            elif not isinstance(m,basestring):
                match1 += [m._expandMatch(ordered=ordered,thin=thin,sourceStore=s,targetStore=t)]
        if (thin
        and len(match1) == 1
        and isinstance(match1[0],basestring)
            ): match1 = match1[0]
        elif isinstance(match,tuple): match1 = tuple(match1)
        self._showDebug(clas='Queryable',method='_expandMatch1',note='returns',line=883,level=0,vars=[['match1',match1]])
        return match1
    def _setQid(self,qid):
        # usage:
        #    set the Queryable ID of self (from unique index)
        # purpose:
        #    supports compact unique ref for tracking infered queries in Query._solve() to ensure these aren't repeated
        # inputs:
        #    qid - unique Queryable ID (as integer or string)
        # returns:
        #    qid - Queryable ID (as string)
        if not isinstance(qid,basestring): qid = str(qid)                           # ensure Queryable ID is a string
        self._qid = qid                                                             # instantiate as _qid instance variable
        index = SuperQueryable._indexs[mtutils._getClass(self)]
        index[qid] = self
        return qid                                                                  # and return
    def _getQid(self):
        # usage:
        #    get the Queryable ID of self
        #    from either:
        #        the _qid instance variable (if set)
        #        or if not set from the object id (non unique)
        # purpose:
        #    supports compact unique ref for tracking infered queries in Query._solve() to ensure these aren't repeated
        # inputs:
        #    index - uniqueness index for leaf object class in case self has no Queryable ID
        # returns:
        #    Queryable ID for self (as String)
        try: return self._qid                                                       # try returning the Queryable ID
        except AttributeError: return self._setQid(self)                            # except: set and return object id as its qid
    def _selectQid(self,qid):
        index = SuperQueryable._indexs[mtutils._getClass(self)]
        if qid in index: return index[qid]
        else: return None
    def _collateVars(self):
        # usage:
        #    collates all the unique variables used within a Queryable object:
        # returns:
        #    rs    - dict of unique query variable names - (as_rs = True)
        #            compatible with rs as used by Query._interpolate()
        #            ie. {qvarname1:[qvarname1], ... , qvarnameN:[qvarnameN]}
        def collateVars(match):
            self._showDebug(clas='Queryable',method='_collateVars',note='.collateVars inputs',line=925,level=0,vars=[['match',match]])
            rs = mtutils.sdict()
            for m in match:
                self._showDebug(clas='Queryable',method='_collateVars',note='.collateVars',line=928,level=1,vars=[['m',m]])
                if isinstance(m,list) or isinstance(m,tuple):
                    rs = rs._deepUnion(collateVars(m))
                else: rs = rs._deepUnion(m._collateVars())
                self._showDebug(clas='Queryable',method='_collateVars',note='.collateVars',line=932,level=1,vars=[['rs',rs]])
            self._showDebug(clas='Queryable',method='_collateVars',note='.collateVars returns',line=933,level=0,vars=[['rs',rs]])
            return rs
        self._showDebug(clas='Queryable',method='_collateVars',note='inputs',line=935,level=0,vars=[['self',self]])
        rs = collateVars(self._getMatch())
        self._showDebug(clas='Queryable',method='_collateVars',note='returns',line=937,level=0,vars=[['rs',rs]])
        return rs

class QueryValueExpression(Queryable):
    def __init__(self,op='',top='',vop='',eop='',vals='',sval='',triples=''):
        self._lop             = '='
        self._nop             = '='
        self._infer           = True
        self._lvals           = ''
        self._default_op      = ''
        self._default_top     = ''
        self._default_vop     = ''
        self._default_eop     = ''
        self._default_vals    = []
        self._default_sval    = []
        self._default_triples = ''
        self._default_valexp  = ''
        Queryable.__init__(self,op=op,top=top,vop=vop,eop=eop,vals=vals,sval=sval,triples=triples)
    def _update(self,lhs=None,match=None,force=None,rs=None,rrs=None,pOK=True,vars=None,vals=None,op=None,top=None,vop=None,eop=None,sval=None,triples=None,bindings=None):
        self._showDebug(clas='QueryValueExpression',method='_update',note='inputs',line=956,level=0,vars=[['op',op],['top',top],['vop',vop],['eop',eop]])
        self._showDebug(clas='QueryValueExpression',method='_update',note='inputs',line=957,level=0,vars=[['vals',vals],['sval',sval],['triples',triples]])
        if vals    is not None: self._setVals(vals)
        if op      is not None: self._setOp(op)
        if top     is not None: self._setTop(top)
        if vop     is not None: self._setVop(vop)
        if eop     is not None: self._setEop(eop)
        if sval    is not None: self._setSval(sval)
        if triples is not None: self._setTriples(triples,rs,rrs,pOK)
        self._generate()
    def _setOp(self,op):
        self._showDebug(clas='QueryValueExpression',method='_setOp',note='inputs',line=967,level=0,vars=[['op',op]])
        if not op: self._op = self._default_op
        elif isinstance(op,basestring):
            self._op = op
            self._setLop(op)
        self._showDebug(clas='QueryValueExpression',method='_setOp',note='returns',line=972,level=0,vars=[['self._op',self._op]])
        return self._op
    def _setTop(self,top):
        self._showDebug(clas='QueryValueExpression',method='_setTop',note='inputs',line=975,level=0,vars=[['top',top]])
        if not top: self._top = self._default_top
        elif isinstance(top,basestring):
            self._top = top
            self._setLop(top)
        self._showDebug(clas='QueryValueExpression',method='_setTop',note='returns',line=980,level=0,vars=[['self._top',self._top]])
        return self._top
    def _setVop(self,vop):
        self._showDebug(clas='QueryValueExpression',method='_setVop',note='inputs',line=983,level=0,vars=[['vop',vop]])
        if not vop: self._vop = self._default_vop
        elif isinstance(vop,basestring):
            self._vop = vop
            self._setLop(vop)
        self._showDebug(clas='QueryValueExpression',method='_setVop',note='returns',line=988,level=0,vars=[['self._vop',self._vop]])
        return self._vop
    def _setEop(self,eop):
        self._showDebug(clas='QueryValueExpression',method='_setEop',note='inputs',line=991,level=0,vars=[['eop',eop]])
        if not eop: self._eop = self._default_eop
        elif isinstance(eop,basestring):
            self._eop = eop
        self._showDebug(clas='QueryValueExpression',method='_setEop',note='returns',line=995,level=0,vars=[['self._eop',self._eop]])
        return self._eop
    def _setLop(self,lop):
        self._lop = lop
        self._setInfered(lop)
        return self._lop
    def _setInfered(self,lop):
        vals = self._getVals()
        if ((lop[0] == '=' and len(lop) > 1)
         or (lop == '!=' and '?' in vals)
            ):
            infer = False
            nop = lop[1:]
        else:
            infer = True
            nop = lop
        self._infer = infer
        self._nop = nop
        return self._infer
    def _setVals(self,vals):
        self._showDebug(clas='QueryValueExpression',method='_setVals',note='inputs',line=1015,level=0,vars=[['vals',vals]])
        if not vals: self._vals = self._default_vals
        elif isinstance(vals,list):
            vals1 = []
            for val in sorted(vals):
                if isinstance(val,basestring):
                    uribits = astore._parseURI(astore,val,mode=[])
                    if 'has_nativeuri' in uribits:
                        val1 = uribits['has_nativeuri']
                        if val1[0] == ' ' or val1[-1] == ' ': val1 = '"'+val1+'"'
                        vals1 += [val1]
            self._vals = vals1
        self._showDebug(clas='QueryValueExpression',method='_setVals',note='returns',line=1027,level=0,vars=[['self._vals',self._vals]])
        return self._vals
    def _setSval(self,sval):
        self._showDebug(clas='QueryValueExpression',method='_setSval',note='inputs',line=1030,level=0,vars=[['sval',sval]])
        if not sval: self._sval = self._default_sval
        elif isinstance(sval,list): self._sval = sval
        self._showDebug(clas='QueryValueExpression',method='_setSval',note='returns',line=1033,level=0,vars=[['self._sval',self._sval]])
        return self._vals
    def _setTriples(self,triples,rs,rrs,pOK):
        # usage:
        #    instantiates a singele QueryList representing a logical reduction of the input
        # note:
        #    Responsibility for performing this reduction is shared amongst collaborating methods.
        #    Here only the most obvious duplications are eliminated.
        # inputs:
        #    triples - list of query lists expanded and/or pre-instantiated as (Querys or QueryLists)
        #              (also accepts a single pre-instantiated QueryList on its own or as 1 item list)
        # outputs:
        #    self._triples - a single instantiated QueryList or the default value (typically a null list)
        self._showDebug(clas='QueryValueExpression',method='_setTriples',note='inputs',line=1046,level=0,vars=[['triples',triples]])
        triples1 = self._default_triples
        if isinstance(triples,Queryable): triples1 = triples
        elif isinstance(triples,list):
            if len(triples) == 1 and isinstance(triples[0],QueryList):
                triples1 = triples[0]
            else:
                qlist = []
                for ql in triples:
                    if isinstance(ql,QueryList): ql = ql._getMatch()
                    if isinstance(ql,list):
                        for q in ql:
                            if q not in qlist: qlist += [q]
                if qlist: triples1 = Queryable._getUnique(QueryList(match=qlist,rs=rs,rrs=rrs,pOK=pOK))
        self._triples = triples1
        self._showDebug(clas='QueryValueExpression',method='_setTriples',note='returns',line=1061,level=0,vars=[['self._triples',self._triples]])
        return self._triples
    def _setValexp(self):
        sval = self._getSval()
        eop  = self._getEop()
        vals = self._getVals()
        if sval and eop and vals: self._valexp = vals[0]+eop+sval[0]
        else: self._valexp = self._default_valexp
        self._showDebug(clas='QueryValueExpression',method='_setValexp',note='returns',line=1069,level=0,vars=[['self._valexp',self._valexp]])
        return self._valexp
    def _generate(self):
        lop     = self._getLop()
        vals    = self._getVals()                                                   # vals sorted by _setVals()
        triples = self._getTriples()                                                # triples as a unique QueryList (uniqueness based on ordered Queries)
        valexp  = self._setValexp()                                                 # just one
        s = ''
        isRegex = False
        vals1 = mtutils.slist()
        if valexp:
            s += str(valexp)
            vals1 += [valexp]
            isRegex = True
        else:
            if vals:
                vals1 += vals
                if len(vals) > 1: s += '|'.join(vals)
                else: s += vals[0]
                if vals[0].startswith('/') and vals[0].endswith('/'):
                    isRegex = True
            if triples:
                vals1 += [triples]
                ts = triples._getMatch()
                for t in ts: s += str(t._expandMatch(thin=True))+'|'
                s = s[:-1]
            self._lvals = vals1
        self._match = s
        if s: s = lop+s
        self._lopmatch = s
        self._isRegex = isRegex
        self._showDebug(clas='QueryValueExpression',method='_generate',note='returns',line=1100,level=0,vars=[['self._match',self._match]])
        return self._lopmatch
    def _getLop(self):
        try:    return self._lop
        except: return None
    def _getOp(self):
        try:    return self._op
        except: return None
    def _getTop(self):
        try:    return self._top
        except: return None
    def _getVop(self):
        try:    return self._vop
        except: return None
    def _getInfer(self):
        try:    return self._infer
        except: return None
    def _getNop(self):
        try:    return self._nop
        except: return None
    def _getEop(self):
        try:    return self._eop
        except: return None
    def _getVals(self):
        try:    return self._vals
        except: return []
    def _getSval(self):
        try:    return self._sval
        except: return None
    def _getValexp(self):
        try:    return self._valexp
        except: return None
    def _getTriples(self):
        try:    return self._triples
        except: return None
    def _getLvals(self):
        try:    return self._lvals                                                  # consistently ordered MatchValues
        except: return []
    def _getLopmatch(self):
        try:    return self._lopmatch                                                # consistently ordered op + MatchValues
        except: return None
    def _getIsRegex(self):
        try:    return self._isRegex
        except: return None
    def _getAllTripleID(self):
        # usage:
        #    tests whether all mastch values are triple ids
        #    caches value
        # returns:
        #    None  - if no triple ids
        #    False - if some but not all Triple ids.
        #    True  - if all are triple ids
        try:    return self._allTripleID
        except:
            lvals = self._getLvals()
            if not lvals: r = False
            else:
                r = True
                s = False
                for lval in self._getLvals():
                    if (not isinstance(lval,basestring)
                     or lval[:2] != '##'
                       ): r = False
                    else: s = True
            if r is False and s is False: r = None
            self._allTripleID = r
            return self._allTripleID
    def _getAllQueryList(self):
        try:    return self._allQueryList
        except:
            if self._getTriples() and len(self._getLvals()) == len(self._getTriples()._getMatch()): self._allQueryList = True
            else: self._allQueryList = False
            return self._allQueryList
    def _expandMatch(self,ordered=None,thin=None):
        # usage:
        #    overrides Queryable._expandMatch()
        #    as leaf Object this simply returns the match with ordered ignored
        return self._getLopmatch()

class QueryExpression(Queryable):
    def __init__(self,match=None,rs=None,rrs=None,pOK=True,vars=[],vals=[],op='',top='',vop='',eop='',sval=[],triples='',bindings=None):
        Queryable.__init__(self,match=match,rs=rs,rrs=rrs,pOK=pOK,vars=vars,vals=vals,op=op,top=top,vop=vop,eop=eop,sval=sval,triples=triples,bindings=bindings)
    def _update(self,lhs=None,match=None,force=None,rs=None,rrs=None,pOK=True,vars=None,vals=None,op=None,top=None,vop=None,eop=None,sval=None,triples=None,bindings=None):
        self._showDebug(clas='QueryExpression',method='_update',note='inputs',line=1183,level=0,vars=[['match',match],['rs',rs],['rrs',rrs],['pOK',pOK]])
        self._showDebug(clas='QueryExpression',method='_update',note='inputs',line=1184,level=0,vars=[['vars',vars],['vals',vals],['op',op]])
        if bindings is not None: self._setBindings(bindings)
        if (match is not None
         or vars or vals or sval or triples
            ):  self._setMatch(match=match,rs=rs,rrs=rrs,pOK=pOK,vars=vars,vals=vals,op=op,top=top,vop=vop,eop=eop,sval=sval,triples=triples)
        else:
            self._showDebug(clas='QueryExpression',method='_update',note='!!missing QueryValueExpression details!!',line=1190,level=1)
            pass
    def _setBindings(self,bindings):
        if isinstance(bindings,dict): self._bindings = bindings
        else: bindings = None
        return bindings
    def _getBindings(self):
        try:                   return self._bindings
        except AttributeError: return None
    def _setMatch(self,match=None,rs=None,rrs=None,pOK=True,vars=None,vals=None,op=None,top=None,vop=None,eop=None,sval=None,triples=None):
        # usage:
        #    - overrides standard version to support optional variable interpolation (based on rs)
        #      as required by Rule._mergeRhs() with variable swapping
        #    - also protects unswapped local variables from potential clashes with swapped variables
        #    - parses the query element and stores its logical components
        # inputs:
        #    match - Query match
        #    rs    - dict of existing variable names to be swapped for new variable names
        #    rrs   - dictionary of swap varnames to original varnames (reverse of rs: original_varnames keyed by swapped_varnames)
        #    pOK   - allow embedded plural QueryElements (True|False)
        # returns:
        #    match with variables swapped or not
        self._showDebug(clas='QueryExpression',method='_setMatch',note='inputs',line=1212,level=0,vars=[['match',match],['rs',rs],['rrs',rrs],['pOK',pOK]])
        self._showDebug(clas='QueryExpression',method='_setMatch',note='inputs',line=1213,level=0,vars=[['vars',vars]])
        self._showDebug(clas='QueryExpression',method='_setMatch',note='inputs',line=1214,level=0,vars=[['op',op],['top',top],['vop',vop],['eop',eop]])
        self._showDebug(clas='QueryExpression',method='_setMatch',note='inputs',line=1215,level=0,vars=[['sval',sval],['vals',vals],['triples',triples]])
        vars1 = mtutils.slist()
        if vars or vals or sval or triples:                                         # if parsed values are known:
            qve = self._setQVE(op=op,top=top,vop=vop,eop=eop
                              ,vals=vals,sval=sval,triples=triples
                              ,rs=rs,rrs=rrs,pOK=pOK
                               )                                                    #  instantiate and get the QueryValueExpression for these
            if vars:                                                                #  if query variables specified:
                vars1 = self._swapVars(vars,rs,rrs)                                 #   swap these if needed
                match = '?'+'=?'.join(vars1)+qve._getLopmatch()                     #   generate an equivalent match expression
            else: match = qve._getMatch()                                           #  else: the match expression is the QVE match
            self._showDebug(clas='QueryExpression',method='_setMatch',line=1226,level=1,vars=[['match',match]])
        elif match is not None:                                                     # else query expression syntax supplied:
            try:                                                                    #  so try parsing it:
                [m,b] = parser._parse(sentence=match)                               #   parse it using element expression parser
                self._showDebug(clas='QueryExpression',method='_setMatch',line=1230,level=1,vars=[['match',match],['b',b]])
                if '<var>'     in b: vars    = sorted(b['<var>'])                   #   bound variable list found set it
                if '<op>'      in b: op      = b['<op>'][0]
                if '<vop>'     in b: vop     = b['<vop>'][0]
                if '<top>'     in b: top     = b['<top>'][0]
                if '<eop>'     in b: eop     = b['<eop>'][0]
                if '<val>'     in b: vals    = b['<val>']
                if '<sval>'    in b: sval    = b['<sval>']
                if '<triples>' in b: triples = b['<triples>']
                self._showDebug(clas='QueryExpression',method='_setMatch',line=1239,level=1,vars=[['op',op],['top',top],['vop',vop],['eop',eop]])
                self._showDebug(clas='QueryExpression',method='_setMatch',line=1240,level=1,vars=[['vals',vals],['sval',sval],['triples',triples]])
                qve = self._setQVE(op=op                                            #   instantiate and get the QueryValueExpression
                                  ,top=top
                                  ,vop=vop
                                  ,eop=eop
                                  ,vals=vals
                                  ,sval=sval
                                  ,triples=triples
                                  ,rs=rs,rrs=rrs,pOK=pOK
                                   )
                if vars:                                                            #   if query variables present:
                    vars1 = self._swapVars(vars,rs,rrs)                             #    swap these if needed
                    if vars != vars1 or triples:                                    #    if variables changed or nested triples:
                        match = '?'+'=?'.join(vars1)+qve._getLopmatch()             #     reform the match expression (otherwise preserve original)
                elif triples: match = qve._getMatch()                               #   no vars but nested triples: also reform the match expression
            except mterrors.ParseError, X:
                X._notify(c='QueryExpression',
                          m='_setMatch()')                                          #   notify ParseErrors
                qve = self._setQVE()
        self._match = match                                                         # set match expression
        self._showDebug(clas='QueryExpression',method='_setMatch',line=1260,level=1,vars=[['vars',vars]])
        self._setVars(vars1)                                                        # set query variables
        self._showDebug(clas='QueryExpression',method='_setMatch',note='returns',line=1262,level=0,vars=[['self._match',self._match]])
        return self._match
    def _setVars(self,vars):
        if isinstance(vars,list): self._vars = sorted(vars)
        return self._vars
    def _setQVE(self,rs=None,rrs=None,pOK=None,op=None,top=None,vop=None,eop=None,vals=None,sval=None,triples=None):
        self._showDebug(clas='QueryExpression',method='_setQVE',note='inputs',line=1268,level=0,vars=[['op',op],['top',top],['vop',vop],['eop',eop]])
        self._showDebug(clas='QueryExpression',method='_setQVE',note='inputs',line=1269,level=0,vars=[['vals',vals],['sval',sval],['triples',triples]])
        self._qve = Queryable._getUnique(QueryValueExpression(op=op,top=top,vop=vop,eop=eop,vals=vals,sval=sval,triples=triples))
        self._showDebug(clas='QueryExpression',method='_setQVE',note='returns',line=1271,level=0,vars=[['self._qve._expandMatch()',self._qve._expandMatch()],['self._qve._getMatch()',self._qve._getMatch()],['self._qve',self._qve]])
        return self._qve
    def _getQVE(self):          return self._qve
    def _getEm(self):           return self._em
    def _getVars(self):         return self._vars
    def _getLop(self):          return self._getQVE()._getLop()
    def _getOp(self):           return self._getQVE()._getOp()
    def _getTop(self):          return self._getQVE()._getTop()
    def _getVop(self):          return self._getQVE()._getVop()
    def _getInfer(self):        return self._getQVE()._getInfer()
    def _getNop(self):          return self._getQVE()._getNop()
    def _getEop(self):          return self._getQVE()._getEop()
    def _getVals(self):         return self._getQVE()._getVals()
    def _getSval(self):         return self._getQVE()._getSval()
    def _getValexp(self):       return self._getQVE()._getValexp()
    def _getTriples(self):      return self._getQVE()._getTriples()
    def _getLvals(self):        return self._getQVE()._getLvals()
    def _getIsRegex(self):      return self._getQVE()._getIsRegex()
    def _getAllTripleID(self):  return self._getQVE()._getAllTripleID()
    def _getAllQueryList(self): return self._getQVE()._getAllQueryList()
    def _getAll(self):          return (self._getVars()
                                       ,self._getOp()
                                       ,self._getTop()
                                       ,self._getVop()
                                       ,self._getEop()
                                       ,self._getVals()
                                       ,self._getSval()
                                       ,self._getTriples()
                                       ,self._getInfer()
                                       ,self._getLop()
                                       ,self._getNop()
                                       ,self._getLvals()
                                       ,self._getBindings()
                                        )
    def _swapVars(self,vars,rs,rrs=None):
        # usage:
        #    recursive QueryExpression variable swapper
        # inputs:
        #    t     - current element (triple/list or element expression)
        #    rs    - dictionary of original varnames to swap varnames (swapped_varnames keyed by original_varnames)
        #    rrs   - dictionary of swap varnames to original varnames (reverse of rs: original_varnames keyed by swapped_varnames)
        # returns:
        #    vars1 - sorted swapped variables
        self._showDebug(clas='QueryExpression',method='_swapVars',note='inputs',line=1314,level=0,vars=[['vars',vars],['rs',rs],['rrs',rrs]])
        if not (rs and vars): vars1 = copy.deepcopy(vars)
        else:
            if rrs is None: rrs = rs._invert()                                      # if None rrs: get it by inverting rs
            vars1 = mtutils.slist()
            for var in vars:                                                        #   for each variable found:
                if var in rs: vars1 = vars1._union(rs[var])                         #    if variable name to be swapped:  do so
                elif var in rrs:                                                    #    elif conflicts with another swap name:
                    var1 = '!'+var                                                  #     prefix local name with ! to avoid clash
                    if var1 not in vars1:
                        vars1 += [var1]
                elif var not in vars1: vars1 += [var]
        self._showDebug(clas='QueryExpression',method='_swapVars',note='returns',line=1326,level=0,vars=[['vars1',vars1]])
        return sorted(vars1)                                                        # return the new element
    def _collateVars(self):
        # usage:
        #    overrides Queryable._collateVars()
        #    collates vars from parsed variables:
        #     - self._vars
        #     - self._triples for nested QueryList
        self._showDebug(clas='QueryExpression',method='_collateVars',note='inputs',line=1334,level=0,vars=[['self',self]])
        rs = mtutils.sdict()
        for var in self._getVars():
            if var not in rs: rs[var] = [var]
        if self._getTriples():
            r1 = self._getTriples()._collateVars()
            rs = rs._deepUnion(r1)
        self._showDebug(clas='QueryExpression',method='_collateVars',note='returns',line=1341,level=0,vars=[['rs',rs]])
        return rs
    def _modifiedClone(self,vars=None,bindings=None):
        (curr_vars,op,top,vop,eop,vals,sval,triples,infer,lop,nop,lvals,curr_bindings) = self._getAll()
        if vars     is None: vars     = curr_vars
        if bindings is None: bindings = curr_bindings
        return Queryable._getUnique(QueryExpression(vars=vars
                                                   ,op=op
                                                   ,top=top
                                                   ,vop=vop
                                                   ,eop=eop
                                                   ,vals=vals
                                                   ,sval=sval
                                                   ,triples=triples
                                                   ,bindings=bindings
                                                    ))                              # instantiate cloned QueryExpression with changed variables
    def _AND(self,qexp,store,rd,infer,rs):
        # usage:
        #    logically ANDs 2 QueryExpressions: self with qexp
        #    required to pass qexp into self
        # algorithm:
        #    specifically it logically ANDs each pair of MatchValues from self and qexp
        #    instantiating from each valid AND pair a unique QueryExpression
        #    and yield each in turn (if any)
        # note:
        #    always called where vars1 == vars2
        # inputs:
        #    qexp    - QueryExpression to unify with self
        #    store   - TripleStore used                                           if QueryExpressions need solving
        #    rd      - current Query._solve() recursion depth                     if QueryExpressions need solving
        #    infer   - Infer missing facts from rules. [None|True|False|'ffi']    if QueryExpressions need solving
        #    rs      - return substitutions dict                                  if QueryExpressions need solving
        # yields:
        #    each resulting unique unified QueryExpression
        # examples:
        #    ?v=Fred  AND ?v=!=?    -> ?v==Fred
        #    ?v!=Fred AND ?v=!=?    -> ?v=!=Fred
        #    ?v==*    AND ?v=John   -> ?v==*            SPECIAL CASE
        #    ?v=Fred  AND ?v=John   -> None
        #    ?v=Fred  AND ?v!=John  -> ?v=Fred
        #    ?v=Fred  AND ?v!=Fred  -> None
        #    ?v=Fred  AND ?v=!=John -> ?v==Fred
        #    ?v>Fred  AND ?v>=Fred  -> ?v>Fred
        #    ?v>Fred  AND ?v>John   -> ?v>John
        #    ?v<Fred  AND ?v<John   -> ?v<Fred
        #    ?v<Fred  AND ?v>John   -> None
        #    ?v~Fred  AND ?v~John   -> ?v~'Fred John'
        #    ?v!~Fred AND ?v!~John  -> ?v!~'Fred John'
        #    ?v!~Fred AND ?v~John   -> None
        #    ?v=Fred  AND ?v~John   -> ?v=Fred
        #    ?v!=Fred AND ?v~John   -> ?v~John
        #    ?v!~Fred AND ?v!=John  -> None
        #    ?v!=Fred AND ?v>Fred   -> ?v>Fred
        #    ?v!=Fred AND ?v>=Fred  -> ?v>Fred
        #    ?v!=Fred AND ?v>John   -> ?v>John
        #    ?v!=Fred AND ?v<John   -> None
        # fast track result where unification only involves the QueryExpression variable
        if qexp == self or not qexp._getLvals(): yield self
        elif not self._getLvals(): yield qexp
        # initialise data collection lists
        opl      = mtutils.slist()
        topl     = mtutils.slist()
        vopl     = mtutils.slist()
        eopl     = mtutils.slist()
        valsl    = mtutils.slist()
        svall    = mtutils.slist()
        triplesl = mtutils.slist()
        inferl   = mtutils.slist()
        lopl     = mtutils.slist()
        nopl     = mtutils.slist()
        lvalsl   = mtutils.slist()
        bindl    = mtutils.slist()
        lvs      = mtutils.slist()
        # gather data from each QueryExpression
        for c,q in enumerate([self,qexp]):
            (vars,opl[c],topl[c],vopl[c],eopl[c],valsl[c],svall[c]
            ,triplesl[c],inferl[c],lopl[c],nopl[c],lvalsl[c],bindl[c]) = q._getAll()
            lvs[c] = []
            if svall[c]: lvs[c] += [(lvalsl[c][0],(valsl[c],svall[c],triplesl[c]))]
            else:
                # also gather data from each QueryValueExpression
                if valsl[c]:
                    for lval in valsl[c]: lvs[c] += [(lval,([lval],None,None))]
                if triplesl[c]:
                    for lval in triplesl[c]._getMatch(): lvs[c] += [(lval,(None,None,[lval]))]
        # attempt to logically "AND" whole QueryExpressions first
        result = lvals = nop = inf = ''
        solve = o = None
        bindings = mtutils.sdict()
        # prepare qexp_AND_map input data
        #  - determines how nops, lvals and inf for self and qexp predispose or favour the result
        #  - this seems the be the most compact representation of the many variations involved
        if not lvalsl[1]: lvals = 'self'
        elif not lvalsl[0]: lvals = 'qexp'
        elif lvalsl[0] == lvalsl[1]: lvals = 'equal'
        elif lvalsl[0] == ['*']: lvals = '*self'
        elif lvalsl[1] == ['*']: lvals = '*qexp'
        elif lvalsl[0] == ['?'] and nopl[0] == '!=': lvals = '?self'
        elif lvalsl[1] == ['?'] and nopl[1] == '!=': lvals = '?qexp'
        elif lvalsl[0]._isSubsetOf(lvalsl[1]): lvals = 'self'
        elif lvalsl[1]._isSubsetOf(lvalsl[0]): lvals = 'qexp'
        elif (self._getAllQueryList()                                               # if solving QueryElement is all QueryList
          and rankop[nopl[0]] < 4 and rankop[nopl[1]] < 4                           #  and both solving and querying ops are equality based
          and (qexp._getAllTripleID() is not None                                   #  and either some query match values are triple ids
            or (nopl[0] != nopl[1] and not qexp._getAllTripleID())                  #      or some aren't triple ids but the ops don't match
              )
             ): solve = self._getTriples()                                          #  : unify by pre-solving the QueryList
        if nopl[0] == nopl[1]: nop = 'equal'
        elif nopl[1] in cNops and nopl[0] in cNops[nopl[1]]: nop = 'self'
        elif nopl[0] in cNops and nopl[1] in cNops[nopl[0]]: nop = 'qexp'
        elif nopl[0][0] == '!': nop = 'qexp'
        elif nopl[1][0] == '!': nop = 'self'
        if inferl[0] == inferl[1]:inf = 'equal'
        elif inferl[0]: inf = 'qexp'
        elif inferl[1]: inf = 'self'
        self._showDebug(clas='QueryExpression',method='_AND',note='summary',line=1456,level=2,vars=[['                 self',self._expandMatch()]])
        self._showDebug(clas='QueryExpression',method='_AND',note='summary',line=1457,level=2,vars=[['                 qexp',qexp._expandMatch()]])
        self._showDebug(clas='QueryExpression',method='_AND',note='summary',line=1458,level=2,vars=[['  self isAllQueryList',self._getAllQueryList()]])
        self._showDebug(clas='QueryExpression',method='_AND',note='summary',line=1459,level=2,vars=[['  qexp  isAllTripleID',qexp._getAllTripleID()]])
        self._showDebug(clas='QueryExpression',method='_AND',note='summary',line=1460,level=2,vars=[['(nop,lvals,inf) map',(nop,lvals,inf)]])
        # if something needs solving inorder to bind
        if solve:                                                                   # if solve to bind:
            tidb = solve._getTIDB(store,rd=rd,infer=infer,vars=vars,rs=rs)          #  solve it to get its triple id bindings
            if nopl[0] == nopl[1]:                                                  #  if ops equal: (match intersection)
                valsl[1] = mtutils.slist()                                          #   prepare to construct new match values list
                for lval in lvalsl[1]:                                              #   construct new match values from querying match
                    if lval in tidb:                                                #    if in solving match:
                        bindings[lval] = tidb[lval]                                 #     match bindings
                        valsl += [lval]                                             #     match values
            elif nopl[1] == '!=':                                                   #  elif only querying !=: (subtract these from solving)
                bindings = copy.deepcopy(tidb)                                      #    start with solving bindings
                if qexp._getAllTripleID() is not None:                              #   if any are triple ids: (filter the solving match)
                    for lval in lvalsl[1]:                                          #    filter matching values
                        if lval in tidb: del bindings[lval]                         #     from solving bindings
                valsl[1] = mtutils.slist([lval for lval in bindings])               #   construct values from bindings
                opl[1] = '='                                                        #   make query '=' the new match list
            elif nopl[0] == '!=':                                                   #  elif only solving !=: (subtract these from querying)
                bindings = copy.deepcopy(tidb)                                      #   start with solving bindings
                if qexp._getAllTripleID() is not None:                              #   if any are triple ids: (filter the querying match)
                    valsl[1] = mtutils.slist()                                      #    prepare to construct new match values list
                    for lval in lvalsl[1]:                                          #    from querying match
                        if lval not in tidb: valsl[1] += [lval]                     #     filtering matching values
                        else: del bindings[lval]                                    #     and bindings
        # consult qexp_AND_map
        if bindings:                                                                # if bindings (from nested Queryable):
            if inf == 'self': o = 1                                                 #  if only qexp is inferable: flag to make it exact
        else:                                                                       # else no bindings: (so consult actions map)
            key = (nop,lvals,inf)                                                   #  make map key
            if key in qexp_AND_map: result = qexp_AND_map[key]                      #  if key in map: get result
            if result == 'self': yield self                                         #  if result is self: yield it
            elif result == 'qexp': yield qexp                                       #  elif result is qexp: yield it
            elif result: o = result                                                 #  elif something has to be made non-inferable: flag what
        if o is not None:                                                           # if something has to be made non-inferable
            # make non-inferable and yield
            if opl[o]:  opl[o]  = '='+opl[o]                                        #  flip comperands to non-inferable equivalent
            if vopl[o]: vopl[o] = '='+vopl[o]
            if topl[o]: topl[o] = '='+topl[o]
            if not (opl[o] or vopl[o] or topl[o]) and lopl[o]: opl[o] = '='+lopl[o] #  catch-all if no explicit comperand set
            if valsl[o] and '?' in valsl[o] and lopl[o][-1] == '=':                 #  qexp cannot match anything equating to '?':
                valsl[o] = valsl[o].remove('?')                                     #   if present remove it
        elif bindings: o = 1                                                        # elif no inference but a bindings change on qexp: flag it
        # something changed to yield? - reinstantiate with changes and yield
        if o is not None:                                                           # if somethings has changed: re-instantiate the change
            if not bindings: bindings = bindl[o]
            yield Queryable._getUnique(QueryExpression(vars    =vars
                                                      ,op      =opl[o]
                                                      ,top     =topl[o]
                                                      ,vop     =vopl[o]
                                                      ,eop     =eopl[o]
                                                      ,vals    =valsl[o]
                                                      ,sval    =svall[o]
                                                      ,triples =triplesl[o]
                                                      ,bindings=bindings
                                                       ))                           # instantiate changed QueryExpression for yielding
        else:
            # proceed to AND each pair of QueryValueExpressions individually
            op1 = opl[0]; top1 = topl[0]; vop1 = vopl[0]; eop1 = eopl[0]; infer1 = inferl[0]; lop1 = lopl[0]; nop1 = nopl[0]
            op2 = opl[1]; top2 = topl[1]; vop2 = vopl[1]; eop2 = eopl[1]; infer2 = inferl[1]; lop2 = lopl[1]; nop2 = nopl[1]
            for (lval1,(val1,sval1,triple1)) in lvs[0]:
                for (lval2,(val2,sval2,triple2)) in lvs[1]:
                    # prepare qvexp_AND_map input data
                    if lval1 == '*': qve = '*self'
                    elif lval2 == '*': qve = '*qexp'
                    elif lval1 and not lval2: qve = 'self'
                    elif lval2 and not lval1: qve = 'qexp'
                    elif lval1 == '?' and nop1 == '!=': qve = '?self'
                    elif lval2 == '?' and nop2 == '!=': qve = '?qexp'
                    elif lval1 == lval2:
                        if nop1 == nop2: qve = 'equal'
                        elif nop2 in cNops and nop1 in cNops[nop2]: qve = 'self'
                        elif nop1 in cNops and nop2 in cNops[nop1]: qve = 'qexp'
                        elif ((nop1 == '>=' and nop2 == '<=')
                           or (nop1 == '<=' and nop2 == '>=')
                              ): qve = 'self'; op1 = '='
                        else: continue
                    elif nop1 == nop2: continue
                    elif nop1[0] == '!' and nop1[-1] == nop2[-1]: qve = 'qexp'
                    elif nop2[0] == '!' and nop1[-1] == nop2[-1]: qve = 'self'
                    elif nop1 == '!=' and nop2 == '>' or nop2 == '<': qve = 'qexp'
                    elif nop2 == '!=' and nop1 == '>' or nop1 == '<': qve = 'self'
                    elif nop1 == '>' and lval2 > lval1 and (nop2 == '=' or nop2 == '>='): qve = 'qexp'
                    elif nop1 == '<' and lval2 < lval1 and (nop2 == '=' or nop2 == '<='): qve = 'qexp'
                    elif nop2 == '>' and lval1 > lval2 and (nop1 == '=' or nop1 == '>='): qve = 'self'
                    elif nop2 == '<' and lval1 < lval2 and (nop1 == '=' or nop1 == '<='): qve = 'self'
                    else: continue
                    # consult qvexp_AND_map
                    result = ''                                                     # assume no result in map
                    key = (qve,inf)                                                 # make map key
                    if key in qvexp_AND_map: result = qvexp_AND_map[key]            # if key in map: get result
                    if result == 'self' or 0:                                       # if result is self: prepare to yield it
                        lop = lop1; op = op1; top = top1; vop = vop1; eop = eop1; val = val1; sval = sval1; triple = triple1
                    elif result == 'qexp' or 1:                                     # elif result is qexp: prepare to yield it
                        lop = lop2; op = op2; top = top2; vop = vop2; eop = eop2; val = val2; sval = sval2; triple = triple2
                    else: continue                                                  # else no result in map: skip to next QVE pair
                    if result == 0 or result == 1:                                  # if non-inferable result: make it so
                        if op:    op  = '='+op                                      #  flip comperands to non-inferable equivalent
                        elif vop: vop = '='+vop
                        elif top: top = '='+top
                        if not (op or vop or top) and lop: op = '='+lop             #  catch-all if no explicit comperand set
                    yield Queryable._getUnique(QueryExpression(vars   =vars
                                                              ,op     =op
                                                              ,top    =top
                                                              ,vop    =vop
                                                              ,eop    =eop
                                                              ,vals   =[val]
                                                              ,sval   =sval
                                                              ,triples=[triple]))   # yield result instantiated as a QueryExpression

wkqe = Queryable._getUnique(QueryExpression(vals=['*']))                            # instantiate common wild key QueryExpression
rkqe = Queryable._getUnique(QueryExpression(vals=['?']))                            # instantiate common rule key QueryExpression
rkqe._setQid('zzzzzzz')                                                             # sort '?' in QueryElements last (to preserve
                                                                                    #  existing algorithmic convention although tests
                                                                                    #  to date indicate ordering has no effect whatsoever
                                                                                    #  on results or metrics - which is reassuring)
class QueryElement(Queryable):
    def __init__(self,match=None,force=None,rs=None,rrs=None,pOK=True):
        self._showDebug(clas='QueryElement',method='__init__',note='inputs',line=1577,level=0,vars=[['match',match],['force',force],['rs',rs],['rrs',rrs],['pOK',pOK]])
        Queryable.__init__(self,match=match,force=force,rs=rs,rrs=rrs,pOK=pOK)
    def _force(self,match):
        if not isinstance(match,list): match = [match]
        match1 = mtutils.slist()
        for m in match:
            if isinstance(m,Queryable): match1 += [m]
        self._match = match1
        return self._match
    def _setMatch(self,match=None,rs=None,rrs=None,pOK=True):
        # usage:
        #    sets match as list of locally unique QueryExpressions it comprises
        #    resolves nested lists by extracting QueryExpressions from list leaves
        #    collates Queries into QueryLists
        # inputs:
        #    match - QueryElement as a list (or nested lists) of QueryExpressions and Query's
        #    rs    - dict of existing variable names to be swapped for new variable names
        #    rrs   - dictionary of swap varnames to original varnames (reverse of rs: original_varnames keyed by swapped_varnames)
        #    pOK   - allow plural QueryElements (True|False)
        # returns:
        #    match as list of locally unique QueryExpressions each with variables swapped or not
        def setMatch(match,rs,rrs,pOK):
            # usage:
            #    nested function to recursively instantiate unique QueryExpressions from supplied match list
            #    also collates a list of unique nested Query's
            # returns:
            #    list of unique instantiated QueryExpressions
            #    list of unique instantiated nested Queries
            self._showDebug(clas='QueryElement',method='_setMatch',note='.setMatch inputs',line=1605,level=0,vars=[['match',match],['rs',rs],['rrs',rrs],['pOK',pOK]])
            if not isinstance(match,list): match = [match]
            match = mtutils.slist(match)._peel(0)                                   # peel away superfuous nested lists
            self._showDebug(clas='QueryElement',method='_setMatch',note='.setMatch',line=1608,level=1,vars=[['match',match]])
            match1 = mtutils.slist()                                                # initialise list for unique QueryExpressions
            qlist = mtutils.slist()                                                 # initialise list for unique Query's
            for m in match:                                                         # for each QueryElement item:
                self._showDebug(clas='QueryElement',method='_setMatch',note='.setMatch',line=1612,level=2,vars=[['m',m]])
                q1 = m1 = None                                                      #  initialise this Query and QueryExpression to None
                if isinstance(m,list): m1,q1 = setMatch(m,rs,rrs,pOK)               #  if item is a nested list gets its
                elif isinstance(m,tuple):                                           #  elif item is a tuple:
                    q1 = [Queryable._getUnique(Query(match=m
                                                    ,rs=rs
                                                    ,rrs=rrs
                                                    ,pOK=pOK
                                                     ))]                            #   instantiate tuple as Query with a list
                else:                                                               #  else: (its a QueryExpression)
                    if isinstance(m,QueryExpression): m1 = [m]
                    else:
                        m1 = [Queryable._getUnique(QueryExpression(match=m
                                                                  ,rs=rs
                                                                  ,rrs=rrs
                                                                  ,pOK=pOK
                                                                   ))]              #   instantiate as candidate QueryExpression
                if m1: match1 = match1._union(m1)                                   #  if QE list: union with collated QueryExpressions
                if q1: qlist = qlist._union(q1)                                     #  if Query list: union with collated Query's
            return match1,qlist                                                     # return lists of collated QueryExpressions and Query's
        ## End setMatch()
        self._showDebug(clas='QueryElement',method='_setMatch',note='inputs',line=1633,level=0,vars=[['match',match],['rs',rs],['rrs',rrs],['pOK',pOK]])
        if match is None: match = '*'                                               # set default match if None
        if rs and rrs is None: rrs = rs._invert()                                   # prepare rrs if needed
        self._showDebug(clas='QueryElement',method='_setMatch',line=1636,level=1,vars=[['match',match],['rrs',rrs]])
        match1,qlist = setMatch(match,rs,rrs,pOK)                                   # get list of (unique) QueryExpressions, QueryList (if any) from match
        self._showDebug(clas='QueryElement',method='_setMatch',line=1638,level=1,vars=[['match1',match1],['qlist',qlist]])
        self._match = self._collateMatch(match1,qlist)                              # collate any QueryExpressions
        self._showDebug(clas='QueryElement',method='_setMatch',note='returns',line=1640,level=0,vars=[['self._match',self._match]])
        return self._match                                                          # and return set match
    def _getMatch(self,ordered=True):
        # usage:
        #    retrieves list of QueryExpressions objects forming the QueryElement
        #    optional ordering (by default) ensures expanded QueryExpressions can be compared
        ordered = mtutils._logical(ordered)
        self._showDebug(clas='QueryElement',method='_getMatch',note='inputs',line=1647,level=0,vars=[['self',self],['ordered',ordered]])
        match = self._match
        if ordered:
            self._showDebug(clas='QueryElement',method='_getMatch',line=1650,note='1)',level=1,vars=[['match',match]])
            match1 = []
            for m in match:
                self._showDebug(clas='QueryElement',method='_getMatch',line=1653,level=0,vars=[['m',m]])
                match1 += [[m,m._getQid()]]
            self._showDebug(clas='QueryElement',method='_getMatch',line=1655,note='2)',level=1,vars=[['match1',match1]])
            match1.sort(key=itemgetter(1))
            self._showDebug(clas='QueryElement',method='_getMatch',line=1657,note='3)',level=1,vars=[['match1',match1]])
            match = mtutils.slist(map(itemgetter(0),match1))
        self._showDebug(clas='QueryElement',method='_getMatch',line=1659,note='returns',level=0,vars=[['match',match]])
        return match
    def _getVars(self):
        vars = mtutils.slist()
        for e in self._getMatch(): vars = vars._union(e._getVars())
        self._showDebug(clas='QueryElement',method='_getVars',note='returns',line=1664,level=0,vars=[['vars',vars]])
        return vars
    def _applyVS(self,vs,rs,store,rd,infer):
        # usage:
        #    applies forward fed QueryExpressions from variable substituions list (vs)
        #    to the QueryExpressions in self (this QueryElement)
        #    and returns potentially a new QueryElement comprising the resulting unified QueryExpressions
        # algorithm:
        #    for each QueryVariable:
        #     each QueryExpression in self is logically ANDed with each QueryExpression in vs
        # inputs:
        #    vs      - value substitution dict   (for passing querying QueryExpressions to solving QueryExpressions)
        #    rs      - return substitutions dict                                  if QueryExpressions need solving
        #    store   - TripleStore used                                           if QueryExpressions need solving
        #    rd      - current Query._solve() recursion depth                     if QueryExpressions need solving
        #    infer   - Infer missing facts from rules. [None|True|False|'ffi']    if QueryExpressions need solving
        # returns:
        #    elm1  - QueryElement comprising unified QueryExpressions
        self._showDebug(clas='QueryElement',method='_applyVS',note='inputs',line=1682,level=0,vars=[['self._expandMatch()',self._expandMatch()],['self',self]])
        self._showDebug(clas='QueryElement',method='_applyVS',note='inputs',line=1683,level=0,vars=[['_expandVS(vs)',_expandVS(vs)],['vs',vs]])
        exps = self._getMatch()                                                     # prepare to extract all variable substitutions
        exps1 = mtutils.slist()                                                     # matching variables in this QueryElement
        d_exps = []                                                                 # FOR DEBUG prepare expanded self
        d_vs_exps = []                                                              # FOR DEBUG prepare expanded input
        d_exps1 = []                                                                # FOR DEBUG prepare expanded result
        ANDed = False                                                               # flag if logical ANDing is attempted
        self._showDebug(clas='QueryElement',method='_applyVS',line=1690,level=1,vars=[['exps',exps]])
        for exp in exps:                                                            # so for each QueryExpression in this QueryElement:
            vars = exp._getVars()                                                   #  get the QueryExpression variables
            d_exp = exp._expandMatch()                                              #  FOR DEBUG expand QueryExpression
            d_exps += [d_exp]                                                       #  FOR DEBUG expanded self
            self._showDebug(clas='QueryElement',method='_applyVS',line=1695,level=1,vars=[['d_exp',d_exp],['vars',vars]])
            for var in vars:                                                        #  for each variable:
                if '?'+var in vs:                                                   #   if used by the input:
                    vs_exps = vs['?'+var]                                           #    get the matching input QueryExpressions
                    self._showDebug(clas='QueryElement',method='_applyVS',line=1699,level=2,vars=[['vs_exps',vs_exps]])
                    for vs_exp in vs_exps:                                          #    for each input QueryExpression
                        d_vs_exp = vs_exp._expandMatch()                            #     FOR DEBUG expand input QueryExpression
                        d_vs_exps += [d_vs_exp]                                     #     FOR DEBUG expanded input
                        self._showDebug(clas='QueryElement',method='_applyVS',line=1703,level=2,vars=[['d_vs_exp',d_vs_exp],['vs_exp._getVars()',vs_exp._getVars()]])
                        ANDed = True                                                #     logical ANDing attempted
                        for exp1 in exp._AND(vs_exp,store,rd,infer,rs):                #     get each logically ANDed with QueryExpression in self
                            if exp1 not in exps1:                                   #     if ANDed QueryExpression is unique
                                exps1 += [exp1]                                     #      collate it
                                d_exp1 = exp1._expandMatch()                        #      FOR DEBUG expand ANDed QueryExpression
                                d_exps1 += [d_exp1]                                 #      FOR DEBUG expanded result
                                self._showDebug(clas='QueryElement',method='_applyVS',line=1710,level=2,vars=[['d_exp1',d_exp1]])
        self._showDebug(clas='QueryElement',method='_applyVS',note='.applyVS',line=1711,level=1,vars=[['exps1',exps1]])
        if (not ANDed                                                               # if nothing to AND/unify
         or exps1 == exps                                                           #  or these equal to self QueryExpressions
         or len(exps1._intersection(exps)) == len(exps)                             #  or these equivalent of self QueryExpressions
            ):                                                                      #  ; (result is self)
            elm1 = copy.deepcopy(self)                                              #  prepare to return copy of self
            d_exps1 = d_exps                                                        #  FOR DEBUG expanded result is expanded self
        elif not exps1:                                                             # elif ANDing failed:
            raise mterrors.QueryElementInterpolationError(d_vs_exps,d_exps)         #  raise interpolating error
        else:                                                                       # else: (instantiate as a new temporary QueryElement)
            elm1 = Queryable._getUnique(QueryElement(force=exps1))                  #  instantiate exps1 as Unique QueryElement
        self._showDebug(clas='QueryElement',method='_applyVS',note='summary',line=1722,level=1,vars=[['self',d_exps],['AND',d_vs_exps],['=>',d_exps1]])
        self._showDebug(clas='QueryElement',method='_applyVS',note='returns',line=1723,level=0,vars=[['elm1._expandMatch()',elm1._expandMatch()],['elm1',elm1]])
        return elm1
    def _collateMatch(self,match,qlist,rpfound=None,infer=None,isInfered=None,lv0c=None,lvs0=None):
        # usage:
        #    collates and instantiates QueryElement match
        #    three step collation of QueryExpressions comprising this QueryElement:
        #    1) collates query variables for query value, query op pairs - to eliminate duplicate searches for different variables
        #    2) collates query values for query variables (collated in 1), query op pairs - for gen/specialisation filter tests
        #    3) filters QueryExpressions logically contained within others also mindfull of gen/specialisation filter preferences
        # inputs:
        #    match        - QueryElement._getMatch() or list of QueryExpressions
        #    qlist        - QueryList or list of unique Query's (as distinct from Query Expressions)
        #    rpfound      - reserved predicate found flag. Set to 'find' for predicate QueryElement
        #                    also indicates if collating an interpolated match (ie. when rpfound is not None)
        #    infer        - inference on (True|False|None|'ffi'). If on then if rpfound not None prepare to insert rule keys
        #    isInfered    - is this a request to collate exclusively inferrable QueryExpressions [Ture|False]
        #    lv0c         - logical variable counter
        #    lvs0         - dict of physical variables indexed by logical ones
        # returns: (selection of)
        #    match        - updated QueryElement expressed as its match - ie a list of QueryExpressions
        #    qelms        - updated QueryElement expressed as an instantiated unique QueryElement
        #    iqelms       - updated inferable QueryElement (see note) expressed as an instantiated unique QueryElement
        #    luqves       - updated list of locally unique collated QueryValueExpressions
        #    iluqves      - updated list of inferable locally unique collated QueryValueExpressions (see note)
        #    rpfound      - updated reserved predicate found flag. Set to 'find' for predicate QueryElement
        #    useIndex     - updated use Index flag [True|False] - True if the value can be found using the TripleStore indexes
        #    rkneeded     - rule key needed for this QueryElement [True|False]
        #    lv0c         - updated logical variable counter
        #    lvs0         - updated dict of physical variables indexed by logical ones
        #    xb           - QueryElement contains extra (pre-solved) bindings [True|False]
        #    ixb          - inferable QueryElement contains extra (pre-solved) bindings [True|False]
        # note:
        #    "inferable" refers to QueryExpressions whose matches may be infered from rules
        def updateLVS(vars,lv0c,lvs0):
            lv0c += 1                                                               #  get next logical variable id
            lv0 = '!'+str(lv0c)                                                     #  get the logical variable name
            lvs0[lv0] = vars                                                        #  index logical to physical variables
            return lv0c,lvs0
        def filterVals(vals):
            self._showDebug(clas='QueryElement',method='_collateMatch',note='.filterVals inputs',line=1762,level=0,vars=[['vals',vals],['QEfilter',QEfilter]])
            if (QEfilter is not None
            and len(vals) > 1
            and '*' in vals
                ):
                if QEfilter == 'generalise': vals = ['*']
                else: vals.remove('*')
            self._showDebug(clas='QueryElement',method='_collateMatch',note='.filterVals returns',line=1769,level=0,vars=[['vals',vals]])
            return mtutils.slist(vals)
        ## End filterVals()
        def finaliseMatch(match,luqves,rkfound,useIndex,lv0c,lvs0
                         ,vars=[],op=None,vals=None,valexps=None
                         ,unboundvars=None,unboundvals=None,unboundvalexps=None,solvedexp=None
                         ):
            # usage:
            #    finalise the following lists:
            #    1) unique QueryExpressions
            #    2) unique QueryValueExpressions (if list was supplied)
            # inputs:
            #    match          - current list of collated QueryExpressions
            #    luqves         - list of locally unique QueryValueExpressions (if list is supplied, or None if not)
            #    rkfound        - rule key found flag
            #    useIndex       - use Index flag [True|False] - True if the value can be found using the TripleStore indexes
            #    lv0c           - logical variable counter [None|int]
            #    lvs0           - dict of physical variables indexed by logical ones
            #    op             - op for bound QueryValueExpression
            #    vars           - list of query variables for bound QueryValueExpression
            #    vals           - list of query values for bound QueryValueExpression
            #    unboundvars    - list of unbound vars for QueryExpression (as an alternative to vars,vals and op)
            #    unboundvals    - list of unbound vals for QueryValueExpression (as an alternative to vars,vals and op)
            #    unboundvalexps - list of unbound valexps for QueryValueExpression (as an alternative to vars,vals and op)
            #    solvedexp      - QueryExpression with bindings already set
            # returns:
            #    match          - updated list of collated QueryExpressions
            #    luqves         - updated list of locally unique collated QueryValueExpressions
            #    rkfound        - updated rule key found flag
            #    useIndex       - updated use Index flag [True|False] - True if the value can be found using the TripleStore indexes
            #    lv0c           - updated logical variable counter [None|int]
            #    lvs0           - updated dict of physical variables indexed by logical ones
            self._showDebug(clas='QueryElement',method='_collateMatch',note='.finaliseMatch inputs',line=1801,level=0,vars=[['match',match]])
            self._showDebug(clas='QueryElement',method='_collateMatch',note='.finaliseMatch inputs',line=1802,level=0,vars=[['luqves',luqves]])
            self._showDebug(clas='QueryElement',method='_collateMatch',note='.finaliseMatch inputs',line=1803,level=0,vars=[['rkfound',rkfound],['useIndex',useIndex]])
            self._showDebug(clas='QueryElement',method='_collateMatch',note='.finaliseMatch inputs',line=1804,level=0,vars=[['op',op],['vars',vars],['vals',vals]])
            self._showDebug(clas='QueryElement',method='_collateMatch',note='.finaliseMatch inputs',line=1805,level=0,vars=[['unboundvars',unboundvars],['unboundvals',unboundvals],['unboundvalexps',unboundvalexps]])
            if unboundvars    is not None: vars    = unboundvars
            if unboundvals    is not None: vals    = unboundvals
            if unboundvalexps is not None: valexps = unboundvalexps
            if op and op[0] == '=' and len(op) > 1: opinfer = False                 # if op and exact prefixed: this op isn't inferable
            else: opinfer = True                                                    # else: op is inferable
            top = vop = eop = ''
            vals1   = mtutils.slist()
            sval    = mtutils.slist()
            triples = mtutils.slist()
            if valexps is not None:
                sval[0]  = valexps[0]
                eop      = valexps[1]
                vals1[0] = valexps[2]
                vop      = op
            elif vals:
                for val in vals:
                    if isinstance(val,Query) or isinstance(val,QueryList):
                        triples += [val]
                    else: vals1 += [val]
                if triples: top = op
            self._showDebug(clas='QueryElement',method='_collateMatch',note='.finaliseMatch',line=1826,level=1,vars=[['op',op],['top',top],['vop',vop],['eop',eop]])
            self._showDebug(clas='QueryElement',method='_collateMatch',note='.finaliseMatch',line=1827,level=1,vars=[['vals',vals],['sval',sval],['triples',triples]])
            if useIndex and useIndex < 9:                                           # if wild or rule search not already detected:
                if not vals or '*' in vals:                                         #  if implicit or explicit wild card search:
                     useIndex = 9                                                   #   set lowest priority index (reserved for wild cards)
                     if opinfer: rkfound = True                                     #   if inferable: indicate (implicit) rule key found
                elif not rkfound and '?' in vals and opinfer: rkfound = True        #  elif flag explicit rule key found for 1st time: flag it
            self._showDebug(clas='QueryElement',method='_collateMatch',note='.finaliseMatch',line=1833,level=1,vars=[['vars',vars],['unboundvars',unboundvars],['vals',vals],['unboundvals',unboundvals],['useIndex',useIndex]])
            # finalise QueryExpression instantiation and listing of unique QueryExpressions
            self._showDebug(clas='QueryElement',method='_collateMatch',note='.finaliseMatch',line=1835,level=1,vars=[['op',op],['top',top],['vop',vop],['eop',eop]])
            self._showDebug(clas='QueryElement',method='_collateMatch',note='.finaliseMatch',line=1836,level=1,vars=[['vars',vars],['vals',vals],['sval',sval],['triples',triples]])
            if solvedexp: exp = solvedexp
            else:                                                                   # instantiate candidate fanalised QueryExpression
                exp = Queryable._getUnique(QueryExpression(vars=vars,op=op,top=top,vop=vop,eop=eop,vals=vals1,sval=sval,triples=triples))
            if exp not in match:
                match += [exp]                                                      # if new to QueryElement add it
                if lv0c is not None: lv0c,lvs0 = updateLVS(vars,lv0c,lvs0)          # if updating logical variable keys: do so
                # processing unique to interpolated queries (ie. where uqves is not None)
                if luqves is not None:
                    # check to update unique QueryValueExpressions list
#                    if vals1 or sval or triples:
                    qve = Queryable._getUnique(QueryValueExpression(op=op,top=top,vop=vop,eop=eop,vals=vals1,sval=sval,triples=triples))
#                    else: qve = None
                    luqves += [qve]
                    self._showDebug(clas='QueryElement',method='_collateMatch',note='.finaliseMatch',line=1850,level=1,vars=[['luqves',luqves]])
                    self._showDebug(clas='QueryElement',method='_collateMatch',note='.finaliseMatch',line=1851,level=2,vars=[['rkfound',rkfound]])
            self._showDebug(clas='QueryElement',method='_collateMatch',note='.finaliseMatch',line=1852,level=1,vars=[['exp._expandMatch()',exp._expandMatch()],['exp',exp]])
            self._showDebug(clas='QueryElement',method='_collateMatch',note='.finaliseMatch returns',line=1853,level=0,vars=[['match',match],['rkfound',rkfound],['useIndex',useIndex]])
            self._showDebug(clas='QueryElement',method='_collateMatch',note='.finaliseMatch returns',line=1854,level=0,vars=[['luqves',luqves]])
            return match,luqves,rkfound,useIndex,lv0c,lvs0
        ## End finaliseMatch()
        self._showDebug(clas='QueryElement',method='_collateMatch',note='inputs',line=1857,level=0,vars=[['match',match],['qlist',qlist]])
        self._showDebug(clas='QueryElement',method='_collateMatch',note='inputs',line=1858,level=0,vars=[['rpfound',rpfound],['infer',infer]])
        if infer: rkneeded = True                                                   # initialise rule key needed
        else: rkneeded = False                                                      #  to boolean of Query infer
        imatch = mtutils.slist()                                                    # prepare inferable match list
        iqelms = None
        ixb = xb = False
        if rpfound is None:                                                         # if not interpolated
            if len(match)+len(qlist) == 1:                                          #  check to skip collation (if only one item):
                if match:                                                           #   if that item is in match: return it
                    self._showDebug(clas='QueryElement',method='_collateMatch',note='returns',line=1867,level=0,vars=[['match',match]])
                    return match
                elif isinstance(qlist[0],QueryList):                                #   else if its a QueryList: return it
                    self._showDebug(clas='QueryElement',method='_collateMatch',note='returns',line=1870,level=0,vars=[['qlist',qlist]])
                    return qlist
            rkfound = None
            luqves = None                                                           #  otherwise flag rule_key_found & local_unique_qves as None
        else:                                                                       # else: (its interpolated)
            rkfound = False                                                         #  and rule_key_found as False
            luqves = mtutils.slist()                                                #  initialise local unique QueryValueExpressions
            iluqves = mtutils.slist()
            # get the isInfered imatch and iluqves - these versions based on collated match of inferable QueryExpressions
            # plus:
            #    1. get the values of exclusively exact QueryValueExpression (elvals)
            #    2. test all infered logical values with lop '=' for:
            #        - setting rpfound reserved predicate found = True
            #        - setting rkneeded = False if only reserved predicates found among inferable values
            if not isInfered:                                                       #  if new full collation (not the inferable subset):
                ilvals  = mtutils.slist()                                           #   initialise list of all infered logical values
                ilvalse = mtutils.slist()                                           #   initialise list of all infered logical values with lop '='
                # build ilvals, ilvalse and elvals:
                #  1st from QueryList if input
                if qlist and isinstance(qlist,list):                                #   if current QEXP is an uninstantiated QueryList
                    iqlist = Queryable._getUnique(QueryList(match=qlist))           #    instantiate it
                else: iqlist = copy.deepcopy(qlist)                                 #   else: copy the instantiation
                if iqlist:                                                          #   if intermedeate QueryList just instantiated/copied:
                    ilvals  += [iqlist]                                             #    append it to list of all infered logical values, and
                    ilvalse += [iqlist]                                             #    append it to list of all infered logical values with lop '='
                #  2nd from match if input
                for m in match:                                                     #   foreach QueryExpression: seperate exact and inferable
                    self._showDebug(clas='QueryElement',method='_collateMatch',line=1897,level=2,vars=[['m._expandMatch()',m._expandMatch()],['m._getInfer()',m._getInfer()],['m._getLvals()',m._getLvals()],['m._getLop()',m._getLop()]])
                    if m._getInfer():                                               #    if inferable:
                        imatch += [m]                                               #     add to inferable match
                        ilvals = ilvals._union(m._getLvals())                       #     collate inferable lvals
                        if m._getLop() == '=':
                            ilvalse = ilvalse._union(m._getLvals())                 #     collate inferable lvals with op '='
                self._showDebug(clas='QueryElement',method='_collateMatch',line=1903,level=2,vars=[['rpfound',rpfound],['ilvalse',ilvalse],['imatch',imatch]])
                if rpfound == 'find' and ilvalse:
                    tmp = ilvalse._intersection(rpreds)
                    if tmp:
                        rpfound = True
                        if (len(tmp) == len(ilvalse)                                #     check to later append rule key to collated QueryExpressions..
                        and len(ilvalse) == len(ilvals)                             #     if inferable QueryExpression values contain only reserved predicates:
                            ): rkneeded = False                                     #      no rule key needed
                if imatch:                                                          #    if inferable match present:
                    if len(imatch) < len(match):                                    #     if inferable match a subset of the match:
                        iqelms,iluqves,ixb = self._collateMatch(imatch              #      collate it again seperately
                                                               ,qlist
                                                               ,rpfound=rpfound
                                                               ,isInfered=True
                                                                )
                else:                                                               #    elif no inferable match:
                    iqelms = Queryable._getUnique(QueryElement(force=imatch))       #     make empty inferable QueryElement
                    rkneeded = False                                                #     no rule key needed
        useIndex = 0                                                                # assume useIndex for =
        if isinstance(qlist,QueryList):
            qlist = qlist._getMatch()                                               # ensure qlist contains (if anything) a list of Queries
            self._showDebug(clas='QueryElement',method='_collateMatch',line=1924,level=1,vars=[['qlist',qlist]])
        if match:
            unboundvars     = mtutils.slist()
            unboundvals     = mtutils.slist()
            unboundvalexps  = mtutils.slist()
            boundvals       = mtutils.sdict()
            boundvars       = mtutils.sdict()
            solvedexps      = mtutils.sdict()
            qlistvars       = mtutils.sdict()
            match1 = match[:]
            # 1) collates query variables for query value, query op pairs - to eliminate duplicate searches for different variables
            for exp in match1:
                vars    = exp._getVars()
                if isinstance(exp,QueryExpression):
                    self._showDebug(clas='QueryElement',method='_collateMatch',line=1938,level=1,vars=[['exp._expandMatch()',exp._expandMatch()]])
                    op      = exp._getLop()
                    nop     = exp._getNop()
                    vals    = exp._getVals()
                    lvals   = exp._getLvals()
                    valexp  = exp._getValexp()
                    if useIndex < 8:
                        if exp._getIsRegex(): useIndex1 = 8
                        else: useIndex1 = rankop[nop]
                        if not useIndex: useIndex = useIndex1
                        elif int(useIndex/2) != int(useIndex1/2): useIndex = 8
                    self._showDebug(clas='QueryElement',method='_collateMatch',line=1949,level=2,vars=[['op',op],['exp._getTop()',exp._getTop()],['exp._getLop()',exp._getLop()],['vals',vals],['vars',vars],['useIndex',useIndex]])
                    if exp._getBindings():                                          # if exp already solved:
                        solvedexps[exp._getQid()] = (exp,vars,op,lvals,useIndex)    #  uniquele add to solvedexps
                        xb = True                                                   #  extra bindings True
                    elif vars and lvals:                                            # if equated to string values (not valexp or triples)
                        if op:
                            for val in lvals:
                                self._showDebug(clas='QueryElement',method='_collateMatch',line=1956,level=2,vars=[['boundvals',boundvals]])
                                if valexp: boundvals = boundvals._deepUnion({((exp._getSval()[0],exp._getEop(),val[0]),op):vars})
                                else: boundvals = boundvals._deepUnion({(val,op):vars})
                                self._showDebug(clas='QueryElement',method='_collateMatch',line=1959,level=2,vars=[['boundvals',boundvals]])
                            match.remove(exp)
                    elif vars:
                        self._showDebug(clas='QueryElement',method='_collateMatch',line=1962,level=2,vars=[['unboundvars',unboundvars]])
                        unboundvars = unboundvars._union(vars)
                        self._showDebug(clas='QueryElement',method='_collateMatch',line=1964,level=2,vars=[['unboundvars',unboundvars]])
                        match.remove(exp)
                    elif lvals:
                        self._showDebug(clas='QueryElement',method='_collateMatch',line=1967,level=2,vars=[['unboundvals',unboundvals]])
                        if valexp: unboundvalexps = unboundvalexps._union([(exp._getSval()[0],exp._getEop(),vals[0])])
                        else: unboundvals = unboundvals._union(lvals)
                        self._showDebug(clas='QueryElement',method='_collateMatch',line=1970,level=2,vars=[['unboundvals',unboundvals]])
                        match.remove(exp)
                elif isinstance(exp,QueryList):                                     # collate any QueryList Queries
                    vals = exp._getMatch()
                    self._showDebug(clas='QueryElement',method='_collateMatch',line=1974,level=1,vars=[['vars',vars],['vals',vals]])
                    qlistvars = qlistvars._deepUnion({tuple(vars):vals})
                    self._showDebug(clas='QueryElement',method='_collateMatch',line=1976,level=1,vars=[['qlistvars',qlistvars]])
                    match.remove(exp)
                else: qlist += [exp]                                                # collate any Queries
            self._showDebug(clas='QueryElement',method='_collateMatch',line=1979,level=1,vars=[['match',match]])
            # 2) unsolved queries: collates query values for query variables (collated in 1), query op pairs - for gen/specialisation filter tests
            for (val,op),vars in boundvals.items():
                if isinstance(val,tuple): k = 0
                else: k = 1
                boundvars[k][(tuple(vars),op)] += [val]
            self._showDebug(clas='QueryElement',method='_collateMatch',line=1985,level=1,vars=[['boundvars',boundvars]])
            # 3) for solved QueryExpressions: collate as is - note filterVals not needed since these are always specific
            self._showDebug(clas='QueryElement',method='_collateMatch',line=1987,level=1,vars=[['solvedexps',solvedexps]])
            if solvedexps:
                for (exp,vars,op,lvals,useIndex) in solvedexps.values():
                    match,luqves,rkfound,useIndex,lv0c,lvs0 = \
                    finaliseMatch(match,luqves,rkfound,useIndex,lv0c,lvs0,solvedexp=exp,vars=vars,op=op,vals=lvals)
            # 4) for unsolved bound variables: filters QueryExpressions logically contained within others also mindfull of gen/specialisation filter preferences
            filtered = []
            for k in boundvars:
                for (vars,op),vals in sorted(boundvars[k].items(),reverse=True):
                    vars = list(vars)
                    vals = filterVals(vals)
                    varsop = vars+[op]
                    instantiate = True
                    for [varsop1,vals1] in filtered:
                        if (varsop1.issuperset(set(varsop))
                            and (vals1.issuperset(set(vals))
                              or (QEfilter == 'generalise' and '*' in vals1)
                              or (QEfilter == 'specialise' and '*' in vals)
                                 )
                                ): instantiate = False
                    if instantiate:
                        filtered += [[set(varsop),set(vals)]]
                        if k:
                            match,luqves,rkfound,useIndex,lv0c,lvs0 = \
                            finaliseMatch(match,luqves,rkfound,useIndex,lv0c,lvs0,op=op,vars=vars,vals=vals)
                        else:
                            match,luqves,rkfound,useIndex,lv0c,lvs0 = \
                            finaliseMatch(match,luqves,rkfound,useIndex,lv0c,lvs0,op=op,vars=vars,valexps=vals)
            # 5) for unbound variables: filters QueryExpressions logically contained within others
            self._showDebug(clas='QueryElement',method='_collateMatch',line=2016,level=1,vars=[['unboundvars',unboundvars]])
            if unboundvars:
                match,luqves,rkfound,useIndex,lv0c,lvs0 = \
                finaliseMatch(match,luqves,rkfound,useIndex,lv0c,lvs0,unboundvars=unboundvars)
            # 6) for unbound valexps: filters QueryExpressions logically contained within others also mindfull of gen/specialisation filter preferences
            self._showDebug(clas='QueryElement',method='_collateMatch',line=2021,level=1,vars=[['unboundvalexps',unboundvalexps]])
            if unboundvalexps:
                match,luqves,rkfound,useIndex,lv0c,lvs0 = \
                finaliseMatch(match,luqves,rkfound,useIndex,lv0c,lvs0,unboundvalexps=filterVals(unboundvalexps))
            # 7) for unbound values: filters QueryExpressions logically contained within others also mindfull of gen/specialisation filter preferences
            self._showDebug(clas='QueryElement',method='_collateMatch',line=2026,level=1,vars=[['unboundvals',unboundvals]])
            if unboundvals:
                match,luqves,rkfound,useIndex,lv0c,lvs0 = \
                finaliseMatch(match,luqves,rkfound,useIndex,lv0c,lvs0,unboundvals=filterVals(unboundvals))
            self._showDebug(clas='QueryElement',method='_collateMatch',line=2030,level=1,vars=[['match',match]])
            if qlistvars:                                                           # if collated Queries: append as a QueryList to QueryExpressions list
                for vars,vals in qlistvars.items():
                    self._showDebug(clas='QueryElement',method='_collateMatch',line=2033,level=1,vars=[['vars',vars],['vals',vals]])
                    match += [Queryable._getUnique(QueryList(vars=list(vars),match=vals))]
            self._showDebug(clas='QueryElement',method='_collateMatch',line=2035,level=1,vars=[['rkfound',rkfound],['rkneeded',rkneeded],['imatch',imatch]])
            if rkfound is False and rkneeded:                                       # if rule key not found but needed and inferable match:
                match += [rkqe]                                                     #  add its QueryExpression to match
                if lv0c is not None: lv0c,lvs0 = updateLVS([],lv0c,lvs0)            # if updating logical variable keys: do so
        if qlist: match += [Queryable._getUnique(QueryList(match=qlist))]           # if collated Queries: append as a QueryList to QueryExpressions list
        if not match: raise mterrors.QueryExpressionError(match)                    # if nothing: raise error
        if rpfound is not None:
            qelms = Queryable._getUnique(QueryElement(force=match))
            if isInfered:
                self._showDebug(clas='QueryElement',method='_collateMatch',note='returns',line=2044,level=0,vars=[['match',match]])
                self._showDebug(clas='QueryElement',method='_collateMatch',note='returns',line=2045,level=0,vars=[['luqves',luqves]])
                return qelms,luqves,xb
            else:
                if iqelms is None:                                                  #  if inferable match not yet set: (set as match)
                    iqelms = qelms                                                  #   set iqelms as qelms
                    iluqves = luqves                                                #   with match key
                    ixb = xb                                                        #   and match extra bindings
#                if rpf == 'find': rpf = False                                      # !! leave in only if reserved predicates in col 1 of triples
                self._showDebug(clas='QueryElement',method='_collateMatch',note='returns',line=2053,level=0,vars=[['match',match]])
                self._showDebug(clas='QueryElement',method='_collateMatch',note='returns',line=2054,level=0,vars=[['imatch',imatch]])
                self._showDebug(clas='QueryElement',method='_collateMatch',note='returns',line=2055,level=0,vars=[['luqves',luqves]])
                self._showDebug(clas='QueryElement',method='_collateMatch',note='returns',line=2056,level=0,vars=[['iluqves',iluqves]])
                self._showDebug(clas='QueryElement',method='_collateMatch',note='returns',line=2057,level=0,vars=[['rpfound',rpfound],['useIndex',useIndex],['rkneeded',rkneeded]])
                return qelms,iqelms,luqves,iluqves,rpfound,useIndex,lv0c,lvs0,xb,ixb
        else:
            self._showDebug(clas='QueryElement',method='_collateMatch',note='returns',line=2060,level=0,vars=[['match',match]])
            return match
    def _interpolate(self,qelm):
        # usage:
        #    Passes values between a query and its solution, here both represented by QueryElement objects.
        #    (That is between query object variables and solving object variables)
        #    Specifically it collates the 3 indexes it returns
        # inputs:
        #    self  - solving or implementing (invoked) QueryElement
        #    qelm  - calling or querying (invoking) QueryElement
        # returns:
        #    vs    - dict of query keys indexed by rhs rule variables ie. {'?var1':key1,..,'?varn':keyn}
        #    rs    - dict of query varnames indexed by rhs rule varnames ie. {'rvarname1':'qvarname1',...}
        #    bd    - dict of bindings detected from interpolation ie. {'qvarname1':'val1',...}
        #            (typically where the rule predicate equates with a query variable)
        self._showDebug(clas='QueryElement',method='_interpolate',note='inputs',line=2075,level=0,vars=[['qelm',qelm]])
        self._showDebug(clas='QueryElement',method='_interpolate',note='inputs',line=2076,level=0,vars=[['self._expandMatch()',self._expandMatch()]])
        if not isinstance(qelm,QueryElement):
            qelm = Queryable._getUnique(QueryElement(match=qelm))
        self._showDebug(clas='QueryElement',method='_interpolate',note='inputs',line=2079,level=0,vars=[['qelm._expandMatch()',qelm._expandMatch()]])
        rs = mtutils.sdict()                                                        # for indexing query varnames by rule varnames
        vs = mtutils.sdict()                                                        # for indexing query keys by rule variables
        bd = mtutils.sdict()                                                        # for collecting interpolation bindings
        qexps = qelm._getMatch()                                                    # get the QueryExpressions in this QueryElement
        self._showDebug(clas='QueryElement',method='_interpolate',line=2084,level=1,vars=[['qexps',qexps]])
        qexps_withVals = []                                                         # prepare to collate values for QueryElement
        for qexp in qexps:                                                          # for each QueryExpression in QueryElement:
            qvals = qexp._getLvals()                                                #  get its logical query values
            self._showDebug(clas='QueryElement',method='_interpolate',line=2088,level=1,vars=[['qvals',qvals]])
            if qvals and qvals != ['?']:                                            #  if logical query values exist for fact element(s):
                qexps_withVals += [qexp]                                            #   append to collection
            if isinstance(qexp,QueryList): triples = qexp                           #  also collate return variables from nested QueryLists
            else: triples = qexp._getTriples()                                      #   or Triple value expressions
            if triples: rs = rs._deepUnion(triples._collateVars())
        qvars = qelm._getVars()                                                     # collate query variables list
        self._showDebug(clas='QueryElement',method='_interpolate',line=2095,level=1,vars=[['qvars',qvars]])
        try:                                                                        # prepare to interpolate reporting mismatches
            for lexp in self._getMatch():                                           #  for each local QueryExpression:
                self._showDebug(clas='QueryElement',method='_interpolate',line=2098,level=2,vars=[['lexp',lexp]])
                if isinstance(lexp,QueryExpression):                                #   if its a QueryExpression:
                    lvars = lexp._getVars()                                         #    get the local query variables
                    self._showDebug(clas='QueryElement',method='_interpolate',line=2101,level=2,vars=[['lvars',lvars]])
                    if lvars:                                                       #    if local query variables:
                        for lvar in lvars:                                          #     for each local query variable
                            self._showDebug(clas='QueryElement',method='_interpolate',line=2104,level=2,vars=[['lvar',lvar]])
                            if qexps_withVals and '?'+lvar not in vs:               #      index query QueryExpressions with values (if any)
                                vs['?'+lvar] = qexps_withVals                       #       by local query variable
                            rs[lvar] = qvars                                        #      index query query variables (null or not) by local query variable
                            self._showDebug(clas='QueryElement',method='_interpolate',line=2108,level=2,vars=[['vs',vs],['rs',rs]])
                    elif qvars:                                                     #    else no local query variables, but if query query variables:
                        lvals = lexp._getVals()                                     #     prepare to bind directly to any local QueryExpression values
                        if lvals:                                                   #     if local QueryExpression values:
                            self._showDebug(clas='QueryElement',method='_interpolate',line=2112,level=2,vars=[['lvals',lvals],['qvars',qvars]])
                            if isinstance(lvals,list) and len(lvals) == 1:          #      !!Temp fix for lvals as a list in bv!!
                                lvals = lvals[0]
                            for qvar in qvars:                                      #      for each query query variable:
                                if qvar not in bd: bd[qvar] = lvals                 #       bind it to the local QueryExpression values
                                self._showDebug(clas='QueryElement',method='_interpolate',line=2117,level=2,vars=[['qvar',qvar],['bd',bd]])
#                else:                                                               #   else: (its a sub-Query)
#                    for qexp in qexps:                                              #    for each query QueryExpression:
                        self._showDebug(clas='QueryElement',method='_interpolate',line=2120,level=1,vars=[['qexp',qexp]])
#                        if isinstance(qexp,Query):                                  #     if matching to sub-Query
#                            v1,r1,b1 = lexp._interpolate(qexp)                      #      interpolate the sub-Query pair
#                            vs = vs._deepUnion(v1)                                  #       collating returned indexes...
#                            rs = rs._deepUnion(r1)
#                            bd = bd._deepUnion(b1)
#                        else:                                                       #     else its not matching an obvious sub-Query pair
#                            triples = qexp._getTriples()                            #      but there may still be sub-Queries expressed triples syntax
#                            if triples:                                             #      if triples:
#                                for triple in triples:                              #       interpolate each as sub-Query paired with the local sub-Query
#                                    v1,r1,b1 = lexp._interpolate(triple)
#                                    vs = vs._deepUnion(v1)                          #        collating returned interpolation indexes
#                                    rs = rs._deepUnion(r1)
#                                    bd = bd._deepUnion(b1)
#                            elif (qexp._getVals() or qexp._getValexp):              #     else test query variables can be bound directly to the
#                                raise mterrors.QueryElementInterpolationError(qelm._expandMatch(),self._expandMatch())
        except mterrors.QueryableError, X:
            X._notify(c='QueryElement',
                      m='_interpolate()')                                           # notify QueryableError
        self._showDebug(clas='QueryElement',method='_interpolate',note='returns',line=2139,level=0,vars=[['vs',vs],['rs',rs],['bd',bd]])
        return vs,rs,bd                                                             #     return

class Query(Queryable):
    def __init__(self,match='',rs=None,rrs=None,pOK=True):
        Queryable.__init__(self,match=match,rs=rs,rrs=rrs,pOK=pOK)
    def _setMatch(self,match=None,rs=None,rrs=None,pOK=True):
        # usage:
        #    sets a triple tuple of QueryElements with optional variable interpolation based on rs
        # inputs:
        #    match - Query match
        #    rs    - dict of existing variable names to be swapped for new variable names
        #    rrs   - dictionary of swap varnames to original varnames (reverse of rs: original_varnames keyed by swapped_varnames)
        #    pOK   - allow embedded plural QueryElements (True|False)
        # returns:
        #    match1 as a tuple of QueryElements with variables swapped or not
        if not match: match = (wkqe,wkqe,wkqe)                                     # set default match if None
        self._showDebug(clas='Query',method='_setMatch',note='inputs',line=2156,level=0,vars=[['match',match],['rs',rs],['rrs',rrs],['pOK',pOK]])
        match1 = []
        if not isinstance(match,tuple): raise mterrors.QueryFormatError(match)
        elif len(match) != 3: raise mterrors.QueryTripleError(match)
        else:
            if rs and rrs is None: rrs = rs._invert()
            for m in match:
                m1 = None
                try:
                    if (not pOK
                    and isinstance(m,list)
                    and len(m) > 1): raise mterrors.RuleQueryElementCardinalityError(m)
                except mterrors.RuleLhsQueryElementError, X:
                    X._notify(c='Query',
                              m='_setMatch()')                                      # notify QueryableError
                    m = m[0]                                                        # and handle by discarding all but the 1st QExp
                if isinstance(m,QueryElement): m1 = m
                else: m1 = Queryable._getUnique(QueryElement(match=m,rs=rs,rrs=rrs,pOK=pOK)
                                                )                                   # instantiate QueryElement
                if m1: match1 += [m1]                                               # if instantiated add QueryElement to this Query match
                else:                                                               # else: abandon instantiating the query
                    match1 = []
                    break
        if not match1: raise mterrors.QueryExpressionError(m)                       # Query not instantiable: so raise error
        else: match1 = tuple(match1)                                                # else: instantiate Query match as tuple
        self._match = match1
        self._showDebug(clas='Query',method='_setMatch',note='returns',line=2182,level=0,vars=[['match1',match1]])
        self._showDebug(clas='Query',method='_setMatch',note='returns',line=2183,level=0,vars=[['self._expandMatch()',self._expandMatch()]])
        return match1
    def _expandMatch(self,ordered=True,thin=False,sourceStore=None,targetStore=None):
        # usage:
        #    gets a match expressed in terms of Query Language Syntax
        #    expansions are cached for subsequent retrieval
        #    optionally re-orders triples from sourceStore to targetStore
        # inputs:
        #    ordered     - optional setting to validate and sort QueryLists within each Equation
        #    thin        - optional set to True to eliminate 1 string item leaf collections - for improved legability
        #    sourceStore - store originating this Query - for input  triple ordering
        #    targetStore - store exploiting this Query  - for output triple ordering
        # outputs:
        #    match       - expanded match. null if invalid.
        self._showDebug(clas='Queryable',method='_expandMatch',note='inputs',line=2197,level=0,vars=[['self',self],['ordered',ordered],['thin',thin]])
        if (ordered,thin,sourceStore,targetStore) in self._em:                      # if this expanded match is cached:
            match = self._em[(ordered,thin,sourceStore,targetStore)]                #  get it
        else:                                                                       # else:
            m = self._getMatch(ordered=ordered)                                     #  get the match
            if targetStore and targetStore != sourceStore:                          #  if a Query and source and target stores different:
                m = targetStore._rt(m,order=sourceStore._getTripleOrder())          #   express match in target triple order of targetStore
                self._showDebug(clas='Query',method='_expandMatch',line=2204,level=1,vars=[['m',m]])
            match = self._expandMatch1(m,ordered,thin,sourceStore,targetStore)      #  derive the expanded match
            self._em[(ordered,thin,sourceStore,targetStore)] = match                #  and cache it (in the expanded match cache)
        self._showDebug(clas='Query',method='_expandMatch',note='returns',line=2207,level=0,vars=[['match',match]])
        return match
    def _getVars(self):
        vars = mtutils.slist()
        for e in self._getMatch(): vars = vars._union(e._getVars())
        self._showDebug(clas='QueryElement',method='_getVars',note='returns',line=2212,level=0,vars=[['vars',vars]])
        return vars
    def _interpolate(self,query):
        # usage:
        #    Passes values between a query and its solution, here both represented by Query objects.
        #    (That is between query object variables and solving object variables)
        #    Specifically it completes the interpolation done at a QueryElement granularity by:
        #     1. collating QueryElement interpolation indexes (vs,rs,db)
        #     2. re-instantiating "vs" QueryExpressions with solving (or rule) variables - done by setVSvars()
        # inputs:
        #    self  - solving or implementing (invoked) Query
        #    query - querying (invoking) Query or query variables as triple
        # returns:
        #    vs    - dict of query keys indexed by rhs rule variables ie. {'?var1':key1,..,'?varn':keyn}
        #    rs    - dict of query varnames indexed by rhs rule varnames ie. {'rvarname1':'qvarname1',...}
        #    bd    - dict of bindings detected from interpolation ie. {'qvarname1':'val1',...}
        #            (typically where the rule predicate equates with a query variable)
        def setVSvars(vs):
            # usage:
            #    switches Variable Substitution index QueryExpressions from querying to solving variables. e.g.
            #    input  vs = {solving_var1:[querying_Qexp1.1_with_querying_vars,..,querying_Qexp1.n_with_querying_vars],..}
            #    output vs = {solving_var1:[querying_Qexp1.1_with_solving__vars,..,querying_Qexp1.n_with_solving__vars],..}
            # inputs:
            #    vs  - querying QueryExpressions indexed by substitute solving variables (vars)
            # returns:
            #    vs1 - new vs with variables substituted in its new indexed QueryExpressions
            self._showDebug(clas='Query',method='_interpolate',note='.setVSvars inputs',line=2238,level=0,vars=[['vs',vs]])
            vs1 = mtutils.sdict()
            for var in vs:                                                          # for each interpolated var substitute:
                self._showDebug(clas='Query',method='_interpolate',note='.setVSvars',line=2241,level=1,vars=[['var',var]])
                self._showDebug(clas='Query',method='_interpolate',note='.setVSvars',line=2242,level=1,vars=[['vs[var]',vs[var]]])
                for exp in vs[var]:
                    exp1 = exp._modifiedClone(vars=[var[1:]])                       # instantiate candidate finalised QueryExpression/QueryList
                    if var not in vs1 or exp1 not in vs1[var]:
                        vs1[var] += [exp1]
                        self._showDebug(clas='Query',method='_interpolate',note='.setVSvars',line=2247,level=2,vars=[['exp1._expandMatch()',exp1._expandMatch()],['exp1',exp1]])
            self._showDebug(clas='Query',method='_interpolate',note='.setVSvars returns',line=2248,level=0,vars=[['vs1',vs1]])
            return vs1
        self._showDebug(clas='Query',method='_interpolate',note='inputs',line=2250,level=0,vars=[['self',self],['query',query]])
        if not isinstance(query,Query): query = Queryable._getUnique(Query(match=query))
        self._showDebug(clas='Query',method='_interpolate',note='inputs',line=2252,level=0,vars=[['self._expandMatch()',self._expandMatch()]])
        self._showDebug(clas='Query',method='_interpolate',note='inputs',line=2253,level=0,vars=[['query._expandMatch()',query._expandMatch()]])
        # prepare to collate QueryElement interpolation indexes
        rs = self._collateVars()                                                    # for indexing query varnames by rule varnames
        vs = mtutils.sdict()                                                        # for indexing query keys by rule variables
        bd = mtutils.sdict()                                                        # for collecting interpolation bindings
        self._showDebug(clas='Query',method='_interpolate',line=2258,level=1,vars=[['rs',rs]])
        query = query._getMatch()
        self._showDebug(clas='Query',method='_interpolate',line=2260,level=1,vars=[['query',query]])
        self._showDebug(clas='Query',method='_interpolate',line=2261,level=1,vars=[['self._getMatch()',self._getMatch()]])
        # collate QueryElement interpolation indexes
        for c,lelm in enumerate(self._getMatch()):
            qelm = query[c]
            self._showDebug(clas='Query',method='_interpolate',line=2265,level=1,vars=[['lelm',lelm],['qelm',qelm]])
            v1,r1,b1 = lelm._interpolate(qelm)
            self._showDebug(clas='Query',method='_interpolate',line=2267,level=1,vars=[['v1',v1],['r1',r1],['b1',b1]])
            vs = vs._deepUnion(v1)                                                  #     collate variable substitutions
            rs = rs._deepUnion(r1,replace=True)                                     #     collate variable_name return subsititions
            bd = bd._deepUnion(b1)                                                  #     collate interpolated variable bindings
            self._showDebug(clas='Query',method='_interpolate',line=2271,level=1,vars=[['vs',vs],['rs',rs],['bd',bd]])
        # switch collated "vs" QueryExpressions from quering to solving variables
        vs1 = setVSvars(vs)
        self._showDebug(clas='Query',method='_interpolate',note='returns',line=2274,level=0,vars=[['vs1',vs1]])
        self._showDebug(clas='Query',method='_interpolate',note='returns',line=2275,level=0,vars=[['_expandVS(vs1)',_expandVS(vs1)]])
        self._showDebug(clas='Query',method='_interpolate',note='returns',line=2276,level=0,vars=[['rs',rs]])
        self._showDebug(clas='Query',method='_interpolate',note='returns',line=2277,level=0,vars=[['bd',bd]])
        return vs1,rs,bd                                                             #     return
    def _makeKey(self,vs,rs,store,rd,infer):
        # usage:
        #    prepares keys for a TripleStore to solve this query
        # inputs:
        #    vs            - value substitution dict   (for passing querying QueryExpressions to solving QueryExpressions)
        #    rs            - return substitutions dict (for returning bound values from solving to querying variables)
        #    store         - store (should nested Queries need evaluating)
        #    rd            - current recursion depth (of rule based inference)
        #    infer         - Infer missing facts from rules. [None|True|False|'ffi'].
        # returns:
        #    aquery        - aggregate (exact+inferred) Query
        #    iquery        - inferable Query
        #    lo            - logical column ordering in keys
        #    keys          - list of QueryExpressions to match. Note: key[0] represents the index key
        #    akey          - aggregate (exact+inferred) query as a triple key expression (ie. variables stripped, and generated keys stripped)
        #    ikey          - inferable query as a triple key expression (ie. variables stripped, and generated keys stripped)
        #    axb           - aggregate query has extra bindings [True|False] (from internals of pre-solved nested Queryables)
        #    ixb           - inferable query has extra bindings [True|False] (from internals of pre-solved nested Queryables)
        #    isBoolean     - is this a boolean query? [True|False]
        #    lvs0          - index of logical to physical variables {lvar1:[pvar1,pvar2,..],..,lvarN:[pvarN1,..]}
        #                     so that queries may expressed for caching in terms of logical variables
        #    lvs1          - index of physical to logical variables {pvar1:[lvar1,lvar2,..],..,pvarN:[lvarN1,..]}
        self._showDebug(clas='Query',method='_makeKey',note='inputs',line=2301,level=0,vars=[['vs',vs],['infer',infer]])
        qelms     = self._getMatch()                                                # QueryElements in self
        aqelms    = mtutils.slist()                                                 # Collated ANDed QueryElements (physical aggregate)
        d_aqelms  = mtutils.slist()                                                 # FOR DEBEG: Expanded aqelms1  (physical aggregate)
        iqelms    = mtutils.slist()                                                 # Collated ANDed QueryElements (physical inferrable)
        d_iqelms  = mtutils.slist()                                                 # FOR DEBEG: Expanded iqelms1  (physical inferrable)
        akey      = mtutils.slist()                                                 # Collated ANDed Query Keys    (independent aggregate)
        ikey      = mtutils.slist()                                                 # Collated ANDed Query Keys    (independent inferrable)
        rpfound   = 'find'                                                          # initialise "reserved predicate found" to 'find'
        isBoolean = True                                                            # initialise "query is boolean" to True
        useIndex  = mtutils.slist()                                                 # initialise list of index types for Query keys
        lv0c      = -1                                                              # initialise logical variable id
        lvs0      = mtutils.sdict()                                                 # index of logical to physical variables
        lvs1      = mtutils.sdict()                                                 # index of physical to logical variables
        axb       = False                                                           # aggregate query has extra bindings [True|False]
        ixb       = False                                                           # inferable query has extra bindings [True|False]
        stoi      = store._getStoi()                                                # get triple order index for this store
        for c in [stoi['p'],stoi['s'],stoi['o']]:                                   # for each QueryElement in this Query (predicate 1st - for performance only):
            try: elm = qelms[c]._applyVS(vs,rs,store,rd,infer)                      #  try unifying QueryElement to input
            except mterrors.QueryElementInterpolationError, X:                      #  except: InterpolationError
                if QEierror:                                                        #   if preferred:
                    X._notify(c='Query',
                              m='_makeKey()')                                       #    notify InterpolationError
                raise mterrors.QueryElementInterpolationError()                     #   and propogate InterpolationError
            aqelms[c],iqelms[c],akey[c],ikey[c],rpfound,useIndex[c],lv0c,lvs0,axb1,ixb1 = \
            elm._collateMatch(elm._getMatch()
                             ,[]
                             ,rpfound=rpfound
                             ,infer=infer
                             ,lv0c=lv0c
                             ,lvs0=lvs0
                              )                                                     #  collate Expressions with QueryElement
            self._showDebug(clas='Query',method='_makeKey',line=2333,level=2,vars=[['iqelms[c]._expandMatch()',iqelms[c]._expandMatch()],['iqelms[c]._getMatch()',iqelms[c]._getMatch()],['iqelms[c]',iqelms[c]]])
            if useIndex[c] != 2: isBoolean = False                                  #  if index can't be used: query result isn't singular
            if ixb1: ixb = True                                                     #  if extra inferable bindings found: flag it
            if axb1: axb = True                                                     #  if extra aggregate bindings found: flag it
        # Instantiate aggregate and inferred physical Query objects for their unique ids later
        aquery = Queryable._getUnique(Query(match=tuple(aqelms)))
        iquery = Queryable._getUnique(Query(match=tuple(iqelms)))
        ## Finalise logical query keys
        akey = QueryKey(match=akey)._expandMatch()
        ikey = QueryKey(match=ikey)._expandMatch()
        ## Index physical to logical variables - invert lvs0 -> lvs1
        for lv0,lv1s in lvs0.items():
            for lv1 in lv1s:
                if lv1 not in lvs1: lvs1[lv1] = [lv0]
                elif lv0 not in lvs1[lv1]: lvs1[lv1] += [lv0]
        ## Add additional variables from extra bindings (if any) to key maps
        if axb:
            for elm in aqelms:
                for exp in elm._getMatch():
                    xbs = exp._getBindings()                                        #  get suppl bindings (from nested Queryables - if any)
                    if xbs:                                                         #  if suppl bindings: (include them in log<->phys indexes)
                        xb = True
                        for xb1 in sorted(xbs):                                     #   for each nested match value:
                            for lv1,xb2 in sorted(xbs[xb1].items()):                #    for each match var,val pair associated with this:
                                if lv1 not in lvs1:                                 #     if exra binding variable not yet mapped: (map it)
                                    lv0c += 1                                       #      get next logical variable id
                                    lv0 = '!'+str(lv0c)                             #      get the logical variable name
                                    lvs1[lv1] = [lv0]                               #      add to physical vars index
                                    lvs0[lv0] = [lv1]                               #      add to logical vars index
        # Summation debug outputs
        self._showDebug(clas='Query',method='_makeKey',note='summary',line=2363,level=1,vars=[['Query     Qexps   ',self._expandMatch()]])
        self._showDebug(clas='Query',method='_makeKey',note='summary',line=2364,level=1,vars=[['Input     QExps   ',_expandVS(vs)]])
        self._showDebug(clas='Query',method='_makeKey',note='summary',line=2365,level=1,vars=[['Inferable QExps   ',iquery._expandMatch()]])
        self._showDebug(clas='Query',method='_makeKey',note='summary',line=2366,level=1,vars=[['Aggregate key     ',akey]])
        self._showDebug(clas='Query',method='_makeKey',note='summary',line=2367,level=1,vars=[['Inferable key     ',ikey]])
        self._showDebug(clas='Query',method='_makeKey',note='summary',line=2368,level=1,vars=[['Physical  bindings',lvs1]])
        self._showDebug(clas='Query',method='_makeKey',note='summary',line=2369,level=1,vars=[['Logical   bindings',lvs0]])
        self._showDebug(clas='Query',method='_makeKey',note='returns',line=2370,level=0,vars=[['iquery._expandMatch()',iquery._expandMatch()],['iquery',iquery]])
        self._showDebug(clas='Query',method='_makeKey',note='returns',line=2371,level=0,vars=[['akey',akey]])
        self._showDebug(clas='Query',method='_makeKey',note='returns',line=2372,level=0,vars=[['ikey',ikey]])
        self._showDebug(clas='Query',method='_makeKey',note='returns',line=2373,level=0,vars=[['isBoolean',isBoolean],['lvs0',lvs0]])
        return aquery,iquery,akey,ikey,axb,ixb,isBoolean,lvs0,lvs1,useIndex
    def _solve(self,store,vs={},rs={},gr=None,rikeys=None,infer=None,ql='None',eq='None',eql='None',rd=None):
        # inputs:
        #    store    - TripleStore used
        #    vs       - variable substitution dict (for rule interpretation only)
        #    rs       - return substitutions dict  (for rule interpretation only - local but not nested variables)
        #    gr       - generic rule identifier (if applicable)
        #    rikeys   - recursed infered keys used in lower recursions
        #    infer    - Infer missing facts from rules. [None|True|False|'ffi'].
        #                If None uses config item 'stores_infer' instead.
        #                _export() sets infer to False via _triples().
        #    ql       - unique id of source QueryList
        #    eq       - unique id of source Equation
        #    eql      - unique id of source EquationList
        #    rd       - current recursion depth (recursive inference)
        # yields:
        #    triples, rules and bindings tuple by tuple
        # Notes:
        #    1. query may:
        #       - contain nested triples
        #       - contain exact or wildcard elements
        #       - wildcard elements may be bound to a named variable
        #       - named variables may be listed to force bound value equivalence
        #    2. query trace is stored in qtrace keyed by 'trace' (since this is orthogonal to recursion it cannot be passed via yield)
        #    3. outcomes caching as follows:
        #       - query outcomes use pre-emptive caching.
        #         That is outcomes are added to caches as they become available rather than when they are complete.
        #         Theoretically a problem may occur with this cache being prematurely read in the following sort of situation:
        #                ak0-1      - 1st invocation, last to complete cache update
        #                 /
        #               ak0-2       - 2nd invocation, updates cache
        #               / \
        #             any ak0-4     - 4th invocation before 1st or 2nd have completed but with results on the cache from 3rd which it will use
        #             /
        #          ak0-3            - 3rd invocation, first cache update
        #         For some reason attempts to prevent this until cache update from 1st invocation is complete cause missing results
        #         Alternative attempts to let re-invocations use both cache and dupplement it yield no more results but destroy performance
        #       - rules outcomes use recursion-depth controled caches.
        #         That is outcomes are only added to caches when complete. 2 levels supported:
        #          - physically keyed rule cache for rules whose logically keyed results haven't yet completed
        #          - logically  keyed rule cache for completed rules (at which point the physically keyed results get deleted)
        def bind_lvs(b,lvs):
            # usage:
            #    swaps bindings variables between logical and physical based on lvs indexes
            #     - lvs0: swaps physical vars for logical vars
            #     - lvs1: swaps logical vars for physical vars
            #    ie:
            #        input  b   = {'!1':['a'],'!2':['b']}
            #        input  lvs = {'!1':['ov1','ov2'],'!2':['ov3']} from lvs0
            #        output b   = {'ov1':['a'],'ov2':['a'],'ov3':['b']}
            #        where  !1, !2 are logical vars, and ov1, ov2, ov3 are original vars
            # inputs:
            #    b    - query result bindings
            #    lvs  - logical variable swap index {lvar1:pvars1,..,lvarN:pvarsN}/{pvar1:lvars1,..,pvarN:lvarsN}
            # returns:
            #    b    - with variables swapped
            # note:
            #    logical vars for queries enables query results to be cached based on criteria alone
            #     and independent of physical variables to be bound
            b1 = mtutils.sdict()
            for lvar,lvals in b.items():
                if lvar in lvs:
                    for var in lvs[lvar]:
                        b1[var] = lvals
            return b1
        ## End bind_lvs()
        def traceQkey(qkey):
            # usage:
            #    reduces qkey for collation within trace (specifically replaces empty QueryElements with wild QueryValueExpression)
            #    and appends it to the trace
            # inputs:
            #    qkey  - original query key
            qu = []
            for elm in qkey:
                if not elm and isinstance(elm,list): elm = '*'
                qu += [elm]
            qu1 = qtrace._getItem('trace',mtutils.slist())+[tuple(qu)]
            qtrace._setItem('trace',qu1)
            self._showDebug(clas='Query',method='_solve',line=2452,note='.traceQkey',level=1,vars=[['qkey',qkey],['qu',qu],['qu1',qu1]])
        ## End reduceQkey()
        def cqsmaint():
            # usage:
            #    union a result set with the store query success cache
            #    if 1st result - ensure key no longer cached as a failure
            # notes:
            #    the choice of key for indexing individual outcomes is significant.
            #    Both triples and bindings are needed since their is a many to many dependency between these.
            #     e.g. triple <-m---m-> binding
            #    An obvious example being an externally bound Query. (1 internal binding, many possible triples outcomes)
            #    Logical bindings needed since physical bindings reflect invocation specific variable interpolations.
            if mtoc:
                cres = store._db['cqs']._getItem(ak0)
                if not cres:
                    cres = mtindex.Index()
                    store._db['cqf']._delItem(ak0)
                if cres._isUnique(bk,default=[tl,rl,bind_lvs(b,lvs1)],munge=False):
                    store._db['cqs']._setItem(ak0,cres)
                    self._showDebug(clas='Query',method='_solve',note='summary',line=2471,level=1,vars=[['cache query  key',ak0],['rd',rd]])
                    self._showDebug(clas='Query',method='_solve',note='summary',line=2472,level=1,vars=[['cache result key',bk]])
                    self._showDebug(clas='Query',method='_solve',note='summary',line=2473,level=1,vars=[['cache bindings  ',bind_lvs(b,lvs1)]])
        ## End cqsmaint() abdi,atpi,(axb or ard!=rd),b,bk,tl,rl,ak0,lvs1
        def result():
            # usage:
            #    selective unqueness test for results
            #    also maintains:
            #     - local triples and bindings uniqueness indexes
            #     - store query success cache (by invoking cqsmaint)
            # returns:
            #    r   - resulting uniqueness as follows:
            #           if bindings exist is True:   True if triple is unique
            #           if externally bound is True: True if bindings exist and are unique
            r = False                                                               # default yield result
            if b: u = abdi._isUnique(bk,default=1,munge=False)                      # if bindings: get their uniqueness (updating index)
            else: u = atpi._isUnique(tl,default=1,munge=False)                      # else: get the uniqueness of the triple
            if u:                                                                   # if unique for purpose:
                r = True                                                            #  return True
                if not axb and ard == rd: cqsmaint()                                #  if no extra bindings: update cache of query success
            return r                                                                # else: return False
        ## End isUnique()
        self._showDebug(clas='Query',method='_solve',note='inputs',line=2493,level=0,vars=[['self',self]])
        self._showDebug(clas='Query',method='_solve',note='inputs',line=2494,level=0,vars=[['gr',gr],['_expandVS(vs)',_expandVS(vs)],['vs',vs]])
        self._showDebug(clas='Query',method='_solve',note='summary',line=2495,level=1,vars=[['     Query',self._expandMatch(thin=True)]])
        if rd is None: rd = 1
        if rikeys is None: rikeys = {}                                              #   recursed infered keys for solving this query - initialise if None
        store._incMetric('tq')                                                      #   metrics: increment total queries counter
        self._showDebug(clas='Query',method='_solve',line=2499,level=1,vars=[['total q',store._getMetric('tq')]])
        if infer is None: infer = store._getInfer()                                 #   get default inference setting if not overidden
        try:
            aquery,iquery,akey,ikey,axb,ixb,isBoolean,lvs0,lvs1,useIndex = \
            self._makeKey(vs,rs,store,rd+1,infer)                                   #   make keys needed to proceed with searching for this query
            aqid = aquery._getQid()                                                 #   get this aggregate query id
            iqid = iquery._getQid()                                                 #   get this inferred query id
            ak0 = mtutils._mungeKey(akey)                                           #   get string form of active query key (and retain as an index for sbqcache)
#            ak0 = aqid
            self._showDebug(clas='Query',method='_solve',line=2508,level=2,vars=[['aquery._expandMatch()',aquery._expandMatch()],['aquery',iquery]])
            self._showDebug(clas='Query',method='_solve',line=2509,level=2,vars=[['iquery._expandMatch()',iquery._expandMatch()],['iquery',iquery]])
            self._showDebug(clas='Query',method='_solve',line=2510,level=2,vars=[['isBoolean',isBoolean]])
            self._showDebug(clas='Query',method='_solve',line=2511,level=2,vars=[['akey',akey]])
            self._showDebug(clas='Query',method='_solve',line=2512,level=2,vars=[['ikey',ikey]])
            self._showDebug(clas='Query',method='_solve',line=2513,level=2,vars=[['ak0',ak0]])
            self._showDebug(clas='Query',method='_solve',line=2514,level=2,vars=[['axb',axb],['ixb',ixb]])
            self._showDebug(clas='Query',method='_solve',line=2515,level=2,vars=[['lvs0',lvs0]])
            self._showDebug(clas='Query',method='_solve',line=2516,level=2,vars=[['lvs1',lvs1]])
            # check previous query failures
            cut = False                                                             #   default cut setting off
            ard = store._pqcache._getItem(ak0)                                      #   get actual result data (on caching of this query)
            if mtoc and not axb:                                                    #   if caching and no nested bindings (to corrupt cache keys)
                if  not (ard and gr):                                               #    allow pre-emptive access to cache unless a generic query:
                    cut = store._db['cqf']._getItem(ak0)                            #     cut if logical key cached as failing
                    self._showDebug(clas='Query',method='_solve',line=2523,level=1,vars=[['cut',cut]])
                    if cut: store._incMetric('bfq')                                 #     if a query has failed: don't re-run but inc metric
                    else:                                                           #     else: these keys haven't failed (yet)
                        # check previous query successes for results
                        cres = store._db['cqs']._getItem(ak0)                       #      get logically keyed cached results (if any)
                        if cres:                                                    #      if logically keyed cached results found: (use them)
                            # yield query results from cache
                            cut = True                                              #      cut (no further results needed)
                            for [tl,rl,lb] in cres.values():                        #      for each result:
                                b = bind_lvs(lb,lvs0)                               #       bind original variables instead of cached logical equivalents
                                self._showDebug(clas='Query',method='_solve',note='summary result cache yields',line=2533,level=0,vars=[['tl',tl],['rl',rl],['b',b]])
                                yield tl,rl,b                                       #       yield it
                if not cut: ard = store._pqcache._getMember(ak0                     #    if no cached failure or successes: (get ready to cache)
                                                           ,default=rd
                                                           ,returnSet=True
                                                           ,munge=False
                                                            )                       #     by markiung as a query being cached
            if not cut:
                # prepare to solve a new query
                self._showDebug(clas='Query',method='_solve',note='new query',line=2542,level=1,vars=[['akey',akey],['rd',rd]])
                traceQkey(akey)                                                     #     append query to trace
                if isBoolean: store._incMetric('tbq')                               #     metrics: increment total boolean queries counter
                abdi = mtindex.Index()                                              #     initialise aggregate unique bindings index
                atpi = mtindex.Index()                                              #     initialise aggregate unique triples  index
                ires0 = mtindex.Index()                                             #     initialise logically keyed infered (rules) results index
                ik0 = mtutils._mungeKey(ikey)                                       #     logical inference (rules) key
                done  = {}                                                          #     initialise repeat rule blocking dict
                skiprules = False                                                   #     flag to skip remaining rules (if logically keyed cache accessed)
                crs = [store._db['crs'],store._crs]                                 #     list of rule success caches [logical,physical]
                crf = [store._db['crf'],store._crf]                                 #     list of rule failure caches [logical,physical]
                for qs,t,b,i in \
                store._solveTriple(aquery,useIndex,rd=rd+1,infer=infer,rs=rs):      #     for each matching triple and bound physical variable index
                    cols = mtutils.slist(t)
                    bk = mtutils._mungeKey(b,dm='values')
                    hasrule = False                                                 #      prepare to detect any triple with associated rule (inferable or not)
                    isrule = 0                                                      #      prepare to detect an inferable rule
                    # re-order retrieved triple elements into their stored sequence and test if any are rules
                    for c in range(3):                                              #      for each result triple element: re-order elements for yielding
                        self._showDebug(clas='Query',method='_solve',line=2561,level=2,vars=[['c',c],['cols',cols],['rd',rd]])
                        if cols[c] == '?': hasrule = True                           #       check if it has an associated rule
                        if (not infer
                         or cols[c] in rpreds                                       #        or a reserved predicate (since makeKey only minimises rule searches
                            ): isrule = None                                        #         for these): if so prevent feed forward inference
                        elif (isrule is not None                                    #       otherwise it might be a rule...
                          and i[c]
                          and cols[c] == '?'                                        #        unnamed rule variable found
                            ): isrule += 1                                          #        : this result is a rule so increment rule variable count in isrule
                    self._showDebug(clas='Query',method='_solve',line=2570,level=1,vars=[['cols',cols],['b',b],['isrule',isrule],['akey',akey]])
                    self._showDebug(clas='Query',method='_solve',note='summary',line=2571,level=1,vars=[['     Found',cols]])
                    self._showDebug(clas='Query',method='_solve',note='summary',line=2572,level=1,vars=[['   Unified',b]])
                    # result has associated rule - so check if it needs to be merged with others from nested stores.
                    # remember to re-order lhs/rhs triples for source or parentStore as required
                    if hasrule:                                                     #      if an associated rule: (proceed to ensure it can be reported)
                        try:                                                        #       try to access/merge rule:
                            for qc,qsi in enumerate(qs):                            #        foreach source querystore with this rule:
                                if qsi == store: scols = cols                       #         if source and parentStores same: source cols are cols
                                else: scols = qsi._rt(cols
                                                     ,order=store._getTripleOrder()
                                                      )                             #         else: source cols must be ordered for source store
                                id = qsi._getIDfromTriple(scols)                    #         get the source triple id with lhs of source cols
                                nrule = qsi._db['i>r'][id]                          #         new rule is rule indexed by this triple id
                                if qc:                                              #         if not the sole source store:
                                    rule._mergeRhs(nrule=nrule._rtClone(qsi,store)) #          merge new rule (ordered for parentStore) into existing rule
                                else:                                               #         else 1st source (and maybe sole source):
                                    rule = nrule                                    #          get existing rule from 1st source
                                    if qsi == store: id1 = id                       #          if query store (qsi) == store: id is the query store id
                                    else:                                           #          else different query store: (get rule id for this store)
                                        id1 = store._getIDfromTriple(cols)          #           get this rule triple id for this store
                                        id_to_rules = store._db['rs']._db['i>r']    #           get id_to_rules dict for this store (from its results store)
                                        if id1 in id_to_rules:                      #           if this store knows about this rule:
                                            rule = id_to_rules[id1]                 #            get the rule from this store
                                            break                                   #            and break
                                        else:                                       #           else: (this rule is new to this store)
                                            rule = rule._rtClone(qsi,store          #            get rule by re-ordering lhs/rhs triples for parentStore
                                                                ,new=True           #            or if triple ordering is unchanged make a new copy
                                                                 )
                                            id_to_rules[id1] = rule                 #            and add it to this stores rules index
                            self._showDebug(clas='Query',method='_solve',line=2600,level=2,vars=[['len(qs)',len(qs)],['id',id],['id1',id1]])
                            self._showDebug(clas='Query',method='_solve',note='summary',line=2601,level=1,vars=[['   is Rule',rule._express()]])
                        except: isrule = 0                                          #       except can't access or merge rule: so handle as data
                    # result has an associated rule which is to be evaluated (ie. isrule = True)
                    if isrule:                                                      #      if a rule: (proceed to infer the rule)
                        if skiprules: continue                                      #       omit remaing rules?
                        if (store._getFFImaint() == 0                               #       if fully maintained feed forward inference
                        and infer != 'ffi'                                          #        being used rather than built
                            ): cut = True                                           #        : cut inference
                        else:                                                       #       else:
                            cut = False                                             #        proceed with inference
                            # prepare inference cache keys. Different keys for successes|failures, generic|non-generic, and logical|physical entries
                            ik1 = (iqid,id1)                                        #        physical inference key (Query id plus merged rule id)
                            if ixb: ikf = iks = []                                  #        if inferable query has extra bindings: avoid cache
                            else:                                                   #        else: prepare keys to maintain/access it
                                if gr:                                              #         if generic rule:
                                    iks = [iqid,ik1]                                #          raw rule success keys list [logical,physical]
                                    ikf = [iqid,ik1]                                #          raw rule failure keys list [logical,physical]
                                else:                                               #         else a non generic rule:
                                    iks = [ik0,ik1]                                 #          raw rule success keys list [logical,physical]
                                    ikf = [ik0,ik1]                                 #          raw rule failure keys list [logical,physical]
                                iks = [ik for ik in iks[:mtoc]]                     #        finalise rule success keys list to cache depth
                                ikf = [ik for ik in ikf[:mtoc]]                     #        finalise rule failure keys list to cache depth
                            self._showDebug(clas='Query',method='_solve',line=2623,level=2,vars=[['iks',iks],['done',done]])
                            # but check if its already been evaluated
                            store._incMetric('rl')                                  #        metrics: increment rules counter
                            gr1 = None                                              #        assume this isn't a generic rule
                            if id1 in done: cut = True                              #        if this query has already run this rule: cut
                            else:                                                   #        else:
                                self._showDebug(clas='Query',method='_solve',line=2629,level=2,vars=[['cut',cut]])
                                for tmp,ik in enumerate(ikf):                       #         if any rule keys (logical or physical)
                                    cut = crf[tmp]._getItem(ik)                     #          have previously failed: cut
                                    if cut:                                         #          if cut
                                        if not tmp: skiprules = True                #           and logical key failure skip any remaining rules
                                        break                                       #           break failure check
                                self._showDebug(clas='Query',method='_solve',line=2635,level=2,vars=[['ikey',ikey],['ik1',ik1],['rikeys',rikeys]])
                        self._showDebug(clas='Query',method='_solve',line=2636,level=2,vars=[['cut',cut]])
                        self._showDebug(clas='Query',method='_solve',line=2637,level=2,vars=[['isrule',isrule]])
                        if cut: store._incMetric('br')                              #       if cut: metrics: increment blocked rules counter
                        elif ik1 in rikeys:                                         #       elif this inference already run in this context
                            cut = True                                              #         cut
                            store._incMetric('brgr')                                #         metrics: increment blocked generic rules counter
# 25/06/2010 restored section - prevents inference loops - think it was commented out for performance at no apparant functionality cost
#                        elif ik1 in rikeys: cut = True                              #       elif 1st order logic loops: cut
# end restored section
                        self._showDebug(clas='Query',method='_solve',line=2645,level=2,vars=[['cut',cut]])
                        if not cut:                                                 #       if rule needs evaluating:
                            # try yielding rule results from cache
                            self._showDebug(clas='Query',method='_solve',line=2648,level=2,vars=[['id',id],["qsi._db['i>r']",qsi._db['i>r']]])
                            ires = []                                               #        default infered cached results setting
                            for tmp,ik in enumerate(iks):                           #        check if any inference keys have succeeded
                                ires = crs[tmp]._getItem(ik)                        #         getting associated cached results
                                if ires:                                            #         if cached inference results:
                                    if not tmp: skiprules = True                    #          from a logical key: skip any remaing rules
                                    break                                           #          break infered cached results check
                            # yield rule results from cache
                            upd = False                                             #         prepare to update rule processing cache
                            ird = None                                              #         default inference caching data
                            if iks:
                                ird = store._prcache._getItem(ik0)                  #         get infered result data (on caching of this rule)
                                if ires:                                            #         if cached results found: (use them)
                                    cut = True                                      #          cut evaluation of this rule
                                    for [tl,rl,b] in ires.values():                 #          for each cached rule result:
                                        self._showDebug(clas='Query',method='_solve',note='summary',line=2663,level=1,vars=[['Cached Infered   Found',tl]])
                                        self._showDebug(clas='Query',method='_solve',note='summary',line=2664,level=1,vars=[['Cached Infered Unified',b]])
                                        self._showDebug(clas='Query',method='_solve',note='summary',line=2665,level=1,vars=[['Cached Infered      rl',rl]])
                                        bk = mtutils._mungeKey(b,dm='values')
                                        if ird is None or rd == ird[0]:
                                            ires0._isUnique(bk,default=[tl,rl,b])    #           add it if new to the logical cached results
                                        if result():                                #           if result is unique for purpose (incl cache update):
                                            self._showDebug(clas='Query',method='_solve',note='summary infered cache yields',line=2670,level=0,vars=[['tl',tl],['rl',rl],['b',b]])
                                            yield tl,rl,b                           #            yield aggregate results
                                else:                                               #         elif no cached results but caching on:
                                    if ird is None:                                 #          if none:
                                        ird = [rd,mtutils.sdict()]                  #           initialise new cache data
                                        upd = True                                  #           and flag for update
                                    if len(iks) > 1 and ik1 not in ird[1]:          #          if physical caching on and physical key not cached:
                                        ird[1][ik1] = rd                            #           add it to cache data
                                        upd = True                                  #           and flag for update
                        if not cut:
                            # evaluate this rule
                            if upd: store._prcache._setItem(ik0,ird)                #         update progressing rule cache
                            self._showDebug(clas='Query',method='_solve',note='invoking rule',line=2682,level=1,vars=[['ikey',ikey],['rikeys',rikeys],['id',id],['cols',cols]])
                            done[id1] = ''                                          #         block rule from further use by this query
                            rikeys1 = copy.copy(rikeys)                             #         index it in a new recursed keys dictionary
                            rikeys1[ik1] = ''                                       #         add query key to recursed keys
                            if isrule == 3:
                                gr1 = True
                                store._incMetric('gr')                      #          metrics: increment OK recursive generic rule counter
                            self._showDebug(clas='Query',method='_solve',line=2689,level=2,vars=[['rule',rule]])
                            ires1 = mtindex.Index()                                 #         initialise physical rule results index
                            for tl,rl,b in rule._solve(iquery
                                                      ,gr=gr1
                                                      ,rikeys=rikeys1
                                                      ,store=store
                                                      ,rd=rd+1
                                                      ,infer=infer
                                                       ):                           #          get triples, rules and bindings solving the rule
                                # prepare to yield rule results in terms of variables expressed in this query
                                rl = rl._union([tuple(cols)])                       #          collating rules used
                                self._showDebug(clas='Query',method='_solve',note='summary',line=2700,level=1,vars=[['New    Infered   Found',tl]])
                                self._showDebug(clas='Query',method='_solve',note='summary',line=2701,level=1,vars=[['New    Infered Unified',b]])
                                self._showDebug(clas='Query',method='_solve',note='summary',line=2702,level=1,vars=[['New    Infered      rl',rl]])
                                bk = mtutils._mungeKey(b,dm='values')
                                if (ires1._isUnique(bk
                                                   ,default=[tl,rl,b]
                                                   ,munge=False
                                                    )                               #          if new physical data cached:
                                and ird and rd == ird[0]
                                    ): ires0._isUnique(bk
                                                      ,default=[tl,rl,b]
                                                      ,munge=False
                                                       )                            #           cache new logical data
                                if result():                                        #          if result is unique for purpose (incl cache update):
                                    self._showDebug(clas='Query',method='_solve',note='summary yields',line=2714,level=0,vars=[['tl',tl],['rl',rl],['b',b]])
                                    yield tl,rl,b                                   #           yield aggregate results
                                if isBoolean: break                                 #          if just this result needed: break
                            # update intermeadiate rule results using physical keys
                            if ires1._isEmpty(): store._incMetric('fr')             #         metrics: increment failed (NA) rule counter
                            if len(iks) > 1 and rd == ird[1][ik1]:                  #         elif completed physical rule to be cached:
                                if ires1._hasItems():                               #          if associated results:
                                    crs[1]._getMember(ik1
                                                     ,default=ires1
                                                     ,munge=False
                                                      )                             #           cache indexed by physical key
                                elif not crf[1]._getMember(ik1
                                                          ,default=1
                                                          ,munge=False
                                                           ):                       #          elif rule failure not yet cached: add it
                                    store._incMetric('ufr')                         #           metrics: increment unique failed rule counter
                    # result has no associated rule - prepare to yield unique results
                    else:                                                           #      else its a fact:
                        tl = tuple(cols)                                            #       convert triple to tuple
                        rl = []
                        self._showDebug(clas='Query',method='_solve',note='summary',line=2734,level=1,vars=[['New    Results   Found',tl]])
                        self._showDebug(clas='Query',method='_solve',note='summary',line=2735,level=1,vars=[['New    Results Unified',b]])
                        self._showDebug(clas='Query',method='_solve',note='summary',line=2736,level=1,vars=[['New    Results      rl',[]]])
                        if result():                        #       if result is unique for purpose (incl cache update):
                            self._showDebug(clas='Query',method='_solve',note='summary yields',line=2738,level=0,vars=[['tl',tl],['rl',[]],['b',b]])
                            yield tl,rl,b                                           #        yield aggregate results (triples, rules and bindings)
                    if isBoolean:                                                   #      if just this result needed:
                        break                                                       #       search no further
                # no more results for this query at this recursion depth - update results caches and metrics
                # 1st update logical rules caches (now all rule results are in)
                if mtoc and not ixb:                                                            #     if caching:
                    ird = store._prcache._getItem(ik0)                              #      get progress data for this rule (if any)
                    if ird and rd == ird[0]:                                        #      if query outcomes are logically completing:
                        for ik1 in ird[1]:                                          #       delete all physically keyed inference cache data
                            crf[1]._delItem(ik1)                                    #        for failures
                            crs[1]._delItem(ik1)                                    #        for successes
                        store._prcache._delItem(ik0)                                #       and delete this query progress data
                        if ires0._hasItems():                                       #       if query produced logically keyed inferred results:
                            if iks[0] not in crs[0]._items:
                                if gr:
#                                    print ('caching OK rule: key=',iks[0],self._selectQid(iks[0])._expandMatch(),'val=',ires0._items)
                                    if ikf[0] in crf[0]._items:
#                                        print ('deleting bad rule: key=',ikf[0])
                                        crf[0]._delItem(ikf[0])
#                                else: print ('caching OK rule: key=',iks[0],'val=',ires0._items)
                                crs[0]._setItem(iks[0],ires0)
#                            crs[0]._getMember(iks[0],default=ires0,munge=False)        #        cache them now
                        else:
                            if ikf[0] not in crf[0]._items:
#                                print ('caching bad rule: key=',ikf[0])
                                crf[0]._setItem(ikf[0],1)
#                            crf[0]._getMember(ikf[0],default=1,munge=False)          #       else cache logically keyed inference failure
                # 2nd update results caches of successful and failed query results
                if abdi._hasItems():                                                #     if aggregate results produced:
                    store._incMetric('qc')                                          #      metrics: increment OK query counter
                    self._showDebug(clas='Query',method='_solve',note='U OK query/results',line=2769,level=1,vars=[['akey',akey],['b',b]])
                    store._incMetric('usqkey')                                      #      metrics: increment unique successful query akey counter
                    lr = len(abdi)                                                  #      get number of unique aggregate results
                    if lr > store._getMetric('maxrc'):                              #      if a new maximum:
                        store._setMetric('maxrc',lr)                                #       metrics: update largest cached result size
                        store._setMetric('qkeymax',akey)                            #       metrics: store associated query akey
                    if isBoolean:                                                   #      get OK boolean query metrics
                        store._incMetric('sbq')                                     #       metrics: increment successful boolean query counter
                        if store._sbqcache._isUnique(ak0,default=1,munge=False):    #       if not already cached: (cache it)
                            store._incMetric('usbq')                                #        metrics: increment unique successful boolean query counter
                    else: store._incMetric('snbq')                                  #      else: metrics: increment unique successful non boolean query counter
                else:                                                               #     else: no aggregate results produced
                    store._incMetric('fq')                                          #      metrics: increment failed query counter
                    if (mtoc                                                        #      if caching
                    and not axb and ard == rd                                       #       and no supplementary bindings influencing results
                    and not store._db['cqs']._getItem(ak0)                          #       and aggregate query hasn't succeeded elsewhere
                        ):                                                          #       :
                        if store._db['cqf']._isUnique(ak0,default=1,munge=False):   #       cache its failure and if not already done:
                            store._incMetric('ufq')                                 #        metrics: increment unique failed query counter
                            self._showDebug(clas='Query',method='_solve',note='summary',line=2788,level=1,vars=[['cache failure key',ak0],['rd',rd]])
        except mterrors.QueryElementInterpolationError, X:                          #  except propogated InterpolationError:
            pass                                                                    #   end without solving Query

class QueryList(Queryable):
    def __init__(self,lhs='',vars=[],match='',rs=None,rrs=None,pOK=True):
        Queryable.__init__(self,lhs=lhs,vars=vars,match=match,rs=rs,rrs=rrs,pOK=pOK)
    def _setLhs(self,lhs):
        # usage:
        #    overrides Queryable._setLhs() since this inputs its output
        #    therefore no need to run again
        self._lhs = lhs
        return self._lhs
    def _setVars(self,vars):
        if isinstance(vars,list): self._vars = sorted(vars)
        return self._vars
    def _getVars(self):    return self._vars
    def _setPolarity(self,p):
        if p is True: p = 1
        elif p is False: p = -1
        if p == 1 or p == -1: self._polarity = p
        return self._polarity
    def _getPolarity(self):
        self._showDebug(clas='QueryList',method='_getPolarity',line=2811,note='returns',level=0,vars=[['self._polarity',self._polarity]])
        return self._polarity
    def _setRecursive(self,r):
        if r is True: r = 1
        elif r is False: r = -1
        if r == 1 or r == -1: self._recursive = r
        self._showDebug(clas='QueryList',method='_setRecursive',line=2817,note='returns',level=0,vars=[['self._recursive',self._recursive]])
        return self._recursive
    def _getRecursive(self): return self._recursive
    def _isRecursive(self):
        if self._reduceVars(self._expandMatch()) == self._getLhs():                 # strip its vars and compare with the lhs
            r = True                                                                #  if same: its recursive
        else: r = False                                                             #  else: its not recursive
        self._showDebug(clas='QueryList',method='_isRecursive',line=2824,level=1,vars=[['self._getLhs()',self._getLhs()],['self._reduceVars(self._expandMatch())',self._reduceVars(self._expandMatch())]])
        self._showDebug(clas='QueryList',method='_isRecursive',line=2825,note='returns',level=0,vars=[['r',r]])
        return r
    def _setMatch(self,match=None,rs=None,rrs=None,pOK=True):
        self._showDebug(clas='QueryList',method='_setMatch',note='inputs',line=2828,level=0,vars=[['match',match],['rs',rs],['rrs',rrs],['pOK',pOK]])
        self._rs  = rs
        self._rrs = rrs
        self._pOK = pOK
        if not match:
            match = [(wkqe,wkqe,wkqe)]                                              # set default match if None
            self._showDebug(clas='QueryList',method='_setMatch',line=2834,level=1,vars=[['match',match]])
        m = mtutils.slist()
        error = 0
        if isinstance(match,tuple): m += [match]
        elif isinstance(match,list):
            if match[0] in l_ne:                                                    # if 1st element of list is NOT polarity indicator:
                match = match[1:]                                                   #  delete from match
                polarity = -1
            else: polarity = 1
            self._setPolarity(polarity)                                             #  set polarity to -1
            self._showDebug(clas='QueryList',method='_setMatch',line=2844,level=1,vars=[['self',self]])
            self._showDebug(clas='QueryList',method='_setMatch',line=2845,level=1,vars=[['self._getPolarity()',self._getPolarity()]])
            for c,web in enumerate(match):
                if isinstance(web,Query): m += [web]
                else:
                    m[c] = Queryable._getUnique(Query(match=web,rs=rs,rrs=rrs,pOK=pOK))
                    if not m[c]: error = 1
        elif isinstance(match,basestring): error = 1
        if not error:
            self._match = m
            self._showDebug(clas='QueryList',method='_setMatch',note='returns',line=2854,level=0,vars=[['m',m]])
            self._showDebug(clas='QueryList',method='_setMatch',note='returns',line=2855,level=0,vars=[['self._expandMatch()',self._expandMatch()]])
            self._setRecursive(self._isRecursive())
            return self._match
        elif error == 1: raise mterrors.QueryListFormatError(match)
        return 0
    def _getMatch(self,ordered=True):
        # usage:
        #    retrieves list of Query objects forming the QueryList
        #    optional ordering (by default) ensures QueryLists can be compared which is required
        #     for deciding if an newly asserted Equation duplicates an existing one used by stores._actionEntry()
        ordered = mtutils._logical(ordered)
        self._showDebug(clas='QueryList',method='_getMatch',note='inputs',line=2866,level=0,vars=[['self',self],['ordered',ordered]])
        match = self._match
        if ordered:
            self._showDebug(clas='QueryList',method='_getMatch',line=2869,note='1)',level=1,vars=[['match',match]])
            match1 = []
            for m in match:
                self._showDebug(clas='QueryList',method='_getMatch',line=2872,level=0,vars=[['m',m]])
                match1 += [[m,str(m._expandMatch())]]
            self._showDebug(clas='QueryList',method='_getMatch',line=2874,note='2)',level=1,vars=[['match1',match1]])
            match1.sort(key=itemgetter(1))
            self._showDebug(clas='QueryList',method='_getMatch',line=2876,note='3)',level=1,vars=[['match1',match1]])
            match = mtutils.slist(map(itemgetter(0),match1))
        self._showDebug(clas='QueryList',method='_getMatch',line=2878,note='returns',level=0,vars=[['match',match]])
        return match
    def _getRs(self): return self._rs
    def _getRrs(self): return self._rrs
    def _getPOK(self): return self._pOK
    def _getLvals(self): return self._getMatch()
    def _solve(self,store,vs={},rs={},gr=None,rikeys=None,infer=None,eq='None',eql='None',rd=None):
        # usage:
        #    solves QueryLists - that is a set of alternative Queries either for triples matches or rules
        # inputs:
        #    store    - TripleStore
        #    vs       - variable substitution dict (for rule interpretation only)
        #    rs       - return substitutions dict  (for rule interpretation only - local but not nested variables)
        #    gr       - generic rule identifier (if applicable)
        #    rikeys   - recursed infered keys
        #    infer    - Infer missing facts from rules. [None|True|False|'ffi'].
        #                If None uses config item 'stores_infer' instead.
        #                _export() sets infer to False via _triples().
        #    eq       - unique id of source Equation
        #    eql      - unique id of source EquationList
        #    rd       - current recursion depth (recursive inference)
        # yields:
        #    triples, rules and bindings from _solveQuery tuple by tuple
        self._showDebug(clas='QueryList',method='_solve',note='inputs',line=2901,level=0,vars=[['store',store],['gr',gr]])
        self._showDebug(clas='QueryList',method='_solve',note='inputs',line=2902,level=0,vars=[['self',self]])
        self._showDebug(clas='QueryList',method='_solve',note='inputs',line=2903,level=0,vars=[['_expandVS(vs)',_expandVS(vs)],['vs',vs]])
        self._showDebug(clas='QueryList',method='_solve',note='summary',line=2904,level=1,vars=[['   Queries',self._expandMatch(thin=True)]])
        iq_results = mtindex.Index()
        if not vs: store._newQL_luw()                                               # if not a linked query start a new luw
        for query in self._getMatch():                                              # for each Query object in this QueryList:
            for t,r,b in query._solve(store
                                     ,vs=vs
                                     ,rs=rs
                                     ,gr=gr
                                     ,rikeys=rikeys
                                     ,infer=infer
                                     ,ql=self._getQid()
                                     ,eq=eq
                                     ,eql=eql
                                     ,rd=rd
                                      ):                                            #  for each triples, rules and bindings Query solution
                self._showDebug(clas='QueryList',method='_solve',line=2919,level=1,vars=[['t',t],['r',r],['b',b]])
                if b: k = b                                                         #   get q_results cache key from either returned bindings (if present)
                else: k = t                                                         #    or triples
                unique = iq_results._isUnique(k,default=1)                          #   check and update uniqueness of this result
                if unique:                                                          #   if unique:
                    self._showDebug(clas='QueryList',method='_solve',note='yields',line=2924,level=0,vars=[['t',t],['r',r],['b',b]])
                    yield t,r,b                                                     #    yield solving triples, rules and bindings
                else: store._incMetric('bdql')                                      #   else: metrics: increment blocked duplicate QueryList result count
    def _getTIDB(self,store,vars=None,rd=None,infer=None,rs={}):
        # Usage:
        #    get triple id bindings solving self - bindings indexed by ids of triples solving self
        #    specifically towards intermedeate unification of nested triple queries
        # Inputs:
        #    store       - parent TripleStore possibly DTS
        #    vars        - external variables list to be bound to results
        #    rd          - recursion depth for passing on
        #    infer       - Infer missing facts from rules. [None|True|False|'ffi'].
        #    rs       - return substitutions dict  (for rule interpretation only - local but not nested variables)
        # Returns:
        #    tidb        - matching bindings indexed by triple ids
        # Note: op may be !=
        #        not handled yet
        self._showDebug(clas='QueryList',method='_getTIDB',note='summary inputs',line=2941,level=0,vars=[['store',store],['vars',vars],['rd',rd],['infer',infer]])
        self._showDebug(clas='QueryList',method='_getTIDB',note='summary inputs',line=2942,level=0,vars=[['self._expandMatch()',self._expandMatch()]])
        if mtoc > 1:                                                            # if intermeadiate outcomes being cached: (try accessing)
            try: return self._tidb                                              #  try returning cached result
            except AttributeError: pass                                         #  except nothing cached: (proceed to derive result)
        # augment query with system selection variables                         # (derive them)
        bvs = ['!mtsub','!mtpred','!mtobj']                                     # introduce system selection variables
        nql = []                                                                # initialise new QueryList
        for q in self._getMatch():                                              # for each Query in the QueryList:
            nq = []                                                             #  initialise new Query
            for c,qelm in enumerate(q._getMatch()):                             #  for each enumerated QueryElement in Query:
                nqelm = []                                                      #   initialise new QueryElement
                for qexp in qelm._getMatch():                                   #   for each QueryExpression in QueryElement:
                    nvars = qexp._getVars()+[bvs[c]]                            #    append corresponding selection variable to variables
                    nqelm += [qexp._modifiedClone(vars=nvars)]                  #    collate newly instantiated Query Expression as new QElm
                nq += [nqelm]                                                   #   collate new QueryElements into new Query
            nql += [tuple(nq)]                                                  #  collate new Query's into new QueryList
        nql = Queryable._getUnique(QueryList(match=nql,vars=vars))              # instantiate the new QueryList
        tidb = mtutils.sdict()                                                  # initialise new dictionary for found
        for t,r,b in nql._solve(store,rd=rd,infer=infer):                       # for each resultant triple and bindings - if any
            tid = store._getIDfromTriple((b[bvs[0]],b[bvs[1]],b[bvs[2]]))       #  get the id for the selected triple
            for bv in bvs: del b[bv]                                            #  remove system selection variables from result bindings
            if vars:                                                            #  if external variables: (bind these to the result)
                for var in vars:                                                #   for each external variable:
                    if var not in b: b[var] = tid                               #    if its not in b: bind it to the result triple_id
            self._showDebug(clas='QueryList',method='_getTIDB',line=2966,note='summary',level=2,vars=[['t',t],['b',b],['r',r]])
            # identify uniquely internal nested variables
            if rs:
                for bv in b:
                    if bv not in rs:
                        b['!*'+bv] = b[bv]
                        del b[bv]
            tidb[tid] = b                                                       #  index bindings by returned triple id in tidb
        if mtoc > 1: self._tidb = tidb                                          # if intermeadiate outcomes being cached: cache these
        self._showDebug(clas='QueryList',method='_getTIDB',note='returns',line=2975,level=0,vars=[['tidb',tidb]])
        return tidb                                                             # return nested triple id bindings

class Equation(Queryable):
    def __init__(self,match='',rs=None,rrs=None,pOK=True):
        Queryable.__init__(self,match=match,rs=rs,rrs=rrs,pOK=pOK)
    def _setMatch(self,match=None,rs=None,rrs=None,pOK=True):
        if not match: match = [[(wkqe,wkqe,wkqe)]]                                  # set default match if None
        self._showDebug(clas='Equation',method='_setMatch',note='inputs',line=2983,level=0,vars=[['match',match],['rs',rs],['rrs',rrs],['pOK',pOK]])
        m = mtutils.slist()
        error = 0
        if not isinstance(match,list): error = 1
        else:
            logical = False
            for c,webs in enumerate(match):
                if isinstance(webs,QueryList):
                    m += [webs]
                    logical = True
                else:
                    m[c] = Queryable._getUnique(QueryList(match=webs,rs=rs,rrs=rrs,pOK=pOK))
                    if not m[c]: error = 1
                    self._showDebug(clas='Equation',method='_setMatch',line=2996,level=2,vars=[['c',c],['m[c]',m[c]],['m[c]._getPolarity()',m[c]._getPolarity()]])
                    if m[c]._getPolarity() > 0: logical = True
            self._showDebug(clas='Equation',method='_setMatch',line=2998,level=1,vars=[['match',match],['logical',logical]])
            if not logical: raise mterrors.EquationLogicError()
        if not error:
            self._showDebug(clas='Equation',method='_setMatch',note='returns',line=3001,level=0,vars=[['m',m]])
            self._match = m
            return self._match
        elif error == 1: raise mterrors.EquationFormatError()
        return 0
    def _getMatch(self,ordered=True):
        # usage:
        #    returns list of QueryLists optionaly sorted with:
        #    1. recursive last
        #    2. NOT polarities last
        #    required in this order by _solve()
        # input:
        #    ordered - optional. Set to false to behave like default _getMatch() else orders as above
        # returns:
        #    [QueryList1,..,QueryListn] optionally sorted with NOT polarities last
        ordered = mtutils._logical(ordered)
        self._showDebug(clas='Equation',method='_getMatch',note='inputs',line=3017,level=0,vars=[['ordered',ordered]])
        if not ordered:                                                             # if unordered:
            self._showDebug(clas='Equation',method='_getMatch',note='returns',line=3019,level=0,vars=[['self._match',self._match]])
            return self._match                                                      #  return self._match as is
        else:                                                                       # else: (prepare to check)...
            l = mtutils.slist()                                                                  #  initialise ordered Equation
            for m in self._getMatch(ordered=False):                                 #  itemize its contents:
                l += [[m,m._getRecursive(),m._getPolarity()]]                       #   by QueryLists, their recursion and polarity
            if l:                                                                   #  if itemised content exists:
                self._showDebug(clas='Equation',method='_getMatch',note='pre sort',line=3026,level=1,vars=[['l',l]])
                l.sort(key=itemgetter(2),reverse=True)                              #   sort by reverse polarity (lowest priority)
                l.sort(key=itemgetter(1))                                           #   sort by recursion        (highest priority)
                self._showDebug(clas='Equation',method='_getMatch',note='post sort',line=3029,level=1,vars=[['l',l]])
                if l[-1][1] > 0 and (l[0][2] < 0 or l[0][1] > 0): l = []            #   fail unterminated recursion (ie. if recursion unaccompanied by at least 1 positive non-recursive QueryList)
                else: l = mtutils.slist(map(itemgetter(0),l))                       #   else: OK extract just the ordered QueryLists
            self._showDebug(clas='Equation',method='_getMatch',note='returns',line=3032,level=0,vars=[['l',l]])
            return l
    def _solve(self
              ,store
              ,triples
              ,rules
              ,bindings
              ,qls=None
              ,vs={}
              ,rs={}
              ,gr=None
              ,rikeys=None
              ,eql='None'
              ,level=0
              ,rd=None
              ,infer=None
               ):
        # usage:
        #    solves an Equation
        # inputs:
        #    store    - triple store being queried
        #    qls      - lists of QueryLists. Ppointer into the next QueryList to be solved within the current equation
        #    triples  - the current set of contributory triples
        #    rules    - the current set of contributory rules
        #    bindings - bindings found local to scope of current rule/query
        #    vs       - variable substitution dict (for rule interpretation only)
        #    rs       - return substitutions dict  (for rule interpretation only - local but not nested variables)
        #    gr       - generic rule identifier (if applicable)
        #    rikeys   - recursed infered keys
        #    eql      - unique id of source EquationList
        #    level    - recursion depth for current invocation of this method
        #    rd       - current recursion depth (recursive inference)
        #    infer    - Infer missing facts from rules. [None|True|False|'ffi'].
        # yields:
        #    triples  - triples found contributing to current set of bindings
        #    rules    - rules found contributing to current set of bindings
        #    bindings - variable bindings for current solution in progress
        self._showDebug(clas='Equation',method='_solve',note='inputs',line=3069,level=0,vars=[['self',self]])
        self._showDebug(clas='Equation',method='_solve',note='inputs',line=3070,level=0,vars=[['store',store]])
        self._showDebug(clas='Equation',method='_solve',note='inputs',line=3071,level=0,vars=[['qls',qls]])
        self._showDebug(clas='Equation',method='_solve',note='inputs',line=3072,level=0,vars=[['triples',triples],['rules',rules],['bindings',bindings]])
        self._showDebug(clas='Equation',method='_solve',note='inputs',line=3073,level=0,vars=[['_expandVS(vs)',_expandVS(vs)],['vs',vs]])
        self._showDebug(clas='Equation',method='_solve',note='inputs',line=3074,level=0,vars=[['gr',gr],['level',level]])
        if not level and not qls:                                                   # if first entry and no qls:
            qls = self._getMatch()                                                  #  get qls = its list of QueryLists
        if qls:                                                                     # if qls contains QueryList(s):
            store._newEQ_luw()                                                      #  initialise equation LUW
            c = 0                                                                   #  count candidate matches
            polarity = qls[0]._getPolarity()                                        #  get QueryList polarity
            self._showDebug(clas='Equation',method='_solve',line=3081,level=1,vars=[['polarity',polarity]])
            self._showDebug(clas='Equation',method='_solve',line=3082,level=1,vars=[['qls',qls],['vs',vs]])
            self._showDebug(clas='Equation',method='_solve',line=3083,level=1,vars=[['qls[0]',qls[0]]])
            self._showDebug(clas='Equation',method='_solve',line=3084,level=1,vars=[['qls[0]._expandMatch(thin=True)',qls[0]._expandMatch(thin=True)],['polarity',polarity]])
            for t1,r1,b1 in qls[0]._solve(store
                                         ,vs=vs
                                         ,rs=rs
                                         ,gr=gr
                                         ,rikeys=rikeys
                                         ,eq=self._getQid()
                                         ,eql=eql
                                         ,rd=rd
                                         ,infer=infer
                                          ):                                        #  for each triple binding QueryList match:
                c += 1                                                              #   increment candidate match count
                self._showDebug(clas='Equation',method='_solve',line=3096,level=2,vars=[['triples',triples]])
                self._showDebug(clas='Equation',method='_solve',line=3097,level=2,vars=[['t1',t1]])
                self._showDebug(clas='Equation',method='_solve',line=3098,level=2,vars=[['rules',rules]])
                self._showDebug(clas='Equation',method='_solve',line=3099,level=2,vars=[['r1',r1]])
                self._showDebug(clas='Equation',method='_solve',line=3100,level=2,vars=[['bindings',bindings]])
                self._showDebug(clas='Equation',method='_solve',line=3101,level=2,vars=[['b1',b1]])
                b = copy.copy(bindings)                                             #   copy inherited bindings
                b = b._matchUnion(b1,                                               #   unify new with inherited bindings
                                  polarity=polarity)                                #    subject to polaity
  #              print ('EQ._solve: 1. polarity=',polarity,'QL._expandMatch=',qls[0]._expandMatch())
  #              print ('EQ._solve: 2. bindings=',bindings)
  #              print ('EQ._solve: 2.       b1=',b1)
  #              print ('EQ._solve: 3.        b=',b)
                self._showDebug(clas='Equation',method='_solve',line=3109,level=2,vars=[['b',b]])
                # proceed to next condition (represented by next QueryList) if this condition:
                #  +ve and binding values agree or
                #  -ve and binding values disagree
                if b or (not b1 and not bindings):                                  #   if bindings unification ok:
                    if not isinstance(t1,list): t1 = [t1]                           #   unify the contributory triples
                    triples = triples._union(t1)                                    #    - as a list of triples
                    if not isinstance(r1,list): r1 = [r1]                           #   unify the contributory rules
                    rules = rules._union(r1)                                        #    - as a list of rules
                    self._showDebug(clas='Equation',method='_solve',line=3118,level=2,vars=[['level',level],['qls[0]',qls[0]]])
                    self._showDebug(clas='Equation',method='_solve',line=3119,level=2,vars=[['triples',triples]])
                    self._showDebug(clas='Equation',method='_solve',line=3120,level=2,vars=[['rules',rules]])
                    self._showDebug(clas='Equation',method='_solve',line=3121,level=2,vars=[['b',b]])
                    self._showDebug(clas='Equation',method='_solve',line=3122,level=2,vars=[['_expandVS(vs)',_expandVS(vs)],['vs',vs]])
                    # prepare to infer bindings from this to the next QueryList
                    # via the variable values substitution index (vs)
                    # to target its search
                    if not qls[1:]:                                                 #   yield now if no more QueryLists in qls
                        self._showDebug(clas='Equation',method='_solve',note='summary',line=3127,level=1,vars=[['bindings',b]])
                        self._showDebug(clas='Equation',method='_solve',note='yields',line=3128,level=0,vars=[['triples',triples]])
                        self._showDebug(clas='Equation',method='_solve',note='yields',line=3129,level=0,vars=[['rules',rules]])
                        self._showDebug(clas='Equation',method='_solve',note='yields',line=3130,level=0,vars=[['b',b]])
                        yield triples,rules,b
                    else:                                                           #   else: (prepare for next QueryList)
                        vs1 = copy.deepcopy(vs)                                     #   prepare infered bindings
                        for varname in b:                                           #    for each bound variable:
                            vs1['?'+varname] = [Queryable._getUnique(QueryExpression(vars=[varname],op='=',vals=[b[varname]])
                                                                     )]             #     bind inferred var value to varname
                        self._showDebug(clas='Equation',method='_solve',line=3137,level=2,vars=[['_expandVS(vs1)',_expandVS(vs1)],['vs1',vs1]])
                        for triples,rules,b in self._solve(store
                                                          ,triples
                                                          ,rules
                                                          ,b
                                                          ,qls=qls[1:]
                                                          ,vs=vs1
                                                          ,rs=rs
                                                          ,gr=gr
                                                          ,rikeys=rikeys
                                                          ,eql=eql
                                                          ,level=level+1            #   yield each triples, bindings solving
                                                          ,rd=rd
                                                          ,infer=infer
                                                           ):                       #    the next QueryList in this equation
                            self._showDebug(clas='Equation',method='_solve',note='summary',line=3152,level=1,vars=[['bindings',b]])
                            self._showDebug(clas='Equation',method='_solve',note='yields',line=3153,level=0,vars=[['triples',triples]])
                            self._showDebug(clas='Equation',method='_solve',note='yields',line=3154,level=0,vars=[['rules',rules]])
                            self._showDebug(clas='Equation',method='_solve',note='yields',line=3155,level=0,vars=[['b',b]])
                            yield triples,rules,b
#            if not c: print ('EQ getting: NOTHING')
            if not c and polarity < 0:                                              #  if no candidate matches found and negative polarity:
                if not qls[1:]:                                                     #   yield now if no more QueryLists in equation
                    self._showDebug(clas='Equation',method='_solve',note='summary',line=3160,level=1,vars=[['bindings',bindings]])
                    self._showDebug(clas='Equation',method='_solve',note='yields',line=3161,level=0,vars=[['triples',triples]])
                    self._showDebug(clas='Equation',method='_solve',note='yields',line=3162,level=0,vars=[['rules',rules]])
                    self._showDebug(clas='Equation',method='_solve',note='yields',line=3163,level=0,vars=[['bindings',bindings]])
                    yield triples,rules,bindings
                else:                                                               #   else: test next -ve condition (QueryList)
                    self._showDebug(clas='Equation',method='_solve',line=3166,level=2,vars=[['_expandVS(vs)',_expandVS(vs)],['vs',vs]])
                    for triples,rules,bindings in self._solve(store
                                                             ,triples
                                                             ,rules
                                                             ,bindings
                                                             ,qls=qls[1:]
                                                             ,vs=vs
                                                             ,rs=rs
                                                             ,gr=gr
                                                             ,rikeys=rikeys
                                                             ,eql=eql
                                                             ,level=level+1         #   yield each triples, bindings solving
                                                             ,rd=rd
                                                             ,infer=infer
                                                              ):                    #    the next QueryList in this equation
                        self._showDebug(clas='Equation',method='_solve',note='summary',line=3181,level=1,vars=[['bindings',bindings]])
                        self._showDebug(clas='Equation',method='_solve',note='yields',line=3182,level=0,vars=[['triples',triples]])
                        self._showDebug(clas='Equation',method='_solve',note='yields',line=3183,level=0,vars=[['rules',rules]])
                        self._showDebug(clas='Equation',method='_solve',note='yields',line=3184,level=0,vars=[['bindings',bindings]])
                        yield triples,rules,bindings                                #   yield from previous QueryList

class EquationList(Queryable):
    def __init__(self, match='',rs=None,rrs=None,pOK=True):
        Queryable.__init__(self,match=match,rs=rs,rrs=rrs,pOK=pOK)
    def _setMatch(self,match=None,rs=None,rrs=None,pOK=True):
        if not match: match = [[[(wkqe,wkqe,wkqe)]]]                                # set default match if None
        self._showDebug(clas='EquationList',method='_setMatch',note='inputs',line=3192,level=0,vars=[['match',match],['rs',rs],['rrs',rrs],['pOK',pOK]])
        ms = mtutils.slist()
        error = 0
        if not isinstance(match,list): error = 1
        else:
            for c,e in enumerate(match):
                if isinstance(e,Equation): ms += [e]
                else:
                    ms[c] = Queryable._getUnique(Equation(match=e,rs=rs,rrs=rrs,pOK=pOK))
                    if not ms[c]: error = 1
        if not error:
            self._match = ms
            self._showDebug(clas='EquationList',method='_setMatch',note='returns',line=3204,level=0,vars=[['self._match',self._match]])
            return self._match
        elif error == 1: raise mterrors.EquationListFormatError(match)
        return 0
    def _getMatch(self,ordered=True):
        # usage:
        #    retrieves list of QueryExpressions objects forming the QueryElement
        #    optional ordering (by default) ensures expanded QueryExpressions can be compared
        ordered = mtutils._logical(ordered)
        self._showDebug(clas='EquationList',method='_getMatch',note='inputs',line=3213,level=0,vars=[['self',self],['ordered',ordered]])
        match = self._match
        if ordered:
            self._showDebug(clas='EquationList',method='_getMatch',line=3216,note='1)',level=1,vars=[['match',match]])
            match1 = []
            for m in match:
                self._showDebug(clas='EquationList',method='_getMatch',line=3219,level=0,vars=[['m',m]])
                match1 += [[m,m._getQid()]]
            self._showDebug(clas='EquationList',method='_getMatch',line=3221,note='2)',level=1,vars=[['match1',match1]])
            match1.sort(key=itemgetter(1))
            self._showDebug(clas='EquationList',method='_getMatch',line=3223,note='3)',level=1,vars=[['match1',match1]])
            match = mtutils.slist(map(itemgetter(0),match1))
        self._showDebug(clas='EquationList',method='_getMatch',line=3225,note='returns',level=0,vars=[['match',match]])
        return match
    def _solve(self
              ,store
              ,bound=mtutils.sdict()
              ,vs={}
              ,rs={}
              ,mode='results'
              ,gr=None
              ,rikeys=None
              ,rd=None
              ,infer=None
               ):
        # usage:
        #    solves an EquationList
        #    direct calls for solving rules - ie from Rule._solve()
        # inputs:
        #    store  - triplestore to be accessed for solving queries
        #    bound  - if called from _import, input bindings to the solving and generation process
        #    vs     - variable substitution dict {solving_var1:[querying Qexp1.1_with_solving_var1,..,querying Qexp1.n_with_solving_var1],..}
        #    rs     - return substitutions dict  {solving_var1:[querying_var1.1,..querying_var1.n],..,solving_varN:[querying_varsN]}
        #             i.e. dict of local (not nested) querying variables indexed by solving variables
        #    mode   - label of results to yield:
        #             * results: yield everything in bindings including: bindings['!triples'|'!rules'|'!equations'|'!unique'...]
        #                - bindings['!triples']    - fact triples from which this result is derived
        #                - bindings['!rules']      - rules from which this result is derived
        #                - bindings['!queries']    - queries from which this result is derived
        #                - bindings['!equations']  - equations this result satisfies
        #                - bindings['!unique']     - True or False for uniqueness of this results variable bindings
        #                - bindings['variable']    - binding for a variable solving the equation
        #                                            (all returned indexed by variable name)
        #              * rule:    yield [triples,rules,bindings] - without uniqueness check
        #    gr     - generic rule identifier (if applicable)
        #    rikeys - recursed infered keys tracing recursive calls
        #    rd     - current recursion depth (recursive inference)
        #    infer  - Infer missing facts from rules. [None|True|False|'ffi'].
        # yields:
        #    results as a list of result types in the order specified in mode
        self._showDebug(clas='EquationList',method='_solve',note='inputs',line=3263,level=0,vars=[['self',self]])
        self._showDebug(clas='EquationList',method='_solve',note='inputs',line=3264,level=0,vars=[['store',store]])
        self._showDebug(clas='EquationList',method='_solve',note='inputs',line=3265,level=0,vars=[['bound',bound]])
        self._showDebug(clas='EquationList',method='_solve',note='inputs',line=3266,level=0,vars=[['_expandVS(vs)',_expandVS(vs)],['vs',vs]])
        self._showDebug(clas='EquationList',method='_solve',note='inputs',line=3267,level=0,vars=[['gr',gr]])
        try:                                                                        # try basic initialisation
            if not isinstance(store,mtstruct.A_TripleStore):                        #  get Query Store
                raise mterrors.SolutionQueryStoreError()                            #   or raise error
        except mterrors.SolutionError, X:
            X._notify(c='EquationList',
                      m='_solve()')                                                 # notify SolutionError
        if vs: mode = 'rule'                                                        #  double check mode based on vsr
        if mode == 'results':                                                       #  if solving results:
            store._newEQLR_luw(infer=infer)                                         #   initialise EQuationList Results LUW and
            qtrace._setItem('trace',mtutils.slist())                                #   initialise query trace
        store._newEQL_luw()                                                         #  initialise new EQuationList luw
        iq_results = mtindex.Index()                                                #  index of unique results
        self._showDebug(clas='EquationList',method='_solve',line=3280,level=2,vars=[['self._getMatch()',self._getMatch()]])
        for equation in self._getMatch(ordered=False):                              #  for each equation:
            self._showDebug(clas='EquationList',method='_solve',line=3282,level=2,vars=[['equation',equation],['bound',bound]])
            self._showDebug(clas='EquationList',method='_solve',line=3283,level=2,vars=[['_expandVS(vs)',_expandVS(vs)],['vs',vs]])
            triples = mtutils.slist()                                               #   initialise list of triples
            rules = mtutils.slist()                                                 #   initialise list of rules
            bindings = copy.deepcopy(bound)                                         #   initialise bindings
            for triples,rules,bindings in equation._solve(store
                                                         ,triples
                                                         ,rules
                                                         ,bindings
                                                         ,vs=vs
                                                         ,rs=rs
                                                         ,gr=gr
                                                         ,rikeys=rikeys
                                                         ,eql=self._getQid()
                                                         ,rd=rd
                                                         ,infer=infer
                                                          ):                        #   for each equation solution:
                unique = iq_results._isUnique(bindings,default=1)                   #    get uniqueness and updated results index
                if unique:                                                          #    results debug outputs
                    self._showDebug(clas='EquationList',method='_solve',note='ok 1',line=3301,level=2,vars=[['equation._expandMatch(thin=True)',equation._expandMatch(thin=True)]])
                    self._showDebug(clas='EquationList',method='_solve',note='ok 2',line=3302,level=2,vars=[['bindings',bindings]])
                    self._showDebug(clas='EquationList',method='_solve',note='ok 3',line=3303,level=2,vars=[['bound',bound]])
                    self._showDebug(clas='EquationList',method='_solve',note='ok 4',line=3304,level=2,vars=[['_expandVS(vs)',_expandVS(vs)],['vs',vs]])
                    self._showDebug(clas='EquationList',method='_solve',note='ok 5',line=3305,level=2,vars=[['rikeys',rikeys]])
                    dummy = 0                                                       #    incase debug lines get deactivated
                else:
                    self._showDebug(clas='EquationList',method='_solve',note='dup 1',line=3308,level=2,vars=[['equation._expandMatch(thin=True)',equation._expandMatch(thin=True)]])
                    self._showDebug(clas='EquationList',method='_solve',note='dup 2',line=3309,level=2,vars=[['bindings',bindings]])
                    self._showDebug(clas='EquationList',method='_solve',note='dup 3',line=3310,level=2,vars=[['bound',bound]])
                    self._showDebug(clas='EquationList',method='_solve',note='dup 4',line=3311,level=2,vars=[['_expandVS(vs)',_expandVS(vs)],['vs',vs]])
                    self._showDebug(clas='EquationList',method='_solve',note='dup 5',line=3312,level=2,vars=[['rikeys',rikeys]])
                    dummy = 0                                                       #    incase debug lines get deactivated
                if mode == 'results':                                               #    if results: (prepare final bindings)
                    queries = qtrace._getItem('trace',mtutils.slist())
                    qtrace._setItem('trace',mtutils.slist())                        #     re-initialise query trace for next result
                    if unique: store._incMetric('irs')                              #     if unique: metrics: increment OK intermediate Result count
                    else: store._incMetric('bdrs')                                  #     else: metrics: increment blocked duplicate Result count
                    self._showDebug(clas='EquationList',method='_solve',line=3319,level=2,vars=[['triples',triples]])
                    self._showDebug(clas='EquationList',method='_solve',line=3320,level=2,vars=[['rules',rules]])
                    self._showDebug(clas='EquationList',method='_solve',line=3321,level=2,vars=[['queries',queries]])
                    self._showDebug(clas='EquationList',method='_solve',line=3322,level=2,vars=[['bindings',bindings]])
                    self._showDebug(clas='EquationList',method='_solve',note='summary',line=3323,level=1,vars=[['bindings',bindings]])
                    results = copy.deepcopy(bindings)                               #     initialise results independent of bindings
                    results['!unique'] = unique                                     #     bind uniqueness
                    results['!triples'] = triples                                   #     bind contributary triples
                    results['!rules'] = rules                                       #     bind contributary rules
                    results['!queries'] = queries                                   #     bind contributary queries
                    results['!equations'] = equation._expandMatch(thin=True)        #     bind equations satisfied
                    self._showDebug(clas='EquationList',method='_solve',note='yields',line=3330,level=0,vars=[['results',results]])
                    yield results                                                   #     yield results
                else:                                                               #    else: (a rule)
                    if unique:                                                      #     if unique:
                        store._incMetric('irl')                                     #      metrics: increment OK intermediate Rule result count
                        yield [triples,rules,bindings]                              #      and yield unique rule result
                    else: store._incMetric('bdrl')                                  #     else: metrics: increment blocked duplicate Rule result count
        if mode == 'results':                                                       #  if results have delivered:
            store._showMetrics()                                                    #   store the query metrics
            store._resetFFI()                                                       #   check to update feed forward inference data
#            SuperQueryable._validateCaches(self)

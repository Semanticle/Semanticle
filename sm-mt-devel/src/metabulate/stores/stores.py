'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

supports ffi with no inference if ffi already built
supports FFI maintenance modes
source re-documented
NOTE: co-requisite to query_splitkeys_07.py

stores38.py Created on 06 Jan 2010
stores39.py Cloned from stores38.py on 25 Jan 2010
stores40.py Cloned from stores39.py on 29 Jan 2010
stores41.py Cloned from stores40.py on 04 Feb 2010
stores42.py Cloned from stores41.py on 26 Feb 2010
stores43.py Cloned from stores42.py on 13 Mar 2010
stores44.py Cloned from stores43.py on 18 Mar 2010
stores45.py Cloned from stores44.py on 21 Mar 2010
stores46.py Cloned from stores45.py on 28 Mar 2010
stores47.py Cloned from stores46.py on 30 Mar 2010
stores48.py Cloned from stores47.py on 12 Apr 2010
stores49.py Cloned from stores48.py on 19 Apr 2010
stores50.py Cloned from stores49.py on 29 Apr 2010
stores51.py Cloned from stores50.py on 12 May 2010
stores52.py Cloned from stores51.py on 06 Jun 2010
stores53.py Cloned from stores52.py on 12 Jun 2010
stores.py Cloned from stores53.py on 07 Jul 2010
Last Updated 23 Oct 2010

As stores50.py with:
    alias support moved from pref01.dat to alias01.dat

    Supports same e.g.:
#    rlt01 = mtrules.Result(equations=[[('  ?person1  ', "desc_of", '?person2')]])                               # pass
#    rlt01 = mtrules.Result(equations=[[(('?person1', 'from', 'Truro'), "child_of", '?person2')]])               # pass
#    rlt01 = mtrules.Result(equations=[[([('?person1', 'from', 'Truro')], "child_of", '?person2')]])             # pass
#    rlt01 = mtrules.Result(equations=[[(['?person1=eve','?person1=eve2'], "child_of", '?person2')]])            # pass
#    rlt01 = mtrules.Result(equations=[[(('?person1', 'from', 'Truro'), "desc_of", '?person2')]])                # pass
#    rlt01 = mtrules.Result(equations=[[([('?person1', 'from', 'Truro')], "desc_of", '?person2')]])              # pass
#    rlt01 = mtrules.Result(equations=[[('?person1', "desc_of", ('?person2','from','Truro'))]])                  # pass - nested Query
#    rlt01 = mtrules.Result(equations=[[('?person1', "desc_of", "('?person2','from','Truro')")]])                # pass - nested QueryExpression Query
#    rlt01 = mtrules.Result(equations=[[('?person1', "desc_of", ('?person2','from',['Truro','London']))]])       # pass - nested Query with QueryElement list
#    rlt01 = mtrules.Result(equations=[[('?person1', "desc_of", "('?person2','from',['London','Truro'])")]])     # pass - nested QueryExpression Query with QueryElement list
#    rlt01 = mtrules.Result(equations=[[('?person1', "desc_of", ('?person2','from','London|Truro'))]])           # pass - nested Query with QueryExpression list
#    rlt01 = mtrules.Result(equations=[[('?person1', "desc_of", "('?person2','from','London|Truro')")]])         # pass - nested QueryExpression Query with QueryExpression list
#    rlt01 = mtrules.Result(equations=[[(['?person1=eve','?person1=eve2'], "desc_of", '?person2')]])             # pass
#    rlt02 = mtrules.Result(equations=[[('eve', "desc_of", '?person2')]])                                        # pass
#    rlt02 = mtrules.Result(equations=[[(('ender', 'from', 'Truro'), "desc_of", '?person2')]])                   # pass
#    rlt02 = mtrules.Result(equations=[[(('ender|eddy', 'from', 'Truro'), "desc_of", '?person2')]])              # pass
#    rlt02 = mtrules.Result(equations=[[(('?person1', 'from', 'Truro'), "desc_of", '?person2')]])                # pass
#    rlt02 = mtrules.Result(equations=[[('eve', "desc_of", '?person2')]
#                                     ,[('?person2', "desc_of", 'alice')]])                                      # pass
#    rlt02 = mtrules.Result(equations=[[('eve', "des_of", '?person2')]
#                                     ,[('?person2', "des_of", 'alice')]])                                       # pass - syn of recursed rule
#    rlt02 = mtrules.Result(equations=[[('eve', "descr_of", '?person2')]
#                                     ,[('?person2', "descr_of", 'alice')]])                                     # pass - reversed syn of recursed rule
#    rlt02 = mtrules.Result(equations=[[('alice', "ancs_of", '?person2')]
#                                     ,[('?person2', "ancs_of", 'eve')]])                                        # pass - ant of recursed rule
#    rlt02 = mtrules.Result(equations=[[('alice', "ancsr_of", '?person2')]
#                                     ,[('?person2', "ancsr_of", 'eve')]])                                       # pass - reversed ant of recursed rule
#    rlt02 = mtrules.Result(equations=[[('alice', "anc_of", '?person2')]
#                                     ,[('?person2', "anc_of", 'eve')]])                                         # pass - ant of syn of recursed rule
#    rlt02 = mtrules.Result(equations=[[('alice', "ancestor1_of", '?person2')]
#                                     ,[('?person2', "ancestor1_of", 'eve')]])                                   # pass - syn of ant of recursed rule
#    rlt02 = mtrules.Result(equations=[[('alice', "ancestor2_of", '?person2')]
#                                     ,[('?person2', "ancestor2_of", 'eve')]])                                   # pass - syn of ant of syn of recursed rule
#    rlt02 = mtrules.Result(equations=[[('alice', "ancestor3_of", '?person2')]
#                                     ,[('?person2', "ancestor3_of", 'eve')]])                                   # pass - syn of syn of ant of syn of recursed rule
#    rlt04 = mtrules.Result(equations=[[('?sub=eve','?pred=child_of','?obj=dan')]])                              # pass
#    rlt04 = mtrules.Result(equations=[[("?sub='*'","?pred='*'","?obj='*'")]])                                   # pass
#    rlt04 = mtrules.Result(equations=[[('?sub="*"','?pred="*"','?obj="*"')]])                                   # pass
#    rlt04 = mtrules.Result(equations=[[('?sub="?"','?pred="?"','?obj="?"')]])                                   # FAIL - NO RULES RETURNED (MAYBE OK?)
#    rlt04 = mtrules.Result(equations=[[("?sub='?'","?pred='?'","?obj='?'")]])                                   # FAIL - NO RULES RETURNED (MAYBE OK?)
#    rlt04 = mtrules.Result(equations=[[('?sub=eve', "?pred=desc_of", '?obj=alice')]])                           # pass
#    rlt04 = mtrules.Result(equations=[[('?sub=?','?pred','?obj')
#                                      ,('?sub','?pred=?','?obj')
#                                      ,('?sub','?pred','?obj=?')]])                                             # pass - all inferences
#    rlt04 = mtrules.Result(equations=[[('?sub','?pred','?obj')]])                                               # pass
#    rlt04 = mtrules.Result(equations=[[('?sub','?pred','?obj')],['not',('?sub','child_of','dan')]])             # pass
#    rlt04 = mtrules.Result(equations=[[('?sub','?pred','?obj')],['not',('?sub','child_of','dan')]
#                                                               ,['not',('?sub','from','London')]])              # pass

10/01/2010:
    _actionTriple():
     - parses facts represented:
        - as Strings with(out) (un)quoted action
        - as lists of elements or
        - as a tuple of listed elements
     - returns detailed compiled list of results
    see updated _actionTriple() source documentation for examples and further details
    _actionEntry() optionally parses string predicates and exploits _actionTriple()
    _generator() generates:
     - facts as lhs tuples
     - rule as seperate predicates for each rhs equation
     - can optionally generate commented rules with invalid rhs's
    _import() exploits Flatfile._values() to extract source lines filtering comments

11/01/2010:
    _actionEntry() supports incremental assertion of rule lhs (equation at a time):
     - duplicates being tested,
     - exploiting Queryables._getMatch()/_expandMatch() default ordering
    _export()/_generate()/_generator() drops support for the following paramters:
     - forceaction
     - protocol

13/01/2010:
    _actionEntry() renamed _actionPredicate()
    _actionPredicate() exploits new Rule._mergeRhs() to merge rhs's

16/01/2010:
    Configurable Exception Handling - exploits mterrors

17/01/2010:
    _deleteTriples() supports bulk deletion of selected Entries matching a QueryList.
      These transmitted via string ids without prefixes.
    _deleteTriple() inputs either t=triple or id=id_string_without_pref
      (change to allow delete from id direct to improve performance of new _deleteTriples())
    _deleteID() inputs same as _deleteTriple() for same reason
      Also if deleted id is for a rule then it gets deleted from the id to rules index
    _addTriple() inputs optional t for compatibility with _deleteTriple() as invoked by _processTriple()

23/01/2010:
    _solveQuery():
      - detection of query element value expressions solvable by pre-indexed triple dicts improved
        (ie. actually examines the value expression components rather than rejecting anything with a variable expression)
      - also checks query result cardinality (based on the above)
        (any boolean queries, with result cardinalities of 0 or 1, now terminate processing immediately a result is yielded)
      - failed boolean query keys are cached and checked to avoid re-running

25/01/2010 stores39.py cloned from stores38.py with:
    _solveQuery():
      - fq/tscache implemented as global rather than singleton indexes
      - valre regex bug fix to eliminate extraction of variable values
      - isRule counts rule variables and if 3 sets isGenericRule=True
      - clauses of a generic rule cannot themselves directly invoke a generic rule (to prevent unbounded recursion)
      - isGenericRule passed to Rule._solve(), _solveTriple(), _solveTriple1(), _solveQueryList()

26/01/2010:
    _solveQuery():
      - valre regex further refined - excludes invalid quoting
    _solveQueryList() and _solveQuery():
      - process contributory rules
      - yield order changed to triples,rules,bindings (to conform to rule._solve() and mtsuss._solveEquationList()/_solveEquation()

29/01/2010 stores40.py cloned from stores39.py with:
    - supports exploitation of chained fully generic rules (ie. syn of syn of ant of syn):
       - TripleStore._newLuw() method sets query caches (grcache and fqcache moved from global to class variables)
       - reserved predicates retrieved from preferences
       - _solveQuery():
         - generates cache keys exclusively from query expression values
         - detects and prevents querying of reserved predicates outside their reserved role.
           ie: with a reserved predicate as both a noun and a predicate

04/02/2010:
    _solveTriple1.tsearch():
      - tscache initialisation retrofitted to handle new Index._getMember() behaviour when default is supplied
      - ensures triples list is always passed to invoke _solveQueryList()
    TripleStore._triples()/_bindings():
      - both invoke self._newELTluw() to set any common variables in leu of Solution._solveEquationList() not being invoked

04/02/2010 stores41.py cloned from stores40.py with:
    done, vs, gr, qkeys no longer passed as params to _solveTriple()/_solveTriple1()/interpret()/tsearch()

06/02/2010:
    several more metrics collected

07/02/2010:
    several more metrics collected
    _solveQuery() also blocks previously failed rules. Additionally to _solveEquationList() now also blocking dup rule results being yielded
    _solveQueryList() always filters duplicate results

09/02/2010:
    metrics collected and reported for boolean queries:
     - total boolean queries,
     - successful boolean queries and
     - unique successful boolean queries

14/02/2010:
    _solveQuery():
     - successful queries/rules also cached and filtered
     - requirs done rules filter to be deactivated (removed)
     - metrics for successful and cached non boolean queries maintained

15/02/2010:
    -solveQuery():
      - done rule blocking index re-introduced for all but 1st time generic rule invocation - significant efficiency gain

26/02/2010 stores42.py cloned from stores41.py with:
    updated mtquery (query10.py) exploited

02/03/2010:
    - updated Index exploited:
       - l_results switched from sdict to Index accordingly (needed later for listed dict values within keys - eg. b)

12/03/2010:
    - _triples() and _bindings():
       - invoke _newEQluw() to permit cache usage
       - invoke _solveQueryList() passing infer=False
    - _solveQueryList()/_solveQuery()
       - input infer to turn this off (notably for store export)
       - if no bindings for i_results key, now uses triples instead (for unbound store queries)

13/03/2010 stores43.py cloned from stores42.py with:
    - updated mtquery (query11.py) exploited
    - failed query cache test in _solveQuery() relocated
    - match parameter initialisation simplified
    - Query/QueryList default object instantiation exploits mtquery.SuperQueryable uniqueness checks

18/03/2010 stores44.py cloned from stores43.py with:
    - exploits non-infered QueryExpression comperands

19/03/2010 further to exploiting non-infered QueryExpression comperands:
    _solveQuery():
      - exploits additional values returned from Query._makeKey():
          - inferable query (iquery) is what rules now get invoked with (omitting all exclusively exact QueryExpression opmatches)
          - triples results caches still indexed by qkey.
          - rule cache now indexed by iqkey (the inferable query key)
          - list of QueryExpression values for exclusively exact searches (one for each query element)
            exploited for additional rule test applied to found triples:
            - if found element is exclusively an exact value or
            - a reserved predicate
            - then prevent inference as a rule.

21/03/2010 stores45.py cloned from stores44.py with:
    - new representation of rules in DDL as dicts, supporting:
       1. nesting of rules within triples
       2. round tripping of rendered rules for immediate or subsequent instantiation

22/03/2010 further for new representation of rules in DDL as dicts. Changes to:
    _expandTriple() handles optional expansion of rules nested within triples or rules on their own:
      - input ExpandRules parameter which if true causes Rule._express() to be called
      - input of errors parameter for options regarding the inclusion of erroneous rhs clauses
    _generator() greatly simplified just calls _expandTriple()
    _actionPredicate():
      - rule instantiation moved from here to _processTriple() as the only method which can instantiate rules nested in triples
      - mode interpretation delegated to _actionTriple()
      - backwards compatible rule DDL results in new rule DDL passed to _actionTriple()
    _actionTriple():
      - now handles rules as dicts as well as tuples and arg lists
      - initialises mode for _processTriple()
    _processTriple():
      - instantiates rules expressed as dicts on their own or nested in tuples or lists
      - now inputs mode and newRules paramters to support above processing

28/03/2010:
    _solveQuery() only submits logical bindings returned from Rule._solve() for uniqueness

28/03/2010 stores46.py cloned from stores45.py with:
    - _solve() refactored:
       (- preliminary to refactored distributed TripleStores support)
       - _solveQueryList() and _solveQuery() moved to mtquery.QueryList._solve() and Query._solve() respectively
       - _solveQueryList() retained as a wrapper for QueryList._solve()
       - _solveQuery() removed

29/03/2010:
    - further to _solve() refactoring:
       - luw setting methods removed
       - rpreds global removed
       - _solve() methods caches passed between _solveTriple(), _solveTriple1()/.interpret/.tsearch and QueryList._solve()

30/03/2010 stores47.py cloned from stores46.py with:
    - Stores class hierachy refactored:
       - TripleStore < SimpleTripleStore < DistSimpleTripleStore (current)
                     < PersistentTripleStore < DistPersistentTripleStore (anticipated)

04/04/2010 DSTS support:
    - DSTS results store defined
    - DSTS methods defined:
       - _expandTriple() deleted to resultsStore._expandTriple()
       - _getIDfromTriple() gets id from resultsStore instantiating if not present
       - _normaliseVal() expresses a store value (triple or triple element) in terms of its resultsStore delegating to _getIDfromTriple() above
       - above methods by pass the resultsStore if DSTS contains just 1 active queryStore
       - _solveTriple():
          - delegates to each each active query store _solveTriple1()
          - returns to Query._solve() the source store (for potential rule handling)
       - overides various other parent methods
    - STS._solveTriple1():
       - enhanced to re-express query ids and returned ids according to either the DSTS or STS (itself) in context
       - changes to _interpret, tsearch and main loop after call to _interpret

05/04/2010:
    - DSTS._solveTriple() changes needed to support inference where rules are distributed.
        Specifically it now submits the query to each active query store yielding matched facts first
        and unique rules last ordered from specific to generic.
    - STS set/get instance variables exploit mtutils._genericSetter()/_genericGetter()

08/04/2010:
    - hardcoded config and prefs also defined
    - metrics file generated subject to new metrics preferences:
        - metrics labelling and sort order also defined in prefs
        - target file and showmetrics settings for TripleStore, SimpleTripleStore, DistSimpleTripleStore
        - missing preferences default to those of parent classes - up the hierachy
        - generated file uses .csv format
    - _get/_set limited to value added instantiations:
        - All others defined and accessed directly
        - _get/_set attributes not supported with Python properties feature to keep nature of attribute instantiation explicit

09/04/2010 standardisation of getter/setter and attribution syntax:
    _get(), _set(), _update() and __init__() methods checked regarding attribution.
    General rule is to reserve getters and setters to externally accessible and decorated attributes.
    These can also be used for just in time attribution (though this isn't currently so outside of the former criteria).
    Attribute setting via _update and __init__ strictly for external accessible attributes.
    Code changed throughout to access all other undecorated attributes directly.
    Python property not currently used to map _get/_set to direct attribute access syntax.

12/04/2010 stores48.py cloned from stores47.py with:
    - revised _processTriple()
    - exploiting error propogation in Rule._mergeRhs()
    - support for prefered handling of multiple versions of queried rules (including auto merge)

14/04/2010 fixes relating to merging of rules variants accessed when querying a DSTS

15/04/2010 STS triple instantiation:
    - _actionTriple() re-engineered:
        - supports list of triples
        - supports nested structures expressed as strings
        - supports optional BNF type syntax for rules
    - _processTriple() submits strings containing nested tuples and lists for recursive instantiation in addition to nested lists
    - _addTriple() raises AddTripleError for invalid triples
    - _actionPredicate() removed not needed as superceded by revised _actionTriple()
    - _import():
        - splits lines into items before invoking _actionTriple(item) to instantiate
        - counts and returns processed [lines, items, triples]

16/04/2010: DSTS load/unload supported.
    - usage of _update() methods() checked:
       - DSTS __init__() invokes TS._update() for update of TS attributes
       - invoking of _update() by other methods switched to _set..() if not None.

19/04/2010 stores49.py cloned from stores48.py with:
    - Refactored Triple Store classes:
       - SimpleTripleStore removed. Methods moved to TripleStore.
       - DistSimpleTripleStore renamed DistTripleStore.
       - reason earlier hierarchy envisaged seperate persistent classes.
          - This has not proved necessary or desirable.
          - The Persistence solution adopted allows optional persistence within existing classes.
    - Persistence supported:
       - TripleStore and DistTripleStore classes __init__() inputs optional dbname parameter.
         If supplied the instantiated store persists under that name.
       - TripleStore operational indexes combined under self._db which is either an connected ODBMS handle, or an sdict.
       - Other TripleStore and DistTripleStore params supplied via __init__() get processed as before by mtutils._genericGetter/Setter
         These updated to test presence of _db connection attribute and optionally set/get persistent values.
       - Thus apart from refactoring variable notation leaves existing methods unchanged for either persistent or transient stores.
       - TripleStore and DistTripleStore.__init__() also input optional dbreset (defaulting to None)
         If dbname=True this will remove any existing files for the named store effectively resetting it.
    - Dependent updates include:
       - mtutils - enhanced _genericGetter()/_genericSetter() and _deleteFiles() method and ODBMS abstract superclass.
       - config04.dat
       - mtquery - Query._solve() uses of store._id_to_rules refactored to store._db['i>r']
       - new ZODB01.py module imported as mtodbms
       - These changes impact the imports (if nothing else) of almost every other module.

21/04/2010 DistTripleStore resultstore persists if the DTS persists:
    - _resultStore refactored as _db['rs']
    - which points to the ODBMS object if persistent or otherwise an sdict()
    - if _db is null then _db['rs'] initialised to a new TripleStore

27/04/2010 _getIDfromTriple():
    - inputs t instead of *t
    - returns non triple inputs as is - ie. if not a triple the id is the input

29/04/2010 stores50.py cloned from stores49.py with:
    - URI support implementation:
       - _parseURI()

30/04/2010 further URI support implementation:
    - _setURImaps()

01/05/2010 further URI support implementation:
    - _parseURI() and _setURImaps() moved to mtstruct so these methods may be exploited by mtquery to prepare query value expressions
    - _parseURI() inputs mode to interpret based on one or both of:
        - base URI - at stores instantiation or stores query execution time
        - preferred predicate labels - at stores instantiation or query instantiation time

11/05/2010 supports choice of URI generation formats for output:
    - _expandTriple() now receives additional optional parameters exploited by mtrender for:
      - uid    - representation [export|native|nativenamespace]
      - target - target store for which UIDs are to be re-represented.
    - also ensures URIcommonbase and URIbasesuffix use compatible folder seperation patterns
    - _expandRule() '##nn' test changed to be for basestring starting with '##' - this excludes dicts

12/05/2010 verified rdf URI support:
    - _expandTriple():
        - side effect on input removed - ie: transformation only affects returned value not input
        - forcenative uri mode added
        - URI in rule rhs rhs get re-expressed via enhanced calls to mtrules._express()
    - _processTriple() URI transformations for rule lhs and rhs added
    - _add/deleteURIdata() and add/deleteNamespace() now use hardcoded system terms for storage

12/05/2010 stores51.py cloned from stores50.py with:
    - explicit alias_ontology support

06/06/2010 stores52.py cloned from stores51.py with:
    - supports query trace results via imports

12/06/2010 stores53.py cloned from stores52.py with:
    - folders re-configured

07/07/2010 stores.py cloned from stores53.py for SVN versioning

12/07/2010 settings support interpetation of config variables

08/08/2010 TripleStore._solveTriple1.interpret special comparator handling fixes:
    - collate matches within csearch() and esearch() and from csearch() within interpret()

09/08/2010:
    - TripleStore._solveTriple1.interpret:
        - indexed != match operator unification
        - bug fix in .csearch() evaluations and string find test
        - like match operator exploits optional fulltextindex if present
    - TripleStore support for ad-hoc fulltextindex setting or default via preference setting

10/08/2010:
    - TripleStore._solveTriple1.interpret() exploits slist()._difference_update() for UNLIKE matching from a fulltextindex.
    - Full text index settings support added for:
        - regex word extraction pattern
        - retrieval case sensitivity with local TS in DTS incompatibilities handled automatically
        - maintains 2 index variants for actual and insensitive word cases
        - multiple regex index generating patterns supports overlapping index generation
            eg: desc_of might generate the following indexes: 'desc', 'of' and 'desc_of'
        - generation of indexes from fti_regex moved to function _fti_getindexes()
        - fti_discontiguousmatch setting exploited: (the following comment is reproduced from prefs.dat)
        - fuzzy discontiguous pattern matching option supported and exploited - reworked see notes below

11/08/2010:
    - Discontiguous matching simplified and enhanced. New functionality expressed as follows:
       - fti_splitmatch setting.
          - Supports discontiguous like value matching. So '?p~fully_relationship' could match 'fully_recursive_relationship'.
          - This splits match values in the same way stored values and tests how well the parts match.
       - fti_splitmodes setting - specifies discontiguous match options which may be any of:
          - Complete:   for a pattern to match it must match ALL split match values, rather just some.
          - Consistent: matches must be present in ALL MATCHING patterns, rather than in one and not another.
       - Note: patterns which don't match anything are ignored. So the above apply only to patterns which do produce matches.

18/08/2010 Queryables instantiation now exploits new auto unique classes:
    - exception being TripleStore._solveQueryList() which explicitly instantiates a non-unique QueryList for solving.
      This is required by Structured._parseURI() for correct URI handling.

23/08/2010 TripleStore supports preference setting for its structure - either dict or rbtree

24/08/2010:
    - Compatibility checked between rbtree/dict or srbtree/sdict.
    - Forwards compatability updates between P2.6/7 and P3
      in handling support of keys(), iteritems(), sort(), map(), itemgetter() and has_key().

26/08/2010 TripleStore._solveTriple1.interpret():
    - rbtree exploited if available for indexed comparative matches

27/08/2010:
    - Towards handling of invalid default settings:
        - all defaults used only by _genericSetter() are now obtained in dual format comprising:
            - the supplied default via settings
            - a backup last resort hardcoded default if this is invalid
    - Bug fix in evaluating >/>=/</<= matches in TripleStore._solveTriple1();
        - incorrect routing of different types of op matches
          new compdx index added to classify these for simpler branhing logic
        - exploits fix in rbtree._extractSubTree() which failed to handled to the null starter tree case.

28/08/2010 performance/consistency enhancement:
    - inference caches standardised - all initiated from _EQLR_luw() (as they logically should be)
    - problem getting this work in the past was simply due to inconsistent DTS namespaces in tests!
    - sqkeycache renamed to sqcache (mirrors fqcache)

30/08/2010 performance enhancements:
    - TripleStore._newEQLR_luw() initialises new progress caches for queries and rules

02/09/2010 qid fix:
    - TripleStore._solveQueryList() QueryList instantiation compatible with latest version of query.py

05/09/2010:
    - DTS._close() added - also closes all nested stores.
    - TripleStore._newEQLRluw() - new caches added for administering caches and caching rule results.

05/09/2010 initial persistent inference cache support:
    - inference caches moved to persistable structures.
    - does NOT yet support:
        - auto reset on triple store changes rendering caches useless.
        - manual reset.
        - preference setting to turn on/off
        - seperation of physically keyed rule outcome caches from persistent cache

06/09/2010 enhanced support for inference caches and better handling of nested DTS:
    - DistTripleStore updates:
       - constructor:
          - supports inference caches
          - resets _queryStores to prevent conflict with ODBMS (see source notes)
       - _getActiveQueryStores():
          - supports nested DTS
          - traps empty stores
          - option to include local update store
       - _resetCaches() method added to reset inference caches throughout the DTS
       - _updated parameter added
    - TripleStore updates:
       - constructor supports inference caches
       - _resetCaches() method added to reset local inference caches
       - _updated parameter added
    - _addTriple/_deleteTriple() set updated to True if TripleStore is changed
    - _newEQLRluw() checks if inference caches need resetting before running query

07/09/2010 inference enhancements:
    - all stores now detect changes to their structure or database mismatches - via new _getIRV() inference relevance validation method
    - automatically generating inference data as a result.
    - DTS updates:
       - can detect changes to their constituent stores.
       - Feed Forward Inference support added.
       - _activeQueryStores attribute changes:
          - no longer clashes between DB and non DB storage - always non DB.
          - indexes results according whether rs and up stores to be included.

11/09/2010 Feed Forward Inference (FFI) administration:
    - supports automated building, maintenance and testing of FFI (DTS only)
    - supports optional full fed forward inference for nested distributed stores
    - methods:
      - _resetCaches()
      - _triggerFFI()
      - _resetFFI()
      - _getFFI()
      - _getFFImaint()
      - _getNestedDTS()
      - DTS._solveTriple() now tests special case of full ffi data covering nested DTS's
      - _getActiveQueryStores() supports new parameter settings:
         - testdts = [True|False] to return optional indicator of nested DTS's
         - rs = 'root' to only return the root 'results store' - not those of any nested DTS which may be accessed

13/09/2010
    - TripleStore._solveTriple1() supports inference at QueryExpression granularity:
       - receives QEXPS with lop (not nop) therefore knows whether it is inferable or not
       - transmits this back together with matches to invoking routines:
          - (Dist)TripleStore._solveTriple()
          - Query._solve()
    - TripleStore structure no longer updatable
       - cannot be supported without re-instantiating whole store.
       - _update(structure) param removed
       - explicit _setStructure() call in init before triple index is built
    - DistrTripleStore supports specification of structure at construction time
       - applies to us and rs stores.
       - invoking the TripleStore(structure=) param for these

18/09/2010 Enhanced Nested Queries support (Queries within Queries):
    - TripleStore._solveTriple1.tsearch():
       - refactored nested triple out to QueryList._getTIDB()
       - now supports negated nested Queries
       - tscache superceded by cache local to the QueryList - note may need globalising
    - TripleStore._solveTriple1.interpret():
       - supports detection of pre-solved nested queries - in which case binds returned as is.

21/09/2010:
    - TripleStore._solveTriple() passes supports nested Queryables variable identification:
       - supports the later identification by Rule._solve() of variables deriving solely from nested Queryables
       - needed for binding and exposing externally.
       - passes these variables through to QueryList._getTIDB()
    - Optionally persistent Nested Queryables cache added

22/09/2010: Persistent nested querylist cache removed. - Won't work accross sessions unless each set up
            queryables consistently which cannot be guaranteed.

07/10/2010: Import/Export extensions:
    - DTS:
        - new attributes supported for exporterrors, importmode, importfile and exportfile
        - new methods for export and import
        - above methods optionally update above added variables for DTS but not TS
    - TS:
        - _export(), _import(), _expandTriple(), _generate(), _generator() all support new update paramter to
          optionally prevent certain paramters updating store defaults (eg. if invoked from DTS)
        - _import() supports mode paramter passing to _processTriple() but bypassing intermediate _actionTriple()
          enables DTS import mode to be supported without updating default importmode for nested TS.

12/10/2010 Stage 0. Mixed Triple ordering support. Any single order support
    - ensure system triples are generated in same order as user supplied triples.
    - A_TripleStore._rt() exploited:
        - reorders the elements within system generated and queried triples to match that of user supplied triples
        - specifically needed for cross querying of modelled URI data with user supplied data
    - exploited by:
       - _add/_deleteURIdata()
       - _add/_deleteNamespace()
    - store specific ordering overides system default if tripleOrder paramter is set. Applies to TripleStore and DistTripleStore.
    - All values tested for validity in the following order:
       - store specific value.
       - user preference (system wide).
       - hardcoded default (not tested).

16/10/2010 Stage 1. Mixed triple ordering support: (triple data re-ordered, store specific search keys derived)
    - TripleStore._solveTriple():
        - generates triple search keys according to prefered indexes and local triple ordering.
        - inother words search is optimised for local triple ordering.
        - delivers resulting triples ordered for the parentStore.

19/10/2010 Stage 3. Mixed triple ordering support: (import and export)
    - _export() - TripleStore and DistTripleStore:
        - order paramter added - choose between self, source ordering (for DTS), and specified store ordering
        - _generate()/_generator()/_expandTriple() updated accoirdingly.
    - _generator() outputs triple ordering comment line documenting order of triples which follow:
        - line is configurable in tripleOrderExportComment setting of prefs.dat
    - _import() interprets triple ordering comment lines in sources to ro-order for self.

20/10/2010:
    - Stage 4. Mixed triple ordering support: (import and export) bug fixes
    - _actionFact()/_actionItem()/_addItem()/_deleteItem()/_expandID() refactored to
        _actionTriple()/_processTriple()/_addTriple()/_deleteTriple()/_expandTriple()
    - TS._export()/_triples()/_bindings()/_exists()/_resetCaches()/_solveQueryList()/_newEQLR_luw()
        accept new forceReset paramter to force a cache reset. Needed for export.
    - TS._import() exploits enhanced Flatfile._getValues() supporting stripping of suffixed comments only.

22/10/2010: Stage 5:  Mixed triple ordering support: Optional re-ordering for IO
    - ioTripleOrder parameter:
        - to TripleStore and DistTripleStore
        - checked by _import()/_export()/_processTriple()
        - _import() sets temporary invoker overide of store or system ioTripleOrder
    - _processTriple():
        - checks invoking method ioTripleOrder before store or system values
        - above paramter can temporarily force re-ordering off
    - _import()/_export() support optional re-ordering specified as TripleStore or as a re-ordering list.

23/10/2010: Stage 5:  Mixed triple ordering support: Optional re-ordering for IO bug fixes:
    - _deleteID: _idstack -> _db['idstack']
    - _actionTriple():
        - not detecting 'delete' or 'add' actions - missing from actkey
        - only seperating action from data if _isPred() returned both combined for 1st element
           - isPred() now returns action seperate to data for clarity
        - raw triple as lists not represented as a tuple.
           - Therefore _processTriple() couldn't identify these for ioTripleOrder based re-ordering.
           - raw triples now expressed as a tuple.

23/10/2010: TripleStore and DistTripleStore._reset() method added

@author: Administrator
'''
from operator import itemgetter
import csv, re, copy, time
import metabulate.utils.utils           as mtutils
import metabulate.utils.debug           as mtdebug
import metabulate.utils.index           as mtindex
import metabulate.utils.errors          as mterrors
import metabulate.singletons.singleton  as mtsingleton
import metabulate.queries.query         as mtquery
import metabulate.stores.structured     as mtstruct
import metabulate.rules.rules           as mtrules
import metabulate.stores.mtZODB         as mtodbms
import metabulate.stores.fti            as mtfti
import metabulate.renderers.render      as mtrender

mtconfig = mtsingleton.Settings()._getItem('config')
mtprefs  = mtsingleton.Settings()._getItem('prefs')
rulere = re.compile('^ *(.*) *:+-? *(.*) *$')
# compile list of action predicate command regex
stw = ['^\"(\+|\-|add|delete|del)\" *,? *(.*)$','^\'(\+|\-|add|delete|del)\' *,? *(.*)$','^(\+|\-|add|delete|del) *,? *(.*)$']
stwre = [re.compile(s,re.I) for s in stw]
actkey = {'+':'add','-':'delete','del':'delete','delete':'delete','add':'add'}
cpersist = mtutils._logical(mtprefs._interpretItem('inferenceCachePersistence','on'))  # do inference caches persist?
ifedforw = mtutils._logical(mtprefs._interpretItem('FFI','on'))                        # do feed forward inference?
ffimaint = mtutils._isstrpercentage(
           mtprefs._interpretItem('FFIpercentageChangeTrigger','0'),0)                 # % change triggering feed forward inference
ffinestd = mtutils._logical(mtprefs._interpretItem('FFInestedDTS','no'))               # FFI includes data from nested DTS [True|false]
# quick comperands
compdx = {'>':'>','>=':'>','<':'>','<=':'>','=':'=','!=':'=','~':'~','!~':'~'}
# synonyms/antonyms queries
qant = mtquery.Queryable._getUnique(mtquery.Query(match=('?sub','antonym_of','?obj')))
qsyn = mtquery.Queryable._getUnique(mtquery.Query(match=('?sub','synonym_of','?obj')))
# triple ordering export/import comment
tocr = toc = mtprefs._interpretItem('tripleOrderComment','# the following triples are ordered as .,.,. ** DO NOT DELETE **')
for mc in ['#','*','!',',','(',')','[',']','+','-']: tocr = tocr.replace(mc,'\\'+mc)
s = '.\,.\,.'
try:
    i = tocr.index(s)
    tocr = '^'+tocr[:i]+'(.\,.\,.)'+tocr[(i+len(s)):]
except:
    tocr = tocr+' (.\,.\,.)'
    toc += ' .,.,.'
tocre = re.compile(tocr)

class RelationalStore(mtstruct.A_RelationalStore): pass
class TripleStore(mtstruct.A_TripleStore):
    _indexes = ['012', '120', '201']
    _idxqe   = mtutils.slist()
    _uriouts = {'export':'has_rdfuri','native':'has_nativeuri','forcenative':'has_nativeuri','nativealias':'has_displayuri'}
    for c,v in enumerate(_indexes): _idxqe[c] = mtquery.Queryable._getUnique(mtquery.QueryExpression(vals=[v]))
    # defaults as pairs for mtutils._genericSetter() from settings and hardcoded
    _default_encoding      = mtconfig._interpretItem('stores_encoding','UTF-8')
    _default_timestamped   = mtconfig._interpretItem('stores_timestamped','no',2)      # (True|default=False)
    _default_versioned     = mtconfig._interpretItem('stores_versioned','no',2)        # (True|default=False)
    _default_secured       = mtconfig._interpretItem('stores_secured','no',2)          # (True|default=False)
    _default_infer         = mtconfig._interpretItem('stores_infer','yes',2)           # infer triples from rules (default=True|False)
    _default_exporterrors  = mtprefs._interpretItem('stores_exporterrors','yes',2)     # allow commented failed rules to be exported
    _default_importmode    = mtprefs._interpretItem('stores_importmode','merge',2)     # mode for handling import of duplicate rules
    _default_fti           = mtprefs._interpretItem('fti','true',2)                    # maintain a fulltextindex
    _default_URIsupport    = mtprefs._interpretItem('URIsupport','yes',2)              # uri support [no|yes|model]
    _default_structure     = mtprefs._interpretItem('structure','dict',2)              # structure of TripleStore [dict|rbtree]
    # defaults as single values (because they are used elsewhere to mtutils._genericSetter())
    _default_importfile    = mtutils.Flatfile(path=mtconfig._interpretItem('stores_importfile_path','%configfilesbase%Results\\')
                                             ,name=mtconfig._interpretItem('stores_importfile_name','mystore')
                                             ,type=mtconfig._interpretItem('stores_importfile_type','sts')
                                             )
    _default_exportfile    = mtutils.Flatfile(path=mtconfig._interpretItem('stores_exportfile_path','%configfilesbase%Results\\')
                                             ,name=mtconfig._interpretItem('stores_exportfile_name','mystore')
                                             ,type=mtconfig._interpretItem('stores_exportfile_type','sts')
                                             )
    _default_loadfile      = mtutils.Flatfile(path=mtconfig._interpretItem('stores_loadfile_path','%configfilesbase%Unloads\\')
                                             ,name=mtconfig._interpretItem('stores_loadfile_name','mystore')
                                             ,type=mtconfig._interpretItem('stores_loadfile_type','pyo')
                                             )
    _default_unloadfile    = mtutils.Flatfile(path=mtconfig._interpretItem('stores_unloadfile_path','%configfilesbase%Unloads\\')
                                             ,name=mtconfig._interpretItem('stores_unloadfile_name','mystore')
                                             ,type=mtconfig._interpretItem('stores_unloadfile_type','pyo')
                                             )
    _metricfile_path       = mtconfig._interpretItem('stores_metricfile_path','%configfilesbase%Metrics/')
    _metricfile_name       = mtconfig._interpretItem('stores_metricfile_name','metrics')
    _metricfile_type       = mtconfig._interpretItem('stores_metricfile_type','csv')
    _default_metricfile    = mtutils.Flatfile(path=_metricfile_path
                                            ,name=_metricfile_name
                                            ,type=_metricfile_type
                                             )
    _default_showmetrics   = mtprefs._interpretItem('stores_showmetrics','yes')        # report metrics [yes|no]
    _default_dbpath        = mtconfig._interpretItem('stores_dbpath','%configfilesbase%Stores/')
    _default_dbtype        = mtconfig._interpretItem('stores_dbtype','fs')
    _default_URIbasesuffix = ''
    _URIcommonbase         = mtprefs._interpretItem('URIcommonbase','http://www.semanticle.org/triples/')
    # ensure consistent folder seperation in URI base
    if _URIcommonbase and _URIcommonbase[-1] != '/': _URIcommonbase += '/'
    while _default_URIbasesuffix and _default_URIbasesuffix[0] == '/': _default_URIbasesuffix = _default_URIbasesuffix[1:]

    def __init__(self
                ,encoding=None
                ,timestamped=None
                ,versioned=None
                ,secured=None
                ,infer=None
                ,exporterrors=None
                ,importmode=None
                ,importfile=None
                ,exportfile=None
                ,loadfile=None
                ,unloadfile=None
                ,metricfile=None
                ,showmetrics=None
                ,dbname=None
                ,dbreset=None
                ,URIsupport=None
                ,URIbasesuffix=None
                ,fti=None
                ,fti_usecase=None
                ,fti_splitmatch=None
                ,fti_splitmodes=None
                ,structure=None
                ,tripleOrder=None
                ,ioTripleOrder=None
                 ):
        # implementation values
        if dbname is not None:                                                  # if supplied db name: (open it as self._db)
            fn = mtutils.Flatfile(path=self._default_dbpath
                                 ,name=dbname
                                 ,type=self._default_dbtype
                                  )._getFullname()                              #  get full db filename
            if dbreset is True: mtutils._deleteFiles(fn+'*')
            self._db = mtodbms.DBstore(fn)                                      #  self._db is a ODBMS instance connected to full db filename
        else: self._db = mtutils.sdict()
        if not self._db:                                                        # if no persistent data: (initialise it)
            if structure is not None: self._setStructure(structure)
            self._reset()
        elif not cpersist:                                                      # elif persistence doesn't include inference caches: (reset them)
            self._db['crs'] = mtindex.Index()                                   #  outcomes cache - rule  successes
            self._db['crf'] = mtindex.Index()                                   #  outcomes cache - rule  failures
            self._db['cqs'] = mtindex.Index()                                   #  outcomes cache - query successes
            self._db['cqf'] = mtindex.Index()                                   #  outcomes cache - query failures
        self._crs = mtindex.Index()                                             # transient outcomes cache - rule  successes (physically keyed)
        self._crf = mtindex.Index()                                             # transient outcomes cache - rule  failures  (physically keyed)
        self._cqs = mtindex.Index()                                             # transient outcomes cache - query successes (physically keyed)
        self._cqf = mtindex.Index()                                             # transient outcomes cache - query failures  (physically keyed)
        # outcomes caches structure: {logical or physical query key:{{bindings}:[triples,rules,{bindings}]},{more results},..]}
        #  - outcomes which are inprogress will have their intermeadiate results cached here indexed by their physical query key
        #  - outcomes which have been fully resolved have their final results cached here indexed by a logical query key
        #    in which case previously cached intermediate results are deleted as no longer needed.
        self._pqcache = mtindex.Index()                                         # in progress query cache  {qkey:[..[..,..,..]]}
        self._prcache = mtindex.Index()                                         # in progress rules cache {iqkey:[..[..,..,..]]}
        # progress caches for queries or rules producing intermediate results
        # structure {logical key:[resolution recursion depth,[unique intermediate physical keys,..]]}
        # Note: self._cqs, self._cqf and self._pqcache not exploited in all versions of query.py
        # API updatable values
        if tripleOrder is not None: self._setTripleOrder(tripleOrder)           # Note: this cannot be updated!!
        self._update(encoding=encoding
                    ,timestamped=timestamped
                    ,versioned=versioned
                    ,secured=secured
                    ,infer=infer
                    ,exporterrors=exporterrors
                    ,importmode=importmode
                    ,importfile=importfile
                    ,exportfile=exportfile
                    ,loadfile=loadfile
                    ,unloadfile=unloadfile
                    ,metricfile=metricfile
                    ,showmetrics=showmetrics
                    ,URIsupport=URIsupport
                    ,URIbasesuffix=URIbasesuffix
                    ,fti=fti
                    ,fti_usecase=fti_usecase
                    ,fti_splitmatch=fti_splitmatch
                    ,fti_splitmodes=fti_splitmodes
                    ,ioTripleOrder=ioTripleOrder
                    )
    def _reset(self):
        # usage:
        #    initialise or empty store contents
        #    called by self.__init__()
        #    can be used to reset a store to its empty state
        self._db['t'] = eval('mtutils.s'+self._getStructure()+'()')             #  set triples index to storeindex 's' variant
        self._db['idstack'] = []                                                #  spare triple ids stack
        self._db['upc'] = 0                                                     #  initialise update count
        self._db['i>t'] = {}                                                    #  triples indexed by triple ids dict
        self._db['i>r'] = {}                                                    #  rules indexed by triple ids dict {id1:Rule1, id2:Rule2,..,idn:Rulen}
        self._db['w']   = mtfti.fti()                                           #  fulltext index = nativeURIs indexed by words
        self._db['cts'] = time.time()                                           #  creation timestamp - serves as an identifier together with size
        self._db['irv'] = []                                                    #  inference relevance validation list - holds (cts,size)
        self._db['crs'] = mtindex.Index()                                       #  outcomes cache - rule  successes
        self._db['crf'] = mtindex.Index()                                       #  outcomes cache - rule  failures
        self._db['cqs'] = mtindex.Index()                                       #  outcomes cache - query successes
        self._db['cqf'] = mtindex.Index()                                       #  outcomes cache - query failures
    def _update(self
               ,encoding=None
               ,timestamped=None
               ,versioned=None
               ,secured=None
               ,infer=None
               ,exporterrors=None
               ,importmode=None
               ,importfile=None
               ,exportfile=None
               ,loadfile=None
               ,unloadfile=None
               ,metricfile=None
               ,showmetrics=None
               ,URIsupport=None
               ,URIbasesuffix=None
               ,fti=None
               ,fti_usecase=None
               ,fti_splitmatch=None
               ,fti_splitmodes=None
               ,ioTripleOrder=None
                ):
        if encoding       is not None: self._setEncoding(encoding)
        if timestamped    is not None: self._setTimestamped(timestamped)
        if versioned      is not None: self._setVersioned(versioned)
        if secured        is not None: self._setSecured(secured)
        if infer          is not None: self._setInfer(infer)
        if exporterrors   is not None: self._setExporterrors(exporterrors)
        if importmode     is not None: self._setImportmode(importmode)
        if importfile     is not None: self._setImportfile(importfile)
        if exportfile     is not None: self._setExportfile(exportfile)
        if loadfile       is not None: self._setLoadfile(loadfile)
        if unloadfile     is not None: self._setUnloadfile(unloadfile)
        if metricfile     is not None: self._setMetricfile(metricfile)
        if showmetrics    is not None: self._setShowmetrics(showmetrics)
        if URIsupport     is not None: self._setURIsupport(URIsupport)
        if URIbasesuffix  is not None: self._setURIbasesuffix(URIbasesuffix)
        if fti            is not None: self._setFti(fti)
        if fti_usecase    is not None: self._setFti_usecase(fti_usecase)
        if fti_splitmatch is not None: self._setFti_splitmatch(fti_splitmatch)
        if fti_splitmodes is not None: self._setFti_splitmodes(fti_splitmodes)
        if ioTripleOrder  is not None: self._setIoTripleOrder(ioTripleOrder)
    def _resetSubmitted(self): self._submitted = mtutils.sdict()
    def _setEncoding(self,*args):
        return mtutils._genericSetter(self,'encoding',args,t=basestring)
    def _getEncoding(self,default=True):
        return mtutils._genericGetter(self,'encoding',default)
    def _setTimestamped(self,*args):
        return mtutils._genericSetter(self,'timestamped',args,m=[True,False],logical=True)
    def _getTimestamped(self,default=True):
        return mtutils._genericGetter(self,'timestamped',default)
    def _setVersioned(self,*args):
        return mtutils._genericSetter(self,'versioned',args,m=[True,False],logical=True)
    def _getVersioned(self,default=True):
        return mtutils._genericGetter(self,'versioned',default)
    def _setSecured(self,*args):
        return mtutils._genericSetter(self,'secured',args,m=[True,False],logical=True)
    def _getSecured(self,default=True):
        return mtutils._genericGetter(self,'secured',default)
    def _setInfer(self,*args):
        return mtutils._genericSetter(self,'infer',args,m=[True,False],logical=True)
    def _getInfer(self,default=True):
        return mtutils._genericGetter(self,'infer',default)
    def _setExporterrors(self,*args):
        return mtutils._genericSetter(self,'exporterrors',args,m=[True,False],logical=True)
    def _getExporterrors(self,default=True):
        return mtutils._genericGetter(self,'exporterrors',default)
    def _setImportmode(self,*args):
        return mtutils._genericSetter(self,'importmode',args,m=['merge','keep','replace'])
    def _getImportmode(self,default=True):
        return mtutils._genericGetter(self,'importmode',default)
    def _setImportfile(self,*args):
        return mtutils._genericSetter(self,'importfile',args,t=mtutils.Flatfile)
    def _getImportfile(self,default=True):
        return mtutils._genericGetter(self,'importfile',default)
    def _setExportfile(self,*args):
        return mtutils._genericSetter(self,'exportfile',args,t=mtutils.Flatfile)
    def _getExportfile(self,default=True):
        return mtutils._genericGetter(self,'exportfile',default)
    def _setLoadfile(self,*args):
        return mtutils._genericSetter(self,'loadfile',args,t=mtutils.Flatfile)
    def _getLoadfile(self,default=True):
        return mtutils._genericGetter(self,'loadfile',default)
    def _setUnloadfile(self,*args):
        return mtutils._genericSetter(self,'unloadfile',args,t=mtutils.Flatfile)
    def _getUnloadfile(self,default=True):
        return mtutils._genericGetter(self,'unloadfile',default)
    def _setMetricfile(self,*args):
        return mtutils._genericSetter(self,'metricfile',args,t=mtutils.Flatfile)
    def _getMetricfile(self,default=True):
        return mtutils._genericGetter(self,'metricfile',default)
    def _setShowmetrics(self,*args):
        return mtutils._genericSetter(self,'showmetrics',args,m=[True,False],logical=True)
    def _getShowmetrics(self,default=True):
        return mtutils._genericGetter(self,'showmetrics',default)
    def _setURIsupport(self,*args):
        return mtutils._genericSetter(self,'URIsupport',args,m=['no','yes','model'])
    def _getURIsupport(self,default=True):
        return mtutils._genericGetter(self,'URIsupport',default)
    def _setURIbasesuffix(self,*args):
        return mtutils._genericSetter(self,'URIbasesuffix',args,t=basestring)
    def _getURIbasesuffix(self,default=True):
        return mtutils._genericGetter(self,'URIbasesuffix',default)
    def _setFti(self,*args):
        return mtutils._genericSetter(self,'fti',args,m=[True,False],logical=True)
    def _getFti(self,default=True):
        return mtutils._genericGetter(self,'fti',default)
    def _setFti_usecase(self,*args):
        return self._getFti()._setUsecase(args)
    def _getFti_usecase(self,default=True):
        return self._getFti()._getUsecase(args)
    def _setFti_splitmatch(self,*args):
        return self._getFti()._setSplitmatch(args)
    def _getFti_splitmatch(self,default=True):
        return self._getFti()._getSplitmatch(args)
    def _setFti_splitmodes(self,*args):
        return self._getFti()._setSplitmodes(args)
    def _getFti_splitmodes(self,default=True):
        return self._getFti()._getSplitmodes(args)
    def _setStructure(self,*args):
        return mtutils._genericSetter(self,'structure',args,m=['dict','rbtree'])
    def _getStructure(self,default=True):
        return mtutils._genericGetter(self,'structure',default)
    def _getFFI(self): return None
    def _getFFImaint(self): return None
    def _resetFFI(self): return False
    def _getURIbase(self): return self._URIcommonbase+self._getURIbasesuffix()
    def _resetActiveQueryStores(self): pass
    def _unload(self, file=None):
        if file is not None: self._setUnloadfile(file)
        return self._getUnloadfile()._unload(self)
    def _load(self, file=None):
        # usage: loads TripleStore object from file
        #        store = store[n]._load(filename='filename')
        # returns: loaded TripleStore
        if file is not None: self._setLoadfile(file)
        return self._getLoadfile()._load()
    def _triples(self, queryList='',forceReset=None):
        # usage:
        #    get triples matching queryList from this store
        # inputs:
        #    queryList  - QueryList object or expression
        #    forceReset - force cache reset regardless of other constraints [True|False]
        # yields:
        #    t          - matching triple one at a time
        for t,r,b in self._solveQueryList(queryList=queryList,infer=False,forceReset=forceReset): yield t
    def _bindings(self, queryList='',forceReset=None):
        # usage:
        #    get bindings matching queryList from this store
        # inputs:
        #    queryList  - QueryList object or expression
        #    forceReset - force cache reset regardless of other constraints [True|False]
        # yields:
        #    b          - matching bindings one result at a time
        for t,r,b in self._solveQueryList(queryList=queryList,infer=False,forceReset=forceReset): yield b
    def _exists(self, queryList='',forceReset=None):
        # usage:
        #    determines if queryList can be matched exactly from this store
        # inputs:
        #    queryList  - QueryList object or expression
        #    forceReset - force cache reset regardless of other constraints [True|False]
        # returns:
        #   exists      - matches exist [True|False]
        exists = False
        for t,r,b in self._solveQueryList(queryList=queryList,infer=False,forceReset=forceReset):
            exists = True
            break
        return exists
    def _makeirv(self):
        # usage:
        #    deduces the current irv value (if any) - if not returns None
        try: irv = (self._db['cts'],self._db['upc'],len(self._db['t']))
        except: irv = None
        return irv
    def _testirv(self,irv=None):
        # usage:
        #    tests the current irv (deduced or supplied) against the stored irv
        bad = True
        if irv:
            if irv == self._db['irv']: bad = False
            else: self._db['irv'] = irv
        else:
            irv = self._makeirv()
            if irv == self._db['irv']: bad = False
        return bad,irv
    def _resetCaches(self,irv=None,force=None):
        # usage:
        #    if store updated since inference caches - clears all inference cache data
        #    tests the current irv (deduced or supplied) against the stored irv
        #    if different resets caches
        # inputs:
        #    irv   - current inference relevance value which if different from stored updates the stored value
        #            if None or ommitted this gets deduced but doesn't update the stored value
        #    force - force cache reset [True|False].
        # returns:
        #    bad   - indicates if caches reset [True|False]
        #    irv   - current inference relevance value
        if irv is None: irv = self._makeirv()
        bad,irv = self._testirv(irv=irv)
        if bad is True or force is True:                                        # only bother if this store has changed
            self._db['crs'] = mtindex.Index()                                   #  outcomes cache - rule  successes
            self._db['crf'] = mtindex.Index()                                   #  outcomes cache - rule  failures
            self._db['cqs'] = mtindex.Index()                                   #  outcomes cache - query successes
            self._db['cqf'] = mtindex.Index()                                   #  outcomes cache - query failures
            self._crs = mtindex.Index()                                         #  transient outcomes cache - rule  successes (physically keyed)
            self._crf = mtindex.Index()                                         #  transient outcomes cache - rule  failures  (physically keyed)
            self._cqs = mtindex.Index()                                         #  transient outcomes cache - query successes (physically keyed)
            self._cqf = mtindex.Index()                                         #  transient outcomes cache - query failures  (physically keyed)
            self._pqcache = mtindex.Index()                                     #  in progress query cache  {qkey:[..[..,..,..]]}
            self._prcache = mtindex.Index()                                     #  in progress rules cache {iqkey:[..[..,..,..]]}
#            self._resetSynonyms()
            # Note: self._cqs, self._cqf and self._pqcache not exploited in all versions of query.py
        return bad,irv
    # setup run-time results caches by scope
    def _resetSynonyms(self):
        ants = {}
        syns = {}
        for t,r,b in qsyn._solve():
            s1 = b['sub']
            s2 = b['obj']
            if s1 not in syns: syns[s1] = mtutils.slist([s2])
            elif s2 not in syns[s1]: syns[s1] += [s2]
            if s2 not in syns: syns[s2] = mtutils.slist([s1])
            elif s1 not in syns[s2]: syns[s2] += [s1]
        for t,r,b in qant._solve():
            a1 = b['sub']
            a2 = b['obj']
            if a1 not in ants: ants[a1] = mtutils.slist([a2])
            elif a2 not in ants[a1]:
                # reciprocol antonyms are synonyms
                for a1a in ants[a1]:
                    a1ss = syns[a1]
                    for a1s in ants[a1a]: a1ss = a1ss._union(syns[a1s])
                    for a1s in ants[a1a]: syns[a1s] = a1ss
                syns[a1] = a1ss
                # common antonyms share synonyms
                if a2 in syns:
                    for a2s in syns[a2]: syns[ants[a1][0]] += a2s
                    syns[a2] = syns[ants[a1][0]]
                ants[a1] += [a2]
            if a2 not in ants: ants[a2] = mtutils.slist([a1])
            elif a1 not in ants[a2]:
                # reciprocol antonyms are synonyms
                for a2a in ants[a2]:
                    a2ss = syns[a2]
                    for a2s in ants[a2a]: a2ss = a2ss._union(syns[a2s])
                    for a2s in ants[a2a]: syns[a2s] = a2ss
                syns[a2] = a2ss
                # common antonyms share synonyms
                if a1 in syns:
                    for a1s in syns[a1]: syns[ants[a2][0]] += a1s
                    syns[a1] = syns[ants[a2][0]]
                ants[a2] += [a1]
        self._db['syn'] = syns
        self._db['ant'] = ants
    def _newEQLR_luw(self,infer=None,forceReset=None):                          # initialisation of EQuationList Results LUW
        # usage:
        #    resets store query/inference caches subject to constraints
        # inputs:
        #    infer      - inference [True|False|'ffi']
        #    forceReset - force cache reset regardless of other constraints [True|False]
        self._resetActiveQueryStores()                                          #  reset list of activeQueryStores (pass if not a distributed store)
        # metrification caches
        self._metrics = mtindex.Index()                                         #  metrics cache
        self._sbqcache = mtindex.Index()                                        #  successfull boolean query cache (metrification)
        if forceReset is True: self._resetCaches(force=True)
        elif infer is not False and infer != 'ffi':                             #  if feed forward inference is neither False nor being built:
            self._resetCaches()                                                 #   check to reset inference caches and rebuild ffi data
    def _newEQL_luw(self):                                                      # initialisation of EQuationList luw
#        self._fqcache = mtindex.Index()                                        #  failed query cache
#        self._sbqcache = mtindex.Index()                                       #  successfull boolean query cache (metrification)
        pass
    def _newEQ_luw(self):                                                       # initialisation of EQuation LUW
#        self._frcache = mtindex.Index()                                        #  failed rules cache
        pass
    def _newQL_luw(self):                                                       # initialisation of QueryList LUW
#        self._fqcache = mtindex.Index()                                        # failed query cache
#        self._sbqcache = mtindex.Index()                                       # successfull boolean query cache
        pass
    def _setMetric(self,item,v):
        if not isinstance(v,int) and ',' in str(v): v = '"'+str(v)+'"'          # for non integer metrics ensure no commas to corrupt csv interpretation
        return self._metrics._setItem(item,v)
    def _getMetric(self,item):
        if item == 'qkeymax': d = ''
        else: d = 0
        return self._metrics._getItem(item,d)
    def _incMetric(self,item): return self._metrics._incItem(item)
    def _showMetrics(self):
        if self._getShowmetrics():
            try:
                self._setMetric('time',time.ctime())
                mp = mtutils._stripsplit(mtprefs._interpretItem('stores_metrics'
                                                               ,'0,timestamp,time,1,total q,tq,2,ok q,qc,3,ok q: u qkey,usqkey,4,q failed,fq,5,u q failed,ufq,6,total b q,tbq,7,ok b q,sbq,8,u ok b q,usbq,9,total ok nb q,snbq,10,rules,rl,11,g rules,gr,12,rg rules,rgr,13,r failed,fr,14,u r failed,ufr,15,EQL res,irs,16,EQL rule res,irl,17,bl rules,br,18,bl rg rule,brgr,19,bl failed q,bfq,20,bl dup EQL res,bdrs,21,bl dup EQL rule res,bdrl,22,bl dup QL res,bdql,23,max cached res count,maxrc,24,max res count query,qkeymax'))
                im = mtutils.sdict()
                for c in range(0,len(mp),3):
                    im[mp[c]] = [mp[c+1],self._getMetric(mp[c+2])]
                mf = self._getMetricfile()
                out = ''
                if not mf._getValue():
                    for k in sorted(im): out += im[k][0]+','
                    if out: out = out[:-1]+'\n'
                for k in sorted(im):
                    i = im[k][1]
                    if not isinstance(i,basestring): i = str(i)
                    out += i+','
                if out:
                    out = out[:-1]+'\n'
                    mf._appendValue(out)
            except: pass
    def _actionTriple(self, *args):
        # usage:
        #    flexible wrapper for updating the triple store: _actionTriple > _processTriple > _addTriple|_deleteTriple
        #    recurses for nested triples, and lists of changed items within repeated triples _triple
        # inputs:
        #    list of args representing a triple optionally prefixed with a triple action. Supplied as:
        #     - string to be evaluated either as enclosed or un-enclosed list with:
        #        - optional action prefix (+|-|delete|add|del):
        #           - optionally quoted
        #           - optionally suffixed by a comma
        #        - examples of acceptable arguements:
        #            args = ["('a','b','c')"]
        #            args = ["delete('a','b','c')"]
        #            args = ["delete ('a','b','c')"]
        #            args = ["delete,('a','b','c')"]
        #            args = ["delete, ('a','b','c')"]
        #            args = ["'delete'('a','b','c')"]
        #            args = ["'delete' ('a','b','c')"]
        #            args = ["'delete',('a','b','c')"]
        #            args = ["'delete', ('a','b','c')"]
        #            args = ["delete 'a','b','c'"]
        #            args = ["delete,'a','b','c'"]
        #            args = ["delete, 'a','b','c'"]
        #            args = ["'delete''a','b','c'"]
        #            args = ["'delete' 'a','b','c'"]
        #            args = ["'delete','a','b','c'"]
        #            args = ['add', "[('bob', 'child_of', 'alice'),('dan', 'child_of', 'cev')]"]
        #            args = ['add', [('cev', 'child_of', 'bob'), "('dan', 'child_of', 'cev')"]
        #            args = ["add [('bob', 'child_of', 'alice'),('dan', 'child_of', 'cev')]"]
        #     - optional triple as last 3 items listed, or as a 3 item tuple
        #    if action prefix missing or invalid this defaults to 'add'
        # returns:
        #    results array of affected triples ([] if no action possible) as follows:
        #        [action,[[id1,result_code1,lhs],..[results for triple n]]
        def isPred(i,c):
            def isrule(i):
                try:                                                            #  logical try (matching rule regex):
                    fact  = eval(rulere.match(i).group(1))                      #   get fact (lhs) from regex
                    rule  = eval(rulere.match(i).group(2))                      #   get rule (rhs) from regex
                    pred = [{fact:rule}]                                        #   re-express as dictionary
                except: pred = False                                            #  failed - so its a fact: get it
                return pred
            # End isrule
            args = []
            action = ''
            rest = i
            if not c and isinstance(i,basestring):
                for s in stwre:                                                 #   for each regex variant:
                    if s.match(i):                                              #    if a match: (parse with match)
                        action = s.match(i).group(1).lower()                    #     get lowercase action
                        rest = s.match(i).group(2)                              #     get fact
                        if action in actkey: action = actkey[action]            #     action as formal keyword
                        break                                                   #     string arg parsed - so break
            fact = isrule(rest)
            if not fact:
                if ((isinstance(rest,tuple) and len(rest) == 3)
                 or isinstance(rest,dict)
                 or isinstance(rest,list)
                    ):
                    fact = rest
                elif isinstance(rest,basestring):
                    try: fact = eval(rest)
                    except: fact = rest
            if fact: args += [fact]
            return action,args
        # End isPred
        self._showDebug(clas='TripleStore',method='_actionTriple',note='inputs',line=1160,level=0,vars=[['args',args]])
        action = 'add'
        args  = mtutils.slist(args)._peel(0)                                    # peel away outer lists if any
        args1 = []                                                              # prepare final data list
        for c,arg in enumerate(args):                                           # for each input arg
            act,args2 = isPred(arg,c)                                           #  interpret action and data
            if not c and act: action = act                                      #  if leading element is action: apply action
            args1 += args2                                                      #  collate data
        self._showDebug(clas='TripleStore',method='_actionTriple',line=1169,level=1,vars=[['action',action],['args1',args1]])
        ids = []                                                                # initialise affected triple ids list
        l = len(args1)                                                          # get data length (either 3=raw triple or 1=list of triples)
        if l == 3: args1 = [tuple(args1)]; l = 1                                # if raw triple: turn into a list of 1 triple
        if l == 1:                                                              # if list of triples:
            for id,rc,ftr in self._processTriple(action,[],args1):              #  process each triple:
                ids += [id]                                                     #   collating the affected triple ids
                self._showDebug(clas='TripleStore',method='_actionTriple',line=1175,level=1,vars=[['id',id],['rc',rc],['ftr',ftr]])
        self._showDebug(clas='TripleStore',method='_actionTriple',note='returns',line=1176,level=0,vars=[['ids',ids]])
        return ids
    def _processTriple(self,action,head,tail,mode=None):
        # usage:
        #    wrapper for inner recursive processTriple() method prepares mode, newRules and referant
        # inputs:
        #    action    - add|delete|assert|retract
        #    head      - list of triple elements already processed
        #    tail      - list of triple elements to be processed
        #    mode      - optional import mode for handling multiple versions of rules overrides preferance [merge|keep|replace]
        # yields:
        #    id        - id of parent triple (new or existing)
        #    rc        - result code for id (1 = new, 0 = existing)
        #    ftr       - full expanded representation of this triple (ie with variable names if any)
        def processTriple(action,head,tail,mode,newRules,referant,order):
            # usage:
            #    (head, tail) recursive interpretter of triples|rule-lhs's for actioning in the store
            # inputs:
            #    action    - add|delete|assert|retract
            #    head      - list of triple elements already processed
            #    tail      - list of triple elements to be processed
            #    mode      - import mode for handling multiple versions of rules [merge|keep|replace]
            #    newRules  - index of rule versions found
            #    referant  - referanced rhs component to a rule
            #    order     - TripleStore object to which the ordering of processed triples conforms if different from self (otherwise None)
            # yields:
            #    id        - id of parent triple (new or existing)
            #    rc        - result code for id (1 = new, 0 = existing)
            #    ftr       - full expanded representation of this triple (ie with variable names if any)
            self._showDebug(clas='TripleStore',method='_processTriple',note='.processTriple inputs',line=1204,level=0,vars=[['action',action],['mode',mode],['newRules',newRules]])
            self._showDebug(clas='TripleStore',method='_processTriple',note='.processTriple inputs',line=1205,level=0,vars=[['head',head]])
            self._showDebug(clas='TripleStore',method='_processTriple',note='.processTriple inputs',line=1206,level=0,vars=[['tail',tail]])
            if tail:                                                            # if elements remain to triple: (process them)
                if isinstance(tail[0],list) or isinstance(tail[0],dict):        #   if its a propogation list
                    for item in tail[0]:                                        #    propogate each list item
                        if isinstance(tail[0],dict): referant = tail[0][item]
                        else: referant = None
                        for id,rc,ftr in processTriple(action,head,[item]+list(tail[1:]),mode,newRules,referant,order
                                                       ):                       #    yield each propogated triple
                            self._showDebug(clas='TripleStore',method='_processTriple',note='.processTriple yields',line=1214,level=0,vars=[['id',id],['rc',rc],['ftr',ftr]])
                            yield id,rc,ftr
                elif isinstance(tail[0],tuple) and len(tail[0]) == 3:           #   elif its a nested triple
                    if order: tail[0] = self._rt(tail[0]                        #    if reorder triple: do so
                                                ,order=order._getTripleOrder()  #     (default re-ordering from order to self)
                                                 )
                    for id,rc,ftr in processTriple(action,[],tail[0],mode,newRules,None,order
                                                   ):                           #    submit and get each id
                        item = '##'+str(id)
                        self._showDebug(clas='TripleStore',method='_processTriple',note='.processTriple',line=1223,level=0,vars=[['id',id],['rc',rc],['item',item]])
                        if referant and action == 'add':                        #        if theres an referant to be added:
                            self._showDebug(clas='TripleStore',method='_processTriple',note='.processTriple',line=1225,level=1,vars=[['id',id]])
                            try:                                                #         try processing refereant as rule rhs:
                                lhs = self._expandTriple(ftr                    #          expand the rule lhs
                                                         ,uri='forcenative'     #           (without re-ordring as this already done)
                                                          )                     #           force native lhs URI's (eg. original may rdf)
                                rhs = self._expandTriple(referant               #          expand the rhs
                                                        ,order=order            #           with re-ordering (if order not None)
                                                        ,orderToSelf=True       #           (re-order from order to self)
                                                        ,uri='forcenative'      #           force native rhs URI's (eg. original may rdf)
                                                         )
                                if (item in self._db['i>r']                     #          if rule exists
                                and (mode == 'merge' or item in newRules)       #           and and ok to merge:
                                    ):                                          #           merge new rhs to existing based on new lhs
                                    self._db['i>r'][item]._mergeRhs(nlhs=lhs,nrhs=rhs)
                                elif (mode != 'keep'
                                   or item not in self._db['i>r']               #          elif new rule ok to add:
                                      ):
                                    self._db['i>r'][item] = \
                                    mtrules.Rule(lhs=lhs,rhs=rhs)               #       add it
                                    if mode != 'merge': newRules[item] = ''     #       if needbe note as new
                            except mterrors.MTerror, X:                         #         except referant as rule rhs fails:
                                pass
                        if len(head)+len(tail) == 3:
                            for id1,rc1,ftr1 in processTriple(action,head+[item],tail[1:],mode,newRules,None,order
                                                              ):                #    for each triple from remaining elements
                                ftr1 = tuple(list(ftr1[:len(head)])             #      build full expanded triple
                                            +[ftr]
                                            +list(ftr1[len(head)+1:])
                                             )
                                self._showDebug(clas='TripleStore',method='_processTriple',note='.processTriple yields',line=1254,level=0,vars=[['id1',id1],['rc1',rc1],['ftr1',ftr1]])
                                yield id1,rc1,ftr1                              #     yield results
                        else: yield id,rc,ftr
                elif isinstance(tail[0],basestring):                            #     check if its a nested element represented as string
                    try:
                        item = eval(tail[0])                                    #      try evaluating the value expression
                        if (isinstance(item,dict)                               #       if its perhaps a rule
                         or isinstance(item,tuple)                              #        or a triple
                         or isinstance(item,list)                               #        or a list of elements:
                            ):
                            for id,rc,ftr in processTriple(action,head,[item]+tail[1:],mode,newRules,None,order
                                                           ):                   #        submit and yield results (if any)
                                yield id,rc,ftr
                    except:                                                     #      except its just a string
                        if tail[0][:1] == '?':                                  #       if its a variable (ie from a rule):
                            item = '?'                                          #        prepare for triple index without the name
                        else: item = tail[0]                                    #       else keep as it is
                        for id,rc,ftr in processTriple(action,head+[item],tail[1:],mode,newRules,None,order
                                                       ):                       #       submit and get each propogation results
                            ftr = tuple(list(ftr[:len(head)])                   #        build full expanded triple
                                       +[tail[0]]
                                       +list(ftr[len(head)+1:])
                                        )
                            self._showDebug(clas='TripleStore',method='_processTriple',note='.processTriple yields',line=1277,level=0,vars=[['id',id],['rc',rc],['ftr',ftr]])
                            yield id,rc,ftr                                     #        yield
            else:                                                               #  elif triple fully examined:
                id,rc = eval('self._'+action+'Triple(t=head)')                  #   action it to the store
                self._showDebug(clas='TripleStore',method='_processTriple',note='.processTriple yields',line=1281,level=0,vars=[['id',id],['rc',rc],['head',head],['tail',head]])
                yield id,rc,tuple(head)                                         #   yield results
            # End processTriple()
        # validate overridable parameters at method, API_method, and class levels
        if mode is None:                                                        # if mode is None:
            try: mode = self._timportmode                                       #  it may have been passed via self._timportmode
            except AttributeError: mode = None                                  #  if not set to None
        if mode is None: mode = self._getImportmode()                           #  if nothing passed via timportmode get from store default
        # validate re-ordering setting and ensure it is expressed as a TripleStore
        order = None                                                            # default no re-ordering
        try: order = self._tioTripleOrder                                       # try getting parent method ioTripleOrder
        except AttributeError: pass                                             # ignore if fails
        if order is None: order = self._getIoTripleOrder()                      # still no re-ordereing? check store ioTripleOrder
        elif order == 'forceNone': order = None                                 # elif parent method forces no re-ordering: re-order is None
        if isinstance(order,list):                                              # if re-ordering list:
            if self._testTorder(order): order = TripleStore(tripleOrder=order)  #  and list valid: express as a TripleStore
            else: order = None                                                  #  otherwise: ignore re-ordering
        elif not isinstance(order,TripleStore): order = None                    # elif re-ordering not a TripleStore: ignore re-ordering
        if (order                                                               # if supplied re-order
        and order._getTripleOrder() == self._getTripleOrder()                   #  is not significant
            ): order = None                                                     #  : ignore re-ordering
        # process the triple
        for id,rc,ftr in processTriple(action,head,tail,mode,mtutils.sdict(),None,order):
            yield id,rc,ftr
    def _addTriple(self, t=None):
        # usage:
        #    adds a triple to the store with an id
        #    if new: add triple with new id
        #    elif versioned (check id - for timestamps):
        #        if new id: add it
        #        else: end
        #    else:
        #        retract the id from the stack and id_to_triples index
        # inputs:
        #    t    - triple elements
        # returns:
        #    id   - id of triple (or id) added, or duplicate not added
        #    rc   - result code of action; 0 - duplicate id not added, 1 - new id added
        self._showDebug(clas='TripleStore',method='_addTriple',note='inputs',line=1311,level=0,vars=[['t',t]])
        t1 = []
        f1 = []
        for elem in t:
            bits = self._parseURI(self,elem)
            self._showDebug(clas='TripleStore',method='_addTriple',note='inputs',line=1316,level=2,vars=[['bits',bits]])
            if 'has_nativeuri' in bits:
                t1 += [bits['has_nativeuri']]
                f1 += [bits['has_urifragment']]
            else: t1 = []; break
        if not t1: rc = id = 0
        else:
            id = str(self._addID(t1))                                           # id
            rc = 1                                                              # result code
            t1 = t1*2                                                           # double the triple - for algorithm index excess
            x = -1                                                              # setup manual loop of each triple item
            while x < 2:                                                        # loop thru 3 indexes: (attempting to istantiate the new triple in each)
                x += 1
                try:                                                            #  outer try to catch and notify any errors
                    try:                                                        #   try to instantiate the new triple in the current index
                        idx = self._indexes[x]                                  #    get this index
                        # maintain full text index
                        if (t1[x] not in self._db['t'][idx]                     #    if this triple element is new to TripleStore
                        and f1[x]                                               #     and it has a fragment value
                        and self._getFti()                                      #     and full text indexed
                            ): self._db['w']._addItem(f1[x],t1[x])              #     : add element to full text index
                        # maintain TripleStore
                        if t1[x+2] not in self._db['t'][idx][t1[x]][t1[x+1]]:   #    if new triple:
                            self._db['t'][idx][t1[x]][t1[x+1]][t1[x+2]] = [id]  #     add to index with its id
                            self._showDebug(clas='TripleStore',method='_addTriple',note='new added',line=1340,level=2,vars=[['id',id]])
                        elif self._getVersioned() is True:
                            if id not in self._db['t'][idx][t1[x]][t1[x+1]][t1[x+2]]:
                                self._db['t'][idx][t1[x]][t1[x+1]][t1[x+2]] += [id]
                                self._showDebug(clas='TripleStore',method='_addTriple',note='duplicate added',line=1344,level=2,vars=[['id',id]])
                            else:
                                x = 3
                                self._showDebug(clas='TripleStore',method='_addTriple',note='duplicate not added',line=1347,level=2,vars=[['id',id]])
                        else:
                            self._db['idstack'].append(int(id))
                            del self._db['i>t'][int(id)]
                            self._showDebug(clas='TripleStore',method='_addTriple',note='duplicate deleted',line=1351,level=2,vars=[['id',id]])
                            id = self._db['t'][idx][t1[x]][t1[x+1]][t1[x+2]][0]
                            x = 3
                            rc = 0
                    except: raise mterrors.AddTripleError(tuple(t))             #   except raise AddTripleError
                except mterrors.AddTripleError, X:                              #  except to trap the raised error
                    X._notify(c='TripleStore',
                              m='_addTriple()')                                 #   notify AddTripleError with params
                    rc = 0
                    break                                                       #   break from further attempted instantiation of failed triple
        if rc: self._addURIdata(t1,id)
        self._showDebug(clas='TripleStore',method='_addTriple',line=1362,level=1,vars=[["self._db['w']",self._db['w']]])
        self._showDebug(clas='TripleStore',method='_addTriple',note='returns',line=1363,level=0,vars=[['id',id],['rc',rc]])
        return id,rc
    def _deleteTriple(self, t=None, id=None):
        self._showDebug(clas='TripleStore',method='_deleteTriple',note='inputs',line=1366,level=0,vars=[['t',t],['id',id]])
        rc = 0
        if id is None and t:
            t1 = []
            f1 = []
            for elem in t:
                bits = self._parseURI(self,elem)
                if 'has_nativeuri' in bits:
                    t1 += [bits['has_nativeuri']]
                    f1 += [bits['has_urifragment']]
                else: t1 = []; break
            if t1: id = self._deleteID(t=t1)
        elif id:
            t1 = self._db['i>t'][id]
            id = self._deleteID(id=id)
        if t1 and id:
            rc = 1
            self._showDebug(clas='TripleStore',method='_deleteTriple',line=1382,level=1,vars=[['t',t],['id',id],['rc',rc]])
            t1 = t1*2
            for x in range(3):
                try:
                    # remove this id
                    self._db['t'][self._indexes[x]][t1[x]][t1[x+1]][t1[x+2]].remove(id)
                    self._showDebug(clas='TripleStore',method='_deleteTriple',note='deleting',line=1388,level=2,vars=[['id',id]])
                    # for each nested index if no values delete it
                    if len(self._db['t'][self._indexes[x]][t1[x]][t1[x+1]][t1[x+2]]) == 0:
                        del self._db['t'][self._indexes[x]][t1[x]][t1[x+1]][t1[x+2]]
                        self._showDebug(clas='TripleStore',method='_deleteTriple',note='deleting',line=1392,level=2,vars=[['t1[x+2]',t1[x+2]]])
                        if len(self._db['t'][self._indexes[x]][t1[x]][t1[x+1]]) == 0:
                            del self._db['t'][self._indexes[x]][t1[x]][t1[x+1]]
                            self._showDebug(clas='TripleStore',method='_deleteTriple',note='deleting',line=1395,level=2,vars=[['t1[x+1]',t1[x+1]]])
                            if len(self._db['t'][self._indexes[x]][t1[x]]) == 0:
                                del self._db['t'][self._indexes[x]][t1[x]]
                                self._showDebug(clas='TripleStore',method='_deleteTriple',note='deleting',line=1398,level=2,vars=[['t1[x]',t1[x]]])
                                # full text index maintenance (only if this element has been deleted)
                                if f1[x] and self._getFti():                            #     if full text indexed and fragment indexable:
                                    self._db['w']._deleteItem(f1[x],t1[x])
                                # remove other unwanted store indexes
                                if len(self._db['t'][self._indexes[x]]) == 0:
                                    del self._db['t'][self._indexes[x]]
                                    self._showDebug(clas='TripleStore',method='_deleteTriple',note='deleting',line=1405,level=2,vars=[['self._indexes[x]',self._indexes[x]]])
                except KeyError: pass
        self._showDebug(clas='TripleStore',method='_deleteTriple',note='returns',line=1407,level=0,vars=[['id',id],['rc',rc]])
        if rc: self._deleteURIdata(t1,id)
        return id,rc
    def _addURIdata(self,t,id):
        # usage:
        #    adds triple URI model data according to preferences
        # inputs:
        #    item - triple (expressed as a list or tuple).
        support = self._getURIsupport()
        if support == 'model':
            id1,rc1 = self._addTriple(t=self._rt(['UDCcontainer','contains','##'+str(id)]))
            if rc1:
                for elem in t:
                    for pred,bit in \
                    items(self._parseURI(self,elem,mode='parts')):
                        id2,rc2 = self._addTriple(t=[elem,pred,bit])
                        if rc2: self._addTriple(t=self._rt(['URIcontainer','contains',id2]))
    def _deleteURIdata(self,t,id):
        # usage:
        #    deletes triple URI model data according to preferences
        # inputs:
        #    item - triple (expressed as a list or tuple).
        support = self._getURIsupport()
        if support == 'model':
            id1,rc1 = self._deleteTriple(t=self._rt(['UDCcontainer','contains','##'+str(id)]))
            if rc1:
                for elem in t:
                    bits = self._parseURI(self,elem,mode='parts')
                    if (bits and not self._exists(queryList=[self._rt(('UDCcontainer'
                                                                      ,'contains'
                                                                      ,[(elem,'*','*'),('*',elem,'*'),('*','*',elem)]
                                                                       ))
                                                             ])):
                        for pred,bit in items(bits):
                            id2,rc2 = self._deleteTriple([elem,pred,bit])
                            if rc2: self._deleteTriple(self._rt(['URIcontainer','contains',id2]))
    def _addNamespace(self,ns,bs):
        support = self._getURIsupport()
        try:
            if support != 'off':
                r = self._splitURI(bs+'#'+ns)
                if r is not None:
                    bs = r[0]
                    ns = r[1]
                    try:
                        bs = r[0]
                        id,rc = self._addTriple(self._rt([bs,'has_urins',ns]))
                        if rc and support == 'model':
                            id,rc = self._addTriple(self._rt(['URIcontainer','contains',id2]))
                    except: raise mterrors.URInamespaceError(ns)
                else: raise mterrors.URIaddNamespaceError(ns,bs)
            else:
                try: raise mterrors.URIsupportOff()
                except mterrors.URIsupportOff, X:
                    X._notify(c='TripleStore',m='_addNamespace()')
                    raise mterrors.URIaddNamespaceError(ns,bs)
        except mterrors.URIerror, X:
            X._notify(c='TripleStore',m='_addNamespace()')
    def _deleteNamespace(self,ns,bs):
        support = self._getURIsupport()
        try:
            if support != 'off':
                r = self._splitURI(bs+'#'+ns)
                if r is not None:
                    bs = r[0]
                    ns = r[1]
                    try:
#                        ns = rensp.match(r[1]).group(0)
                        bs = r[0]
                        id,rc = self._deleteTriple(self._rt([bs,'has_urins',ns]))
                        if rc and support == 'model':
                            id,rc = self._deleteTriple(self._rt(['URIcontainer','contains',id2]))
                    except: raise mterrors.URInamespaceError(ns)
                else: raise mterrors.URIdeleteNamespaceError(ns,bs)
            else:
                try: raise mterrors.URIsupportOff()
                except mterrors.URIsupportOff, X:
                    X._notify(c='TripleStore',m='_deleteNamespace()')
                    raise mterrors.URIdeleteNamespaceError(ns,bs)
        except mterrors.URIerror, X:
            X._notify(c='TripleStore',m='_deleteNamespace()')
    def _deleteTriples(self, queryList=''):
        # usage:
        #    bulk deletes triples matching a supplied QueryList
        # inputs:
        #    queryList - QueryList instantiated or as pre-instantiated Python List and/or Tuple
        # returns:
        #    deleted   - list of deleted triple ids
        ids = []                                                                # prepare to collect the affected ids
        for t in self._triples(queryList=queryList):                            # for each unique entry matching the selection:
            if t:                                                               #  if valid:
                id = self._getIDfromTriple(t)[2:]                               #   get triple id (without prefix)
                if id: ids += [id]                                              #   accumilate list of ids to delete
        deleted = []                                                            # prepare to delete ids - listing deleted ids
        for id in ids:                                                          # for each id to be deleted:
            id,rc = self._deleteTriple(id=id)                                   #  delete it - getting the return code
            if rc: deleted += [id]                                              #  if deleted: add its id to those deleted
        return deleted                                                          # return deleted ids
    def _addID(self, t):
        if len(self._db['idstack']) == 0: id = 1
        else: id = self._db['idstack'].pop()
        if len(self._db['idstack']) == 0: self._db['idstack'].append(id+1)
        self._db['i>t'][id] = t                                                 # stored as a tuple
        self._db['upc'] += 1                                                    # increment updates count
        return id
    def _deleteID(self, t=None, id=None):
        # usage:
        #    deletes index of ids to triples stacking released id for reuse
        #    if id is supplied as input this gets used
        #    elif triple is supplied instead the id gets pulled from this
        #    also if deleted id is for a rule then it gets deleted from the id to rules index
        # inputs either:
        #    t  - triple for whome id is to deleted
        #    id - id to be deleted
        if id is None and t:                                                    # get id from triple
            idstr = self._getIDfromTriple(t)                                    #  as prefixed string
            if idstr: id = idstr[2:]                                            #  id without prefix
        elif id:
            idstr = '##'+str(id)                                                # else get string id from id
        if id:                                                                  # if id: proceed to delete related entries
            self._db['idstack'].append(id)                                      #  stack the id for later reuse
            del self._db['i>t'][int(id)]                                        #  del it from the
            if idstr in self._db['i>r']:                                        #  if a rule:
                del self._db['i>r'][idstr]                                      #   delete id string from rule index
        self._db['upc'] += 1                                                    # increment updates count
        return id                                                               # return the id
    def _expandTriple(self
                     ,t
                     ,expandRules=False
                     ,rulesAsTriple=False
                     ,errors=None
                     ,uri=None
                     ,target=None
                     ,order=None
                     ,orderToSelf=False
                     ,update=True
                      ):
        # usage:
        #    recursively expands triples or triple elements supporting a variety of controls
        # inputs:
        #    t             - element or triple to be expanded
        #    expandRules   - include the rhs of rules in the expansion [True|False]?
        #    rulesAsTriple - express embedded rules as Triples (rather than pairs using dictionary syntax)
        #    errors        - mark rule errors in expanded (commented) outputs
        #    uri           - express uri in the following formats:
        #                     - native             use has_nativeuri (or just the current format)
        #                     - forcenative        same as native but forces a transformation even where the source and target stores are the same
        #                     - export             use has_rdfuri
        #                     - nativealias        use has_displayuri (same as has_nativeuri, but swaps bases for namespaces where specified)
        #    target        - target store for which uri's are to be represented (default is self)
        #    order         - TripleStore object to which the ordering of triples should conform (typically self, target or None to ignore)
        #    orderToSelf   - direction of any re-ordering:
        #                     - False (default) if order is target order ie. for export
        #                     - True            if order is source order ie. for import
        #    update        - update default exporterrors settings [True|False]
        # returns:
        #    t             - the expanded element or triple
        def expandTriple(self,t,expandRules,rulesAsTriple,errors,uri,target,order,orderToSelf):
            self._showDebug(clas='TripleStore',method='_expandTriple',note='.expandTriple inputs',line=1565,level=0,vars=[['t',t],['expandRules',expandRules],['errors',errors]])
            # interpret string elements
            id = None                                                           # initialise id as None
            if isinstance(t,basestring):                                        # if triple element is a string:
                if t[:2] == '##':                                               #  if its a triple_id:
                    id = int(t[2:])                                             #   get id as integer
                    self._showDebug(clas='TripleStore',method='_expandTriple',note=',expandTriple before expand',line=1571,level=2,vars=[['t',t],['t[2:]',t[2:]]])
                    t = tuple(self._db['i>t'][id])                              #   get the triple from the id
                    self._showDebug(clas='TripleStore',method='_expandTriple',note='.expandTriple after expand',line=1573,level=2,vars=[['t',t]])
                else:                                                           #  else triple element isn't an id:
                    try:                                                        #   try checking if a string representation
                        t1 = eval(t)                                            #    of someother structure: eg. list, dict, tuple
                        if (isinstance(t1,dict)
                         or isinstance(t1,tuple)
                         or isinstance(t1,list)
                            ): t = t1                                           #    if so triple element is that structure
                    except: pass
            # expand interpretted triple
            if isinstance(t,list):                                              # if triple element is a list:
                for c in range(len(t)):                                         #  expand each element of that list
                    t[c] = expandTriple(self,t[c],expandRules,rulesAsTriple,errors,uri,target,order,orderToSelf)
            elif isinstance(t,dict):                                            # elif triple element is a dict:
                t1 = {}                                                         #  initialise replacement dict
                for lhs,rhs in t.items():                                       #  and populate by expanding each lhs:rhs pair
                    t1[expandTriple(self,lhs,expandRules,rulesAsTriple,errors,uri,target,order,orderToSelf)] = \
                    expandTriple(self,rhs,expandRules,rulesAsTriple,errors,uri,target,order,orderToSelf)
                t = t1                                                          #  set triple element to replacement dict
            elif isinstance(t,tuple):                                           # elif triple element is a tuple (triple):
                rule = ''                                                       #  prepare to expand an associated rule (if any)
                if expandRules:                                                 #  if rules are to be expanded:
                    if not id: id = self._getIDfromTriple(t)                    #   get triple id if not already known:
                    if id in self._db['i>r']:                                   #   if id of a rule: get the rule from the id..
                        rule = self._db['i>r'][id]                              #    and set triple element to the expanded rule
                        t = rule._express(asTriple=rulesAsTriple,errors=errors,uri=uri,sourceStore=self,targetStore=target,orderStore=order,orderToSelf=orderToSelf)
                if not rule:                                                    #  if no rule: (treat as a "data" triple)
                    t = list(t)                                                 #   turn into a list
                    if order is not None:                                       #   if new order specified:
                        t = self._rt(t,order=order._getTripleOrder(),toself=orderToSelf
                                     )                                          #    re-order accordingly
                    for c in range(len(t)):                                     #   triple is triple with each element expanded
                        t[c] = expandTriple(self,t[c],expandRules,rulesAsTriple,errors,uri,target,order,orderToSelf)
                    t = tuple(t)                                                #   return triple to tuple
            # singe element? test to flip its uri expression
            elif (uri is not None                                               #  if switching stores or uri formats:
              and isinstance(t,basestring)
              and self._getURIsupport() != 'off'
              and uri in self._uriouts
              and (uri != 'native' or target != self)
                  ):
                t = self._parseURI(target,t)[self._uriouts[uri]]                #   re-express the uri to the target store/uri format
            self._showDebug(clas='TripleStore',method='_expandTriple',note='.expandTriple returns',line=1615,level=0,vars=[['t',t]])
            return t
        self._showDebug(clas='TripleStore',method='_expandTriple',note='inputs',line=1617,level=0,vars=[['t',t],['expandRules',expandRules],['errors',errors]])
        self._showDebug(clas='TripleStore',method='_expandTriple',note='inputs',line=1618,level=0,vars=[['uri',uri],['target',target]])
        if target is None: target = self
        if update:
            self._update(exporterrors=errors)                                   # update exporterrors setting if needbe
            errors = self._getExporterrors()                                    # get updated exporterrors
        if (order == self
         or (order and order._getTripleOrder() == self._getTripleOrder())
            ): order = None                                                     # if order is self: set to None to skip re-odering
        t1 = copy.deepcopy(t)                                                   # preserve original input before expanding the input
        t1 = expandTriple(self,t1,expandRules,rulesAsTriple,errors,uri,target,order,orderToSelf)
        self._showDebug(clas='TripleStore',method='_expandTriple',note='returns',line=1628,level=0,vars=[['t1',t1]])
        return t1                                                               # return the expanded input
    def _getIDfromTriple(self,t):
        idstr = ''
        if isinstance(t,basestring): idstr = t
        elif ((isinstance(t,list) or isinstance(t,tuple))
          and len(t) == 3
          and self._indexes[0] in self._db['t']
          and t[0] in self._db['t'][self._indexes[0]]
          and t[1] in self._db['t'][self._indexes[0]][t[0]]
          and t[2] in self._db['t'][self._indexes[0]][t[0]][t[1]]
              ): idstr = '##'+str(self._db['t'][self._indexes[0]][t[0]][t[1]][t[2]][0])
        return idstr
    def _toString(self):
        s = ''
        for k1 in self._db['t']:
            s += 'Triple Index: '+str(self._expandTriple(k1))+'\n'
            for k2 in self._db['t'][k1]:
                s += ' > '+str(self._expandTriple(k2))+'\n'
                for k3 in self._db['t'][k1][k2]:
                    s += ' > > '+str(self._expandTriple(k3))+'\n'
                    for k4 in self._db['t'][k1][k2][k3]:
                        s += ' > > > '+str(self._expandTriple(k4))+'\n'
                        for id in self._db['t'][k1][k2][k3][k4]:
                            if '##'+str(id) in self._db['i>r']:
                                id = ':- '+str(self._db['i>r']['##'+str(id)]._express(ordered=True))
                            else: id = ':- '+str(id)
                            s += ' > > > > '+id+'\n'
        s += 'Id to Triples index:\n'
        for k1 in self._db['i>t']: s += ' > '+str(k1)+':'+str(self._db['i>t'][k1])+'\n'
        return s
    def _generate(self
                 ,action=None
                 ,queryList=''
                 ,rulesAsTriple=False
                 ,errors=None
                 ,uri=None
                 ,target=None
                 ,order=None
                 ,update=True
                  ):
        # usage:
        #    wrapper collating and returning yielded generator results
        #    typically an alternative to _export() returning entire output in one go
        # inputs:
        #    file          - export file [mtutils.FlatFile object|None] - None uses default exportfile
        #    action        - action to insert at col 0 of each row (if any)
        #    queryList     - _queryList() query. Default is generate everything
        #    rulesAsTriple - express embedded rules as Triples (rather than pairs using dictionary syntax)
        #    errors        - mark rule errors in expanded (commented) outputs
        #    update        - update default exportfile and exporterrors settings [True|False]
        #    uri           - express uri in the following formats:
        #                     - native             use has_nativeuri (or just the current format)
        #                     - forcenative        same as native but forces a transformation even where the source and target stores are the same
        #                     - export (default)   use has_rdfuri
        #                     - nativealias        use has_displayuri (same as has_nativeuri, but swaps bases for namespaces where specified)
        #    target        - target store for which uri's are to be represented
        #    order         - TripleStore object to which the ordering of triples should conform (typically self, target or None to ignore)
        # returns:
        #    s             - collated result string
        s = ''
        for s1 in self._generator(action=action
                                 ,queryList=queryList
                                 ,errors=errors
                                 ,export=False
                                 ,uri=uri
                                 ,target=target
                                 ,order=update
                                 ,update=update
                                  ): s += s1
        return s
    def _export(self
               ,file=None
               ,action=None
               ,queryList=''
               ,rulesAsTriple=False
               ,errors=None
               ,uri='export'
               ,target=None
               ,order=None
               ,update=True
               ,fm=None
               ,o=None
                ):
        # usage:
        #     wrapper for generator to export yielded results to file
        #     TripleStore._save('filename'?, [triple]?, 'add|delete'??)
        #     where [triple] may be an empty list
        # inputs:
        #    file          - export file [mtutils.FlatFile object|None] - None uses default exportfile
        #    action        - action to insert at col 0 of each row (if any)
        #    queryList     - _queryList() query. Default is generate everything
        #    rulesAsTriple - express embedded rules as Triples (rather than pairs using dictionary syntax)
        #    errors        - mark rule errors in expanded (commented) outputs
        #    uri           - express uri in the following formats:
        #                     - native             use has_nativeuri (or just the current format)
        #                     - forcenative        same as native but forces a transformation even where the source and target stores are the same
        #                     - export (default)   use has_rdfuri
        #                     - nativealias        use has_displayuri (same as has_nativeuri, but swaps bases for namespaces where specified)
        #    target        - target store for which uri's are to be represented
        #    order         - list or TripleStore object to which the ordering of triples should conform (typically self, target, or None to ignore)
        #    update        - update default exportfile, exporterrors and ioTripleOrder settings [True|False]
        # returns:
        #    1             - done
        #    0             - failed
        #
        # prepare class and method parameter settings
        if isinstance(order,list):
            if self._testTorder(order): ots = TripleStore(tripleOrder=order)
            else: ots = order = None
        elif isinstance(order,TripleStore):
            ots   = order
            order = order._getTripleOrder()
        else: ots = order = None
        if update: self._update(exportfile=file,exporterrors=errors,ioTripleOrder=order)
        if file   is None: file   = self._getExportfile()
        if errors is None: errors = self._getExporterrors()
        if order  is None: order  = self._getIoTripleOrder()
        if ots is None and order: ots = TripleStore(tripleOrder=order)
        # export
        fn = file._getFullname()
        if fn:
            if fm is None: fm = 'w'
            f = open(fn,fm)
            for c,s in enumerate(self._generator(rulesAsTriple=rulesAsTriple
                                                ,errors=errors
                                                ,action=action
                                                ,queryList=queryList
                                                ,update=False
                                                ,uri=uri
                                                ,target=target
                                                ,order=ots
                                                ,forceReset=True
                                                 )):
                if not c:
                    if order is None: ol = self._getTripleOrder()
                    else: ol = ots._getTripleOrder()
                    if ol != o:
                        os = ''
                        for i in ol: os += i+','
                        f.write(toc.replace('.,.,.',os[:-1])+'\n')
                        o = ol
                f.write(s)
            f.close()
        return o
    def _generator(self
                  ,action=None
                  ,queryList=''
                  ,rulesAsTriple=False
                  ,errors=None
                  ,update=True
                  ,uri=None
                  ,target=None
                  ,order=None
                  ,forceReset=None
                   ):
        # usage:
        #    triple output generator
        #    e.g. for export
        # inputs:
        #    action        - action to insert at col 0 of each row (if any)
        #    queryList     - _queryList() query. Default is generate everything
        #    rulesAsTriple - express embedded rules as Triples (rather than pairs using dictionary syntax)
        #    errors        - mark rule errors in expanded (commented) outputs
        #    update        - update default exportfile and exporterrors settings [True|False]
        #    uri           - express uri in the following formats:
        #                     - native             use has_nativeuri (or just the current format)
        #                     - forcenative        same as native but forces a transformation even where the source and target stores are the same
        #                     - export             use has_rdfuri (default, if export is True)
        #                     - nativealias        use has_displayuri (same as has_nativeuri, but swaps bases for namespaces where specified)
        #    target        - target store for which uri's are to be represented
        #    order         - TripleStore object to which the ordering of triples should conform (typically self, target or None to ignore)
        #    forceReset    - force cache reset regardless of other constraints [True|False]
        # outputs:
        #    multiline string of matching predicates in the desired protocol
        self._showDebug(clas='TripleStore',method='_generator',note='inputs',line=1792,level=0,vars=[['action',action],['queryList',queryList]])
        if isinstance(action,basestring): action = action.lower()               # get lowercase action string
        if action in actkey: action = actkey[action]                            # get consistent action
        if action != 'add' and action != 'delete': action = ''
        else: action += ', '
        for t in self._triples(queryList=queryList,forceReset=forceReset):      # for each entry matching the selection:
            if t:                                                               #  if valid:
                t1 = self._expandTriple(t
                                       ,expandRules=True
                                       ,rulesAsTriple=rulesAsTriple
                                       ,errors=errors
                                       ,update=update
                                       ,uri=uri
                                       ,target=target
                                       ,order=order
                                        )
                if t1:
                    t1 = action+str(t1)
                    self._showDebug(clas='TripleStore',method='_generator',note='yields',line=1810,level=0,vars=[['t1',t1]])
                    yield t1+'\n'                                               #    yield fact string (with linefeed)
    def _import(self
               ,file=None
               ,mode=None
               ,update=True
               ,order=None
                ):
        # usage:
        #    loads and actions triples from .csv filename
        # input:
        #    file      - source file (.csv format) - set to update default
        #    mode      - action when the import duplicates existing rules (merge|keep|replace) - set to update default
        #    update    - update default importfile, importmode and ioTripleOrder settings [True|False]
        #    order     - list or TripleStore object to which the ordering of imported triples should conform (typically self, target, or None to ignore)
        # returns:
        #    processed - number of [lines, items, triples] processed
        # notes:
        #    processed triples does not necessarily correspond to number of affected triples as some may be duplicates and actions vary
        #    import file may:
        #     - be commented (full lines or line suffixes)
        #    rules may presented as:
        #     - a single predicate with lhs EquationList, or
        #     - seperate predicates for each lhs Equation
        #
        # prepare class and method parameter settings
        if isinstance(order,list):
            if not self._testTorder(order): order = None
        elif isinstance(order,TripleStore): order = order._getTripleOrder()
        else: order = None
        if update: self._update(importmode=mode,importfile=file,ioTripleOrder=order)
        if mode  is None: mode  = self._getImportmode()
        if file  is None: file  = self._getImportfile()
        if order is None: order = self._getIoTripleOrder()
        self._timportmode    = mode                                             # mode is supplied but not to be updated (pass to processTriple avoiding actionTriple)
        self._tioTripleOrder = order
        # import
        triples = lines = items = 0
        for line in file._getValues(strip=['suffix']):
            if not line.startswith('#'): isdata = True
            else:
                isdata = False
                try:
                    o = tocre.match(line).group(1)
                    if o:
                        o = mtutils._stripsplit(o)
                        if (self._testTorder(o)
                        and o != self._getTripleOrder()
                        and o != order
                            ):
                            self._tioTripleOrder = order = o
                except: pass
            if isdata:
                if not isinstance(line,list): line = [line]
                done = False
                for item in line:
                    t = self._actionTriple(item)
                    if t:
                        triples += len(t)
                        items += 1
                        done = True
                if done: lines += 1
        self._timportmode    = None                                             # remember to reset mode passing variable to None
        self._tioTripleOrder = None
        processed = [lines,items,triples]
        return processed
    def _solveQueryList(self,queryList='',vs={},gr=None,rikeys=None,infer=None,forceReset=None):
        # usage:
        #    solves QueryLists - that is a set of alternative Queries either for triples matches or rules
        # inputs:
        #    queryList  - not present default to everything
        #                 a tuple: assume this is a single Query so put in a list
        #                 a list: assume its a list of Queries OR QueryList expressed as tuples
        #                 all others do nothing ie empty list
        #    vs         - query element expressions indexed by rule variables (for substition by Query._makeKey())
        #                 ie. value setting dependencies inherited from linked queries
        #    gr         - generic rule identifier (if applicable)
        #    rikeys     - recursed infered keys - tracing recursive inference
        #    infer      - Infer missing facts from rules. [None|True|False|'ffi'].
        #                  If None Query._solve() eventually uses config item 'stores_infer' instead.
        #                  _export() sets infer to False via _triples().
        #    forceReset - force cache reset regardless of other constraints [True|False]
        # yields:
        #    triples, rules and bindings from _solveQuery tuple by tuple
        self._showDebug(clas='TripleStore',method='_solveQueryList',note='inputs',line=1885,level=0,vars=[['queryList',queryList]])
        self._showDebug(clas='TripleStore',method='_solveQueryList',note='inputs',line=1886,level=0,vars=[['gr',gr],['mtquery._expandVS(vs)',mtquery._expandVS(vs)],['vs',vs]])
        if not isinstance(queryList,mtquery.QueryList):                         # if query list not instantiated:
            queryList = mtquery.QueryList(match=queryList)                      #  Note: instantiate a non-unique QueryList - ensures it always gets re-solved
            self._showDebug(clas='TripleStore',method='_solveQueryList',note='inputs',line=1889,level=2,vars=[['queryList',queryList]])
        self._showDebug(clas='TripleStore',method='_solveQueryList',line=1890,level=1,vars=[['queryList._expandMatch()',queryList._expandMatch()]])
        if queryList:
            self._newEQLR_luw(infer=infer,forceReset=forceReset)
            self._newEQL_luw()
            self._newEQ_luw()
            for t,r,b in queryList._solve(self
                                         ,vs=vs
                                         ,gr=gr
                                         ,rikeys=rikeys
                                         ,infer=infer
                                          ):                                    #  solve the QueryList
                self._showDebug(clas='TripleStore',method='_solveQueryList',note='yields',line=1901,level=0,vars=[['t',t],['r',r],['b',b]])
                yield t,r,b
    def _solveTriple(self,aquery,useIndex,parentStore=None,rd=None,infer=None,rs={}):
        # usage:
        #    wrapper for _solveTriple1() which initialises added variables and enables it to be invoked recursively
        #    _solveTriple1() being a solution generic to more than Triples
        # inputs:
        #    aquery      - Query to be executed from which store specific search keys will be derived
        #    useIndex    - list of efficiency rated search index types for each triple element (ranked in ascending order 1-best, 9-worst)
        #    parentStore - parent triple store                                        if distributed store
        #    rd          - current inference recursion depth                          if QueryExpressions need solving
        #    infer       - Queryable specific inference [True|False|None|'ffi']       if QueryExpressions need solving
        #    rs          - return substitutions dict                                  if QueryExpressions need solving
        # yields:
        #    store       - list of stores sourcing these results (contains just self)
        #    t           - matching triples (as tuples)
        #    b           - matching bindings (as an sdict)
        #    i           - match specific inference
        next_col  = lambda c: (c+1)%3
        self._showDebug(clas='TripleStore',method='_solveTriple',line=1920,note='inputs',level=0,vars=[['aquery._expandMatch()',aquery._expandMatch()],['useIndex',useIndex]])
        self._showDebug(clas='TripleStore',method='_solveTriple',line=1921,note='inputs',level=0,vars=[['self',self],['parentStore',parentStore]])
        self._showDebug(clas='TripleStore',method='_solveTriple',line=1922,note='inputs',level=0,vars=[['rd',rd],['infer',infer],['rs',rs]])
        # map triple element orders between parentStore and self
        sto_c  = self._getTripleOrder()                                         # current triple ordering       offset -> type
        stoi_c = self._getStoi()                                                # current triple ordering index type   -> offset
        if parentStore is None or parentStore == self:                          # if no parentStore or also the sourceStore:
            sto_p  = sto_c                                                      #  parent triple ordering = current triple ordering
            stoi_p = stoi_c                                                     #  parent triple ordering index = source offset index
        else:                                                                   # else: (get these seperately for the parentStore)
            sto_p  = parentStore._getTripleOrder()
            stoi_p = parentStore._getStoi()
        # select triple index for self
        uI = [[stoi_c[sto_p[c]],v] for c,v in enumerate(useIndex)]              #   collate indexes by element
        uI.sort(key=itemgetter(1))                                              #   sort indexes by efficiency
        if uI[0][1] == uI[1][1] and abs(uI[0][0]-uI[1][0]) > 1: io = 2          #    if elements 0 and 2 top priority: start with 2
        else: io = uI[0][0]                                                     #    else: start index with top priority element
        # prepare keys for selected triple index
        tkeys = mtutils.slist()                                                 #   prepare match key for searching triple store
        los_c = mtutils.slist()                                                 #   maps offsets in key to current store triple ordering
        los_p = mtutils.slist()                                                 #   maps offsets in current to parent store triple ordering
        tkeys[0] = io                                                           #   1st key is triple index type [012, 120, 201]
        los_c[0] = io                                                           #   1st key<->current offset map value is offset of index type
        los_p[0] = stoi_p[sto_c[io]]                                            #   1st current<->parent offset map value
        aqelms = aquery._getMatch()                                             #   get QueryElements sourcing the the key
        for c in range(len(aqelms)):                                            #   derive remaining keys
            tkeys[c+1] = aqelms[los_p[c]]._getMatch()                           #    next key (1st key is index type)
            los_c[c+1] = next_col(los_c[c])                                     #    next key<->current offset map value
            los_p[c+1] = stoi_p[sto_c[los_c[c+1]]]                              #    next current<->parent offset map value
        tkeys[0] = [self._idxqe[tkeys[0]]]                                      #   convert 1st key to the search index label
        # do search
        self._showDebug(clas='TripleStore',method='_solveTriple',line=1951,level=2,vars=[['mtquery._expandKeys(tkeys)',mtquery._expandKeys(tkeys)],['tkeys',tkeys]])
        bound = mtutils.slist([[mtutils.sdict()]]*len(tkeys))                   #   initial bindings index settings
        for t,b,i in self._solveTriple1(copy.deepcopy(self._db['t'])
                                     ,1
                                     ,4
                                     ,tkeys
                                     ,bound
                                     ,parentStore
                                     ,rd
                                     ,infer
                                     ,rs
                                      ):
            # express matched triple and inference list in parentStore order
            t1 = mtutils.slist()                                                #    prepare re-ordered match triple
            i1 = mtutils.slist()                                                #    prepare re-ordered match triple Element inference data
            for c,e in enumerate(t):                                            #    foreach enumerated triple element
                t1[los_p[c]] = e                                                #     re-order the triple element
                i1[los_p[c]] = i[c]                                             #     re-order the triple element inference value
            self._showDebug(clas='TripleStore',method='_solveTriple',line=1969,note='yields',level=0,vars=[['t1',t1],['b',b],['i1',i1]])
            yield [self],tuple(t1),b,i1
    def _solveTriple1(self,index,s,e,keys,bound,parentStore,rd,infer,rs):
        # background:
        #    a version of sdict._yieldMatch which "knows" enough of the semantics of triples to handle nested triples
        # usage:
        #    matches multilevel index of arbitrary depth to list of keys
        #    supports nested query structures, complex element expressions and
        #    lists of alternative element expressions
        # inputs:
        #    s           - start of range of keys in index
        #    e           - end of range of keys in index
        #    keys        - lists of keys between depths s(tart) and e(nd) matching supplied list of keys
        #    bound       - is a list of inherited bindings that corresponds to keys
        #    parentStore - parent triple store                                        if distributed store
        #    rd          - current inference recursion depth                          if QueryExpressions need solving
        #    infer       - Queryable specific inference                               if QueryExpressions need solving
        #    rs          - return substitutions dict                                  if QueryExpressions need solving
        # yields:
        #    array of index matches, variable bindings, and match specific inference
        def tsearch(qlist,parentStore,rd,infer,rs,op,vars=None,index=None):
            # Usage:
            #    gets bindings indexed by ids of triples matching the input list of triple queries
            # Inputs:
            #    qlist       - nested QueryList to solve
            #    parentStore - parent store possibly DTS
            #    rd          - recursion depth for passing on
            #    infer       - store inference setting
            #    rs          - return substitutions dict
            #    op          - comparator for this selection [=|!=]
            #    vars        - external variables to be bound to matches
            #    index       - current triple store index
            # Returns:
            #    found/index - matching bindings indexed by triple ids
            #    hasBindings - found contains variale bindings [True|False]
            #    fromIndex   - found is the triple index [True|False]
            self._showDebug(clas='TripleStore',method='_solveTriple1',note='.interpret.tsearch inputs',line=2005,level=0,vars=[['qlist',qlist]])
            found = qlist._getTIDB(parentStore
                                      ,rd=rd
                                      ,infer=infer
                                      ,vars=vars
                                      ,rs=rs
                                       )                                        # get found bindings solving qlist
            if op == '!=' and index:                                            # if these are not required: (remove them from index)
                for tid in found:                                               #  for each matching triple_id:
                    tid1 = self._normaliseVal(tid,parentStore)                  #   normalise triple_id to that of self
                    if tid1 in index: del index[tid1]                           #   and delete it from the index if present
                return index,False,True                                         #  return the index,fromIndex=True,hasBinding=False
            else: return found,True,False                                       # else: return found bindings,fromIndex=False,hasBindings=True
        def interpret(index,qexp,parentStore,rd,infer,rs):
            # usage:
            #    replaces following code from stores11.py
            #    if keys and dummy == '*': bv = ''; this1 = index
            #    elif keys and dummy[:1] == '?': bv = dummy[1:]; this1 = index
            #    else: this1 = [dummy]; bv = ''
            # inputs:
            #    index       - remaining TripleStore index dimensions
            #    qexp        - QueryExpression to interpret and match with index - extracted from keys
            #    parentStore - parent store possibly DTS
            #    rd          - recursion depth for passing on
            #    infer       - store inference setting
            #    rs          - return substitutions dict
            # returns:
            #    index|bindings
            #    hasBindings - {True|False]
            #    fromIndex   - [True|False]
            def csearch(index,vop,val,parentStore):
                # generator yielding keys in index
                # matching simple comparator value OR list
                self._showDebug(clas='TripleStore',method='_solveTriple1',note='.interpret.csearch inputs',line=2038,level=0,vars=[['index',index],['vop',vop],['val',val]])
                cval = []                                                       # holds final match objects
                for v in val:                                                   # iterate through value set
                    if v != '*':                                                #  skip any wild searches since non wild ones exist
                        if v.startswith('/') and v.endswith('/'):               #   if its a regex value
                            ep = mtutils._splitRegex(v)                         #    strip outer regex parenthesis
                            try:                                                #    try processing the regex:
                                ec,maxp = mtutils._pdepth(ep[0])                #     count and validate inner parenthesis
                                if ec == 1: raise mterrors.UnbalancedParenthesisError(ep[0]) #test error code to raise errors
                                elif ec == 2: raise mterrors.UnspecifiedParenthesisError()
                                try: cval += [[re.compile(ep[0]),ep,maxp[0]]]   #     try compiling it into a regex object
                                except: raise mterrors.ExpressionError(ep[0])   #     escalate failure
                            except mterrors.ExpressionError, X:
                                X._notify(c='TripleStore',
                                          m='_solveTriple1.csearch()')          #    notify ExpressionError
                        else: cval += [[v]]                                     #   else its a string match
                l = len(cval)                                                   # get new comparator list length minus omitted
                if vop == '=' or vop == '~': vop = '='+vop                      # set equals to python equals comparator
                op = vop
                results = []                                                    # prepare to collate list of matching results
                for k in index:                                                 # for each key in this index
                    bt = parentStore._parseURI(self,k)                          #  re-express key according to URI parts
                    f = bt['has_urifragment']
                    c = -1                                                      #  prepare manual loop through comparators
                    while c+1 < l:                                              #  for each comparator object
                        c += 1
                        cv = cval[c][0]                                         #  set cv - default comparator value
                        if isinstance(cv,basestring) and vop[-1] == '~':        #  if its (not)like a string
                            op = vop[:-1]+'='                                   #   flip like to '='
                            if f.find(cv) > -1: cv = f                          #   prepare cv for final test
                            else: cv = ''
                        elif not isinstance(cv,basestring):                     #  if its not a string its a regex comparator value
                            f = bt['has_nativeuri']                             #   note regex evaluated on nativeuri
                            if vop[-1] == '~': op = vop[:-1]+'='                #   if its a like regex expression flip it to '='
                            ep = cval[c][1]
                            pc = cval[c][2]
                            if cv.match(f):                                     #   if a regex match
                                if (op == '=='                                  #    if equality based comparison or
                                 or op == '!='                                  #     inequality or
                                 or (len(ep) < 2 and pc == 0)): cv = f          #     or no extract groups set cv to this key
                                else:                                           #    else set cv to the group specified in the regex
                                    o,cv = mtutils._evalRegex(f,cv,ep=ep)       #     get match from regex with(out) substitutions
                            elif op == '==' or op == '!=': cv = ''              #   elif equality based comparison set cv to null
                        if eval('f'+op+'cv'):                                   #  if match against the comparator operator
                            c = l                                               #   look no further for this key
                            results += [bt['has_nativeuri']]                    #   collate native uri results
                return results                                                  # return results
            def esearch(index,vop,sval,eop,eval,parentStore):
                # generator yielding keys in index
                # where key values match expression is true or false as required
                self._showDebug(clas='TripleStore',method='_solveTriple1',note='.interpret.esearch inputs',line=2088,level=0,vars=[['index',index],['vop',vop],['sval',sval],['eop',eop],['eval',eval]])
                cval = []
                for v in [sval,eval]:
                    if v.startswith('/') and v.endswith('/'):
                        cval += [re.compile(sval[1:-1])]
                    else: cval = [v]
                results = []                                                    # prepare to collate list of matching results
                for k in index:
                    bt = parentStore._parseURI(self,k)                          #  re-express key according to URI parts
                    f = bt['has_urifragment']
                    val = []
                    c = -1
                    while c+1 < len(cval):
                        c += 1
                        if isinstance(cval[c],basestring): val += [cval[c]]
                        elif cval[c].match(f):
                            val += cval[c].match(f).group(1)
                        else: val = []; c = len(cval)
                    if val:
                        r = eval('val[0]'+eop+'val[1]')
                        if ((vop[:1] == '!' and not r) or
                            (vop[:-1] == '=' and r)
                            ):
                            results += [bt['has_nativeuri']]                    #    collate native uri results
                return results                                                  # return results
            self._showDebug(clas='TripleStore',method='_solveTriple1',note='.interpret inputs',line=2113,level=0,vars=[['index',index],['qexp',qexp]])
            self._showDebug(clas='TripleStore',method='_solveTriple1',note='.interpret',line=2114,level=1,vars=[['qexp._expandMatch()',qexp._expandMatch()]])
            bv       = qexp._getVars()                                          #  get bound variable list
            bindings = qexp._getBindings()                                      #  get bindings of pre-solved QueryExpressions
            if bindings: return bindings,bv,True,False                          #  if bindings: return as result + bv,hasBindings=True,fromIndex=False
            op       = qexp._getNop()                                           #  get logical comparater operand
            vals     = qexp._getVals()                                          #  get values
            valexp   = qexp._getValexp()                                        #  get regex value expressions
            triples  = qexp._getTriples()                                       #  get QueryLists value expression
            hasBindings = False                                                 # by default the returned iterator has no bindings
            fromIndex = True
            this1 = index                                                       # iterator = received triple index
            keys = mtutils.slist()                                              # initialise empty index keys list
            if valexp:                                                          #  if a comparator value expression exits use it
                sval = valexp['<sval>'][0]
                eop  = valexp['<eop>'][0]
                val  = valexp['<val>'][0]
                this1 = esearch(index,eop,sval,op,val,parentStore)              #   iterator = index key expression search generator
            elif triples:                                                       #  elif triples specified:
                this1,hasBindings,fromIndex = tsearch(triples
                                                     ,parentStore
                                                     ,rd
                                                     ,infer
                                                     ,rs
                                                     ,op
                                                     ,vars=bv
                                                     ,index=this1
                                                      )                         #   iterator = ids linked to internal bindings
            elif vals:                                                          #  if comporator values exist potentially use them
                fromIndex = False
                this2 = mtutils.slist()                                         #   new results iterator
                c = -1                                                          #      (since candidate iterator may get regected later)
                optype = compdx[op]
                while c+1 < len(vals):                                          #   for each key value to be matched
                    c += 1
                    val = vals[c]
                    self._showDebug(clas='TripleStore',method='_solveTriple1',note='.interpret',line=2149,level=1,vars=[['op',op],['val',val]])
                    if val != '*':                                              #    if not wild:
                        if ((optype != '='                                      #     if not an equates based match operator
                         and (optype != '~' or not self._db['w'])               #      and not a like match or no fulltext index
                         and (optype != '>' or self._getStructure() == 'dict')
                             )
                         or (val.startswith('/') and val.endswith('/'))         #      or a regex match
                            ):                                                  #      : proceed
                            this2 = this2._union(csearch(index
                                                        ,op
                                                        ,vals[:]
                                                        ,parentStore
                                                         ))                     #      collate matches from a comparative search
                            self._showDebug(clas='TripleStore',method='_solveTriple1',note='.interpret',line=2162,level=2,vars=[['this1',this1],['op',op]])
                            c = len(vals)                                       #      no need to check further
                        elif optype == '=':                                     #     elif an equals based match:
                            val1 = parentStore._parseURI(self
                                                        ,val
                                                         )['has_nativeuri']     #      get native parent stored form of match value
                            if op == '=': this2 += [val1]                       #      if equals: use this (it'll be tested by invoker)
                            else:                                               #      else anything but: use indexed unification
                                if not c: fromIndex = True
                                if val1 in this1: del this1[val1]               #       if this in index copy: delete it
                        elif optype == '~':                                     #     elif (un)like based match using full text index:
                            if not keys: keys += [key for key in this1]         #      1st time get index keys
                            keys1 = copy.deepcopy(keys)                         #      copy index keys for results processing
                            val1 = parentStore._parseURI(self,val)\
                                    ['has_urifragment']                         #      get fti match value from uri_fragment
                            uris = self._db['w']._matchItem(parentStore._db['w']
                                                           ,val1
                                                           ,op
                                                            )
                            if op == '~': this2 += keys1._intersection(uris)    #      if like: keep matching uris also in this2
                            else: this2 += keys1._difference_update(uris)       #      else: exclude matching uris from this2
                        elif optype == '>':                                     #     else: do comparative matching using tree index
                            this1 = this1._extractSubTree(op,val)               #      extract the matching sub-tree (as copy)
                            fromIndex = True                                    #      flag results are indexed
                            c = len(vals)                                       #      no need to check further (just one val allowed)
                    elif op == '=':                                             #    if matching wild:
                        fromIndex = True
                        c = len(vals)                                           #     no need to check further
                if not fromIndex: this1 = this2
            self._showDebug(clas='TripleStore',method='_solveTriple1',note='.interpret returns',line=2191,level=0,vars=[['this1',this1],['bv',bv]])
            return this1,bv,hasBindings,fromIndex                               # return the interator, bound variable and iterator types
        if parentStore is None: parentStore = self
        self._showDebug(clas='TripleStore',method='_solveTriple1',note='inputs',line=2194,level=0,vars=[['index',index],['s',s],['e',e],['bound',bound]])
        self._showDebug(clas='TripleStore',method='_solveTriple1',note='inputs',line=2195,level=0,vars=[['mtquery._expandKeys(keys)',mtquery._expandKeys(keys)],['keys',keys]])
        if e > 0:                                                               # if not at end of key range:
            if keys:                                                            #  if keys exist:
                self._showDebug(clas='TripleStore',method='_solveTriple1',line=2198,level=1,vars=[['keys',keys]])
                this = keys[0]                                                  #   prepare stage 1 iterator from keys
                if isinstance(this[0],list):
                    this = this[0]
                    keys[0] = this
                self._showDebug(clas='TripleStore',method='_solveTriple1',line=2203,level=2,vars=[['len(bound[0])',len(bound[0])],['len(this)',len(this)]])
                if len(bound[0]) < len(this):                                   #   prepare bindings list
                    bound[0] = mtutils.slist(bound[0])
                    for c in range(len(bound[0]),len(this)): bound[0][c] = bound[0][0]
                self._showDebug(clas='TripleStore',method='_solveTriple1',note='Preparing to test for nested web queries',line=2207,level=1,vars=[['this',this],])
            else: this = index                                                  #  else: stage 1 iterator is remaining triples index
            self._showDebug(clas='TripleStore',method='_solveTriple1',line=2209,level=1,vars=[['this',this],['bound[0]',bound[0]]])
            c = -1                                                              #  prepare results counter
            for qexp in this:                                                   #  for each item in iterator:
                i1 = qexp._getInfer()                                           #   get inference associated with this QueryExpression
                fromIndex = True
                if isinstance(qexp,mtquery.QueryList):                          #   if an unbound nested triple: (evaluate)
                    bv = []                                                     #    set bound variables list to empty = unbound
                    this1,hasBindings,fromIndex = tsearch(qexp
                                                         ,parentStore
                                                         ,rd
                                                         ,infer
                                                         ,rs
                                                         ,'='
                                                          )
                else: this1,bv,hasBindings,fromIndex = interpret(index
                                                                ,qexp
                                                                ,parentStore
                                                                ,rd
                                                                ,infer
                                                                ,rs
                                                                 )              #   else: interpret iterator, variables, iterator properties
                self._showDebug(clas='TripleStore',method='_solveTriple1',line=2230,level=1,vars=[['keys',keys],['c',c]])
                self._showDebug(clas='TripleStore',method='_solveTriple1',line=2231,level=1,vars=[['this1',this1],['bv',bv],['hasBindings',hasBindings],['fromIndex',fromIndex]])
                for k1 in this1:                                                #   for each item in stage 2 iterator: (assumed from match not index)
                    self._showDebug(clas='TripleStore',method='_solveTriple1',line=2233,level=1,vars=[['k1',k1]])
                    if fromIndex:                                               #    if instead from index: (switch iterators)
                        k = k1                                                  #     set index iterator (k) to this iterator
                        k1 = parentStore._normaliseVal(k,self)                  #     get match value iterator (k1) by expressing (k) for parent store
                    else: k = self._normaliseVal(k1,parentStore)                #    else: also get index iterator from (k1) - null if non existant
                    self._showDebug(clas='TripleStore',method='_solveTriple1',line=2238,level=1,vars=[['k',k],['k1',k1]])
                    if k and k in index:                                        #    if item valid for current subset: proceed (it may not be if derived from tsearch())
                        c += 1                                                  #     increment item counter
                        self._showDebug(clas='TripleStore',method='_solveTriple1',line=2241,level=1,vars=[['e',e],['c',c],['keys',keys],['bv',bv],['bound',bound]])
                        self._showDebug(clas='TripleStore',method='_solveTriple1',line=2242,level=2,vars=[['c',c]])
                        if hasBindings: b1 = copy.deepcopy(this1[k1])           #     if index keys already bound: use them (will be target native uris)
                        else:                                                   #     or prepare to get them:
                            if parentStore != self:                             #      if source and target stores different:
                                k1 = self._parseURI(parentStore                 #       get nativeuri for the parent (target) store
                                                   ,k1)['has_nativeuri']        #       (otherwise k1 already is the nativeuri of the target)
                            b1 = mtutils.sdict()                                #      initialise bindings dict
                        self._showDebug(clas='TripleStore',method='_solveTriple1',line=2249,level=2,vars=[['b1',b1],['c',c]])
                        if keys and bv:                                         #     if item itself bound to variables
                            for tbv in bv: b1[tbv] = k1                         #      add these to the item bindings
                            self._showDebug(clas='TripleStore',method='_solveTriple1',line=2252,level=2,vars=[['b1',b1],['c',c]])
                        if c >= len(bound[0]) or not bound[0][c]:               #     check if bound list cells need initialising
                            bound[0] = mtutils.slist(bound[0])                  #      with autovivication dicts
                            bound[0][c] = {}
                        ok = 1                                                  #     assume bindings unify ok
                        if b1 or bound[0][c]:                                   #     but if possible changes: (re-check)
                            self._showDebug(clas='TripleStore',method='_solveTriple1',line=2258,level=2,vars=[['bound[0][c]',bound[0][c]]])
                            b1 = b1._matchUnion(bound[0][c])                    #      unify bindings of this item with stored bindings
                            if not b1: ok = 0                                   #      if unify fails: bindings don't unify ok
                        if ok:                                                  #     if bindings unified ok: proceed further with item
                            bound[0][c] = b1                                    #      set stored bindings to unified bindings
                            self._showDebug(clas='TripleStore',method='_solveTriple1',line=2263,level=1,vars=[['b1',b1],['bound[0][c]',bound[0][c]]])
                            if index[k]:                                        #      item exists in k, if further indexed: proceed
                                if e > 1:                                       #       if next index within end search range:
                                    self._showDebug(clas='TripleStore',method='_solveTriple1',line=2266,level=2,vars=[['index[k]',index[k]],['keys[1:]',keys[1:]],['bound[1:]',bound[1:]]])
                                    for o,b,i in self._solveTriple1(index[k]
                                                                     ,s-1
                                                                     ,e-1
                                                                     ,keys[1:]
                                                                     ,bound[1:]
                                                                     ,parentStore
                                                                     ,rd
                                                                     ,infer
                                                                     ,rs
                                                                      ):        #        for triples,bindings,inference from next key/index:
                                        self._showDebug(clas='TripleStore',method='_solveTriple1',line=2277,level=1,vars=[['o',o],['b',b],['i',i]])
                                        self._showDebug(clas='TripleStore',method='_solveTriple1',line=2278,level=2,vars=[['b1',b1],['s',s],['e',e]])
                                        ok = 1                                  #         assume bindings valid
                                        if b1 or b:                             #         but check
                                            b = b._matchUnion(b1)               #          by unifying
                                            if not b: ok = 0                    #          if can't unify: bindings set to invalid
                                        if ok:                                  #         if valid bindings:
                                            if s < 1:                           #          if outside start search range:
                                                o[0:0] = [k1]                   #           insert this triple value
                                                i[0:0] = [i1]                   #           insert this inference value
                                            self._showDebug(clas='TripleStore',method='_solveTriple1',note='yields',line=2287,level=0,vars=[['o',o],['b',b],['i',i]])
                                            yield o,b,i
                                else:                                           #       else next index outside end search range:
                                    self._showDebug(clas='TripleStore',method='_solveTriple1',note='yields',line=2290,level=0,vars=[['k1',k1],['b1',b1],['i1',i1],['e',e]])
                                    yield [k1],b1,[i1]                          #        so yield what it has
    def _normaliseVal(self,sourceVal,sourceStore):
        # usage:
        #    re-expresses a source value from a source store in terms of a unique value for this store
        #    in practice only the ids of nested triples get re-expressed since all atomic values are already unique
        # inputs:
        #    sourceVal   - source value as triple or triple element - anything which _expandTriple can accept
        #    sourceStore - store in which the source value is unique
        # returns:
        #    tv          - target value (for this store)
        if sourceStore == self: return sourceVal                                # if source and target stores are the same: return value as is
        tv = sourceVal                                                          # initialise target value = source value
        if isinstance(sourceVal,basestring) and sourceVal[:2] == '##':          #  if source value is a triple id:
            try: tv = self._getIDfromTriple(sourceStore._expandTriple(sourceVal))   #   try: getting the corresponding id for this store
            except: tv = None                                                   #   except: None target value
        return tv                                                               # return the target value
    def _close(self):
        if isinstance(self._db,mtutils.ODBMS):
            self._db._close()
    def _commit(self):
        if isinstance(self._db,mtutils.ODBMS):
            self._db._commit()

    def _showDebug(self,
                   clas='',
                   method='',
                   note='',
                   vars=[],
                   line='',
                   level=2):
        mtdebug.Debug()._notify(clas=clas,method=method,note=note,line=line,level=level,vars=vars)

class DistTripleStore(TripleStore, mtstruct.A_DistTripleStore):
    _default_queryStores = [TripleStore()]                                      # Note: order query stores in order of preference as sources for rules
    _metricfile_path     = mtconfig._interpretItem('stores_DTSmetricfile_path',TripleStore._metricfile_path)
    _metricfile_name     = mtconfig._interpretItem('stores_DTSmetricfile_name',TripleStore._metricfile_name)
    _metricfile_type     = mtconfig._interpretItem('stores_DTSmetricfile_type',TripleStore._metricfile_type)
    _default_metricfile  = mtutils.Flatfile(path=_metricfile_path
                                           ,name=_metricfile_name
                                           ,type=_metricfile_type
                                            )
    _default_showmetrics = mtprefs._interpretItem('stores_DTSshowmetrics'       # report metrics [yes|no]
                                                 ,TripleStore._default_showmetrics)
    _default_rulesmode   = mtprefs._interpretItem('stores_DTSrulesmode'
                                                 ,'merge',2)                    # mode for handling conflicting versions of rules

    def __init__(self
                ,queryStores=None
                ,rulesmode=None
                ,loadfile=None
                ,unloadfile=None
                ,dbname=None
                ,dbreset=None
                ,URIsupport=None
                ,URIbasesuffix=None
                ,structure=None
                ,exporterrors=None
                ,importmode=None
                ,importfile=None
                ,exportfile=None
                ,tripleOrder=None
                ,ioTripleOrder=None
                 ):
        if dbname is not None:
            fn = TripleStore._default_dbpath+dbname+'.'+TripleStore._default_dbtype
            if dbreset is True: mtutils._deleteFiles(fn+'*')
            self._db = mtodbms.DBstore(fn)
        else: self._db = mtutils.sdict()
        if not self._db:                                                        # if no persistent data: (initialise it)
            if structure   is not None: self._setStructure(structure)
            if tripleOrder is not None: self._setTripleOrder(tripleOrder)       #  !! set self._tripleOrder after self._db test !!..
            self._reset()
        elif not cpersist:                                                      # elif persistence doesn't include inference caches: (reset them)
            if tripleOrder is not None: self._setTripleOrder(tripleOrder)       #  !! set self._tripleOrder after self._db test !!
            self._db['crs'] = mtindex.Index()                                   #  outcomes cache - rule  successes
            self._db['crf'] = mtindex.Index()                                   #  outcomes cache - rule  failures
            self._db['cqs'] = mtindex.Index()                                   #  outcomes cache - query successes
            self._db['cqf'] = mtindex.Index()                                   #  outcomes cache - query failures
        # outcomes caches structure: {logical or physical query key:{{bindings}:[triples,rules,{bindings}]},{more results},..]}
        #  - outcomes which are inprogress will have their intermeadiate results cached here indexed by their physical query key
        #  - outcomes which have been fully resolved have their final results cached here indexed by a logical query key
        #    in which case previously cached intermediate results are deleted as no longer needed.
        self._crs = mtindex.Index()                                             # transient outcomes cache - rule  successes (physically keyed)
        self._crf = mtindex.Index()                                             # transient outcomes cache - rule  failures  (physically keyed)
        self._cqs = mtindex.Index()                                             # transient outcomes cache - query successes (physically keyed)
        self._cqf = mtindex.Index()                                             # transient outcomes cache - query failures  (physically keyed)
        # progress caches for queries or rules producing intermediate results
        # structure {logical key:[resolution recursion depth,[unique intermediate physical keys,..]]}
        # Note: self._cqs, self._cqf and self._pqcache not exploited in all versions of query.py
        self._pqcache = mtindex.Index()                                         # in progress query cache  {qkey:[..[..,..,..]]}
        self._prcache = mtindex.Index()                                         # in progress rules cache {iqkey:[..[..,..,..]]}
        # Persistence normally causes all the DTS attributes to be stored
        # However because nested QueryStores may themselves be persistent this causes ZODB to loop
        # therefore nested QueryStores are reset and must be specified by the calling routine each time
        # a DTS is opened. This makes sense for other reasons as it offers users the flexibility:
        #  - to support persistence at lower levels - ie in the nested stores
        #  - to mix persistent and transient stores
        #  - to change DTS structure - ie open a DSTS on a variety of underlying stores
        #    (in this latter case users should also submit a cache rest request - as inference caches will no longer match)
        self._setQueryStores()
        self._FFItrigger = False                                                # FFItrigger is off by default
        self._update(queryStores=queryStores
                    ,rulesmode=rulesmode
                    ,loadfile=loadfile
                    ,unloadfile=unloadfile
                    ,URIsupport=URIsupport
                    ,URIbasesuffix=URIbasesuffix
                    ,exporterrors=exporterrors
                    ,importmode=importmode
                    ,importfile=importfile
                    ,exportfile=exportfile
                    ,ioTripleOrder=ioTripleOrder
                     )
    def _reset(self):
        # usage:
        #    initialise or empty store contents
        #    called by self.__init__()
        #    can be used to reset a store to its empty state
        tripleOrder = self._getTripleOrder()                                    #   but outside of _update() since it must not be updatable.
        structure   = self._getStructure()
        self._db['us']  = TripleStore(structure=structure
                                     ,tripleOrder=tripleOrder
                                      )                                         #  native data to this store
        self._db['rs']  = TripleStore(structure=structure
                                     ,tripleOrder=tripleOrder
                                      )                                         #  result store TripleStore (run-time and infered triples)
        self._db['w']   = mtfti.fti()                                           #  fulltext index = nativeURIs indexed by words
        self._db['cts'] = time.time()                                           #  creation timestamp - serves as an identifier together with size
        self._db['irv'] = mtutils.slist()                                       #  inference relevance validation list - holds (cts,upc,size) for each active store on last inference
        self._db['crs'] = mtindex.Index()                                       #  outcomes cache - rule  successes
        self._db['crf'] = mtindex.Index()                                       #  outcomes cache - rule  failures
        self._db['cqs'] = mtindex.Index()                                       #  outcomes cache - query successes
    def __add__(self,s):
        self._actionQueryStores('add',s)
        return self
    def __sub__(self,s):
        self._actionQueryStores('delete',s)
        return self
    def _update(self
               ,queryStores=None
               ,rulesmode=None
               ,loadfile=None
               ,unloadfile=None
               ,URIsupport=None
               ,URIbasesuffix=None
               ,exporterrors=None
               ,importmode=None
               ,importfile=None
               ,exportfile=None
               ,ioTripleOrder=None
                ):
        if queryStores   is not None: self._setQueryStores(queryStores)
        if rulesmode     is not None: self._setRulesmode(rulesmode)
        if loadfile      is not None: self._setLoadfile(loadfile)
        if unloadfile    is not None: self._setUnloadfile(unloadfile)
        if URIsupport    is not None: self._setURIsupport(URIsupport)
        if URIbasesuffix is not None: self._setURIbasesuffix(URIbasesuffix)
        if exporterrors  is not None: self._setExporterrors(exporterrors)
        if importmode    is not None: self._setImportmode(importmode)
        if importfile    is not None: self._setImportfile(importfile)
        if exportfile    is not None: self._setExportfile(exportfile)
        if ioTripleOrder is not None: self._setIoTripleOrder(ioTripleOrder)
    def _setQueryStores(self,*qs):
        if not qs: self._queryStores = []
        else: self._queryStores = mtutils._flatten(list(qs),t=TripleStore)
        return self._queryStores
    def _getQueryStores(self):
        return self._queryStores
    def _setRulesmode(self,*args):
        return mtutils._genericSetter(self,'rulesmode',args,m=['merge','keep','retain','first'])
    def _getRulesmode(self,default=True):
        return mtutils._genericGetter(self,'rulesmode',default)
    def _resetActiveQueryStores(self):
        self._activeQueryStores = None
        return self._activeQueryStores
    def _getActiveQueryStores(self,ius=True,irs=False,dts=True,filter=True,testdts=False):
        # usage:
        #    gets a list of nested "leaf" TripleStores containing triples
        #    resolves nested DistTripleStores (DTS)
        #    includes the update TripleStore for this and any nested DTS if it contains triples
        # inputs:
        #    ius     - include DTS update stores (True|False]
        #    irs     - include DTS result (and ffi data) stores [True|False|'root']
        #              'root' includes it for the root store only
        #    dts     - include stores from nested DTS [True|False]
        #    filter  - filter stores with no data [True|False]
        #    testdts - test if store nests other distributed stores
        # returns:
        #    if testdts = True:
        #        ndts - store nests other distributed stores [True|False]
        #        acs  - list of all TriplesStores containing triples
        #    if testdts = False:
        #        acs  - list of all TriplesStores containing triples
        def filtered(s,f):
            # usage:
            #    if filtering check if store has triples
            # inputs:
            #    s - store triple index to check
            #    f - filter [True|False]
            # returns:
            #    triples found [True|False]
            return not f or ('t' in s._db and s._db['t'])
        # End filtered()
        k = (str(ius),str(irs),str(filter))
        acs = None
        ndts = False
        iacs = getattr(self,'_activeQueryStores',None)
        if iacs is None: self._activeQueryStores = {}
        elif k in iacs: acs = iacs[k]
        if acs is None:
            acs = []
            for qs in self._getQueryStores():
                if filtered(qs,filter) and qs not in acs: acs += [qs]
                elif isinstance(qs,DistTripleStore):
                    if testdts: ndts = True
                    if dts:
                        if irs == 'root': drs = 'False'
                        else: drs = irs
                        acs += qs._getActiveQueryStores(ius=ius,irs=drs,dts=dts)
            if ius:
                us1 = self._db['us']
                if filtered(us1,filter) and us1 not in acs: acs += [us1]
            if irs:
                rs1 = self._db['rs']
                if filtered(rs1,filter) and rs1 not in acs: acs += [rs1]
            self._activeQueryStores[k] = acs
        if testdts: return ndts,acs
        else: return acs
    def _actionQueryStores(self, action, *args):
        # usage takes one or more of any TripleStore object and adds or substracts it to this DSTS
        self._showDebug(clas='DistTripleStore',method='_actionQueryStores',note='inputs',line=2513,level=0,vars=[['action',action],['args',args]])
        action1 = 'add'
        if isinstance(action,basestring):
            action = action.lower()
            if action in actkey: action1 = actkey[action]
        if args:
            args = mtutils._flatten(args,t=TripleStore)
            for s in args: eval('self._'+action1+'QueryStore(s)')
        return self._getQueryStores()
    def _addQueryStore(self,s):
        qs = self._getQueryStores()
        if s not in qs: qs += [s]
        self._setQueryStores(qs)
    def _deleteQueryStore(self,s):
        qs = self._getQueryStores()
        if qs:
            if s in qs: qs.remove(s)
            self._setQueryStores(qs)
    def _actionTriple(self,*args):
        ids = []
        us = self._db['us']
        if us: ids = us._actionTriple(*args)
        return ids
    def _processTriple(self,action,head,tail,mode,newRules):
        us = self._db['us']
        if us:
            for id,rc,ftr in us._processTriple(action,head,tail,mode,newRules):
                yield id,rc,ftr
    def _addTriple(self, t=None):
        rc = id = 0
        us = self._db['us']
        if us: id,rc = us._addTriple(t=t)
        return id,rc
    def _deleteTriple(self, t=None, id=None):
        rc1 = id1 = 0
        us = self._db['us']
        if us: id1,rc1 = us._deleteTriple(t=t,id=id)
        return id1,rc1
    def _deleteTriples(self, queryList=''):
        deleted = []
        us = self._db['us']
        if us: deleted = us._deleteTriples(queryList=queryList)
        return deleted
    def _expandTriple(self
                     ,t
                     ,expandRules=False
                     ,errors=None
                     ,uri=None
                     ,target=None
                     ,order=None
                      ):
        # usage:
        #    DistTripleStore wrapper for TripleStore._expandTriple()
        #    recursively expands triples or triple elements supporting a variety of controls
        # inputs:
        #    t           - element or triple to be expanded
        #    expandRules - include the rhs of rules in the expansion [True|False]?
        #    errors      - mark rule errors in expanded (commented) outputs
        #    uri         - express uri in the following formats:
        #                   - native             use has_nativeuri (or just the current format)
        #                   - forcenative        same as native but forces a transformation even where the source and target stores are the same
        #                   - export             use has_rdfuri
        #                   - nativealias        use has_displayuri (same as has_nativeuri, but swaps bases for namespaces where specified)
        #    target      - target store for which uri's are to be represented (default is self)
        #    order       - TripleStore object to which the ordering of triples should conform (typically self, target or None to ignore)
        # returns:
        #    t           - the expanded element or triple
        acs = self._getActiveQueryStores(filter=False)
        if acs and len(acs) == 1: s = acs[0]
        else: s = self._db['rs']
        return s._expandTriple(t,expandRules=expandRules,errors=errors,uri=uri,target=target,update=False)
    def _getIDfromTriple(self,t):
        acs = self._getActiveQueryStores(filter=False)
        if acs and len(acs) == 1: s = acs[0]
        else: s = self._db['rs']
        try: idstr = rs._getIDfromTriple(t)
        except:
            id,rc = self._db['rs']._addTriple(t=t)
            idstr = '##'+str(id)
        return idstr
    def _normaliseVal(self,sourceVal,sourceStore):
        # usage:
        #    re-expresses a source value from a source store in terms of a unique value for this store
        #    in practice only the ids of nested triples get re-expressed since all atomic values are already unique
        # inputs:
        #    sourceVal   - source value as triple or triple element - anything which _expandTriple can accept
        #    sourceStore - store in which the source value is unique
        # returns:
        #    tv          - target value (for this store)
        acs = self._getActiveQueryStores()                                      # get the active query stores
        if acs and len(acs) == 1: return sourceVal                              # if just one: return target value as source value
        tv = sourceVal                                                          # initialise target value = source value
        if isinstance(sourceVal,basestring) and sourceVal[:2] == '##':          # if source value is a triple id:
            try: tv = self._getIDfromTriple(sourceStore._expandTriple(sourceVal)
                                            )                                   #  try: getting the corresponding id for this store
            except: tv = None                                                   #  except: None target value
        return tv                                                               # return the target value
    def _toString(self):
        acs = self._getActiveQueryStores(ius=False)
        if acs and len(acs) == 1: return acs[0]._toString()
        for c,qs in enumerate(self._getActiveQueryStores(ius=False)):
            print ('QueryStore '+str(c+1),qs)
            print (qs._toString())
        us = self._db['us']
        if us:
            print ('UpdateStore')
            print (us._toString())
        print ('ResultStore')
        print (self._db['rs']._toString())
    def _export(self
               ,scope=['update','foreign','nested']
               ,file=None
               ,action=None
               ,queryList=''
               ,rulesAsTriple=False
               ,errors=None
               ,uri=None
               ,target=None
               ,order=None
               ,update=True
                ):
        # usage:
        #    exports selected triples from a distributed store
        #    according to scope
        # inputs:
        #    scope         - which Triple Stores to export from any of [update|results|foreign|nested]
        #                    default is ['update','foreign','nested'] = everything but intermediate and ffi data (if any)
        #    file          - export file [mtutils.Flatfile object|None] - None uses default exportfile
        #    action        - action prefix for triples [add|delete] (if any)
        #    queryList     - query list as Python structure or mtquery.QueryList object for selecting data to export (null exports all)
        #    rulesAsTriple - express embedded rules as Triples (rather than pairs using dictionary syntax)
        #    errors        - mark rule errors in expanded (commented) outputs
        #    uri           - express uri in the following formats:
        #                     - native             use has_nativeuri (or just the current format)
        #                     - forcenative        same as native but forces a transformation even where the source and target stores are the same
        #                     - export (default)   use has_rdfuri
        #                     - nativealias        use has_displayuri (same as has_nativeuri, but swaps bases for namespaces where specified)
        #    target        - target store for which uri's are to be represented
        #    order         - ordering of elements in exported triples [None|'self'|'source'|store|[list]] where:
        #                      - None is interpreted as 'self' ie. self._getTripleOrder()
        #                      - 'source' exports triples in same order as they are stored - which could be mixed order with each labelled (see below)
        #                      - TripleStore object to which ordering should conform
        #                      - list specifying a bespoke triple element ordering
        #                      export file will include comment lines identifying the order of the triples following it. These lines are interpretted by import.
        #    update        - update default exportfile, exporterrors and ioTripleOrder settings [True|False]
        # returns:
        #    ok            - status code [0 - filed|1 - ok]
        # notes:
        #    does not filter output or merge rules
        #    matching content exported as is
        #    exports data only - no settings.
        #     - To save settings use _unload() or better still make the DTS persistent.
        #     - May add an XML export option with settings option later.
        #
        # prepare class and method parameter settings
        o = None
        if order == 'source': o = order; order = None
        elif order is None or order == 'self': o = self; order = None
        if isinstance(order,list):
            if not self._testTorder(order): order = None
        elif isinstance(order,TripleStore): order = order._getTripleOrder()
        else: order = None
        if update: self._update(exportfile=file,exporterrors=errors,ioTripleOrder=order)
        if file   is None: file   = self._getExportfile()
        if errors is None: errors = self._getExporterrors()
        if order is None:
            if o is None: order  = self._getIoTripleOrder()
            elif o == self: order = self
        # validate/interpret scope
        ius = irs = dts = False
        if 'update' in scope: ius = True
        if 'results' in scope: irs = True
        if 'nested' in scope: dts = True
        if 'foreign' in scope: acs = self._getActiveQueryStores(ius=ius,irs=irs,dts=dts)
        else:
            acs = []
            if ius: acs += [self._db['us']]
            if irs: acs += [self._db['rs']]
        o  = None
        ol = []
        for c,qs in enumerate(acs):
            if c: fm = 'a'
            else: fm = None
            o = qs._export(file=file
                          ,action=action
                          ,queryList=queryList
                          ,rulesAsTriple=rulesAsTriple
                          ,errors=errors
                          ,update=False
                          ,uri='export'
                          ,target=self
                          ,order=order
                          ,fm=fm
                          ,o=o
                           )
            if o: ol += [o]
        return ol
    def _import(self,file=None,mode=None,order=None,update=None):
        # usage:
        #    imports data from source file to DTS update triple store
        # inputs:
        #    file      - import file (should be mtutils.Flatfile object, or None to use default import file)
        #    mode      - action when the import duplicates existing rules (merge|keep|replace) - set to update default
        # returns:
        #    processed - number of [lines, items, triples] processed
        #
        # prepare class and method parameter settings
        if isinstance(order,list):
            if not self._testTorder(order): order = None
        elif isinstance(order,TripleStore): order = order._getTripleOrder()
        else: order = None
        if update: self._update(importmode=mode,importfile=file,ioTripleOrder=order)
        if mode  is None: mode  = self._getImportmode()
        if file  is None: file  = self._getImportfile()
        if order is None: order = self._getIoTripleOrder()
        # delegate import
        return self._db['us']._import(file=file,mode=mode,order=order,update=False)
    def _solveTriple(self,aquery,useIndex,rd=None,infer=None,rs={}):
        # usage:
        #    DSTS wrapper for STS._solveTriple()
        #    submits the query to each active query store yielding matched facts first
        #    and unique rules last ordered from specific to generic
        # inputs:
        #    keys  - triple match criteria
        #    rd          - current inference recursion depth                          if QueryExpressions need solving
        #    infer       - Queryable specific inference [True|False|None|'ffi']       if QueryExpressions need solving
        #    rs          - return substitutions dict                                  if QueryExpressions need solving
        # yields:
        #    qsi   - list of source query stores (list needed if multiple versions of a rule are found for merging)
        #    t     - matched triple
        #    b     - matched values bound to query vareiables
        #    i     - match specific inference
        # note:
        #    all returned values are unique for the DSTS
        if (self._getNestedDTS()
        and self._getFFImaint() == 0
        and infer is not False
            ): dts = True; urs = 'root'
        else:
            if infer == 'ffi': dts = False                                      # if generating feed forward inference data:
            else: dts = True                                                    #  exclude nested DTS from this (each generates its own)
            if infer is False: irs = False                                      #  set rs to boolean of infer
            else: irs = True
        acs = self._getActiveQueryStores(irs=irs,dts=dts)                       # get the active query stores
        if len(acs) == 1:                                                       # if just one active query store process as an STS
            for qsi,t,b,i in acs[0]._solveTriple(aquery,useIndex,parentStore=self,rd=rd,rs=rs
                                                 ):
                yield qsi,t,b,i
        else:                                                                   # else multiple active query stores: (process as a DSTS)
            i_rules = {}                                                        #  initialise rules cache
            for qs in acs:                                                      #  for each active store:
                for qsi,t,b,i in qs._solveTriple(aquery,useIndex,parentStore=self,rd=rd,rs=rs
                                                 ):                             #   for each matching source store, triples, bindings, inference:
                    isrule = 0                                                  #    initialise generic rule variable counter
                    for e in t:                                                 #    for each element of matched triple:
                        if e == '?': isrule += 1                                #     count the generic rule variables
                    if isrule:                                                  #    if any rule variables found: (cache rule for later)
                        mode = self._getRulesmode()                             #     get the DSTS rules mode
                        if (isrule,t) not in i_rules:                           #     if rule not cached:
                            if mode != 'first' or qs == acs[0]:                 #      if its either the first querystore or any store is ok
                                i_rules[(isrule,t)] = [qsi,b,i]                 #       cache rule (source, bindings and inference) indexed by (var count and triple)
                        elif mode == 'replace':                                 #     elif already cached but replacable:
                            i_rules[(isrule,t)] = [qsi,b,i]                     #      then replace it in the cache
                        elif mode == 'merge':                                   #     elif mergable: add source to source list in cache
                            l_qs = i_rules[(isrule,t)][0]
                            if qs not in l_qs:
                                i_rules[(isrule,t)] = [l_qs+qsi,b,i]
                    else: yield qsi,t,b,i                                       #    else: yield fact source, triple, bindings, inference
            for (isrule,t),[qsi,b,i] in sorted(i_rules.items()):                # yield rules last sorted most specific first
                yield qsi,t,b,i
    def _close(self):
        # usage:
        #    closes the DB connection of this and all nested persistent stores
        # note: TripleStore._close() tests if store is persistent before closing the DB connection
        for ac in self._getQueryStores(): ac._close()                           # close each nested store (which may itself be a DTS)
        TripleStore._close(self)                                                # close this explicitly via its parent method
    def _getFFI(self): return ifedforw
    def _getNestedDTS(self):
        try: n = self._nestedDTS
        except AttributeError:
            n,d = self._getActiveQueryStores(testdts=True)
            self._nestedDTS = n
        return n
    def _getFFImaint(self):
        # usage:
        #    wraps _getFFI() into a further test of the FFI rebuild trigger
        # returns:
        #    if no FFI - returns None
        #    else returns the FFIpercentageChangeTrigger setting
        if not self._getFFI(): return None
        else:
            f = ffimaint
            if not f and self._getNestedDTS() and not ffinestd: f = 0.001
            return f
    def _resetCaches(self):
        # usage:
        #    if this or any nested store has been updated since the inference caches - reset the caches concerned
        # returns:
        #    reset - caches reset [True|False]
        reset = False
        irvc = self._db['irv']
        irvs = mtutils.slist()
        ndts,acs = self._getActiveQueryStores(testdts=True)
        for ac in acs:
            dummy,irv = ac._testirv()
            irvs += [irv]
        self._nestedDTS = ndts
        irvs1 = irvc._symmetric_distance(irvs)
        self._showDebug(clas='DistTripleStore',method='_resetCaches',line=2799,level=1,vars=[['irvs',irvs],['ndts',ndts]])
        self._showDebug(clas='DistTripleStore',method='_resetCaches',line=2800,level=1,vars=[['irvs1',irvs1]])
        if irvs1:
            reset = True
            TripleStore._resetCaches(self,irv=irvs)
            f = self._getFFImaint()
            if f is None: pass
            elif f == 0 or not irvc: self._resetFFI(trigger=True)
            elif f < 100: self._triggerFFI(irvs)
        return reset
    def _triggerFFI(self,irv):
        # usage:
        #    compares the perecentage change in the store to that required to trigger FFI rebuild.
        #    if triggered then sets _FFItrigger to True
        # inputs:
        #    irv - latest irv value to compare with stored value to determine percentage change
        # returns:
        #    trigger FFI rebuild [True|False]
        f = self._getFFImaint()
        if f is not None:
            s1 = s2 = 0
            for (c,u,s) in self._db['irv']: s1 += s
            for (c,u,s) in irv: s2 += s
            if s1 > s2: s = s1; sl = s2; s2 = s
            cf = s1/s2*100
            if cf > f: self._FFItrigger = True
            self._showDebug(clas='DistTripleStore',method='_triggerFFI',line=2825,level=1,vars=[['cf',cf],['f',f],['self._FFItrigger',self._FFItrigger]])
    def _resetFFI(self,trigger=False):
        # usage:
        #    resets the FFI according the mainentance preference
        #    if maint is an any change it performs a full rebuild
        #    else a partial rebuild
        #    resets _FFItrigger to False
        # inputs:
        #    trigger - optional {True|False]. If True forces the FFI to rebuild regardless of _FFItrigger value
        #                                     Else rebuilds the FFI if _FFItrigger is True
        # returns:
        #    reset   - was the FFI rest [True|False]
        if trigger or self._FFItrigger:
            f = self._getFFImaint()
            if f is not None:
                reset = True
                if f == 0: request = [[('?sub','?pred','?obj')]
                                     ,['not',('?sub==*','?pred==*','?obj==*')]
#                                     ,['not',('?sub == ?','?pred==*','?obj==*')
#                                            ,('?sub==*','?pred = =?','?obj==*')
#                                            ,('?sub==*','?pred==*','?obj==?')]
                                     ]
                else: request = [[('?sub=?','?pred','?obj'),('?sub','?pred=?','?obj'),('?sub','?pred','?obj=?')]]
                mtrules.Result(request=request
                              ,outputs=[mtrender.Sequence(pattern=[('?sub', '?pred', '?obj')]
                                                         ,targets=[self._db['rs']]
                                                          )])._generate(store=self,infer='ffi')
                self._FFItrigger = False
        else: reset = False
        return reset

'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

Created on 28 Jan 2009
Last Updated on 10 July 2010

As test20 with tests of:
    rules instantiation and query inference

Related:
    test20r-00   - rules via recursion, compound rules, recursive rules no
    test20r-01   - rules via recursion, compound rules, recursive rules via value interpolation
    test20r-02   - rules via recursion, compound rules, recursive rules via 2 stage interpolation
    test20r-03   - rules via recursion, compound rules, recursive rules via 2 stage interpolation + feed forward inference
    test20r-04   - rules via recursion, compound rules, recursive rules via reduced 2 stage interpolation + value feeding between QueryLists
                    works for bounded recursion:
                    deepcopy _solveTriple1(index) and _solveEquation new vs for next QueryList
    test20r-05   - as test20r-04 but tests reduced bindings support
    test20r-06   - as test20r-05 but tests multi variable, listed and tuple query element expressions
                    & local rule var naming convention
    test20r-07   - as test20r-06 taking use of local rule variable naming convention to support direct use of
                    query variables within rules. Note: this doesn't seem to cope with local variables which
                    on recursion themselves become query variables
    test20r-08   - as test20r-06 without local variables and with revised rule._interpolate()/_interpolate1()
                    supporting passing lists and triples to rule query elements. !!Bug in solving nested triples!!
    test20r-09   - as test20r-08 addressing !!Bug in solving nested triples!!
                    - triples nested in query element lists work
                    - triples in rule query elements still FAIL
    test20r-10   - as test20r-09 supporting
                    - bound nested triples
                    - nested triples syntax
                    - cached retreival of nested triples
    test20r-11   - as test20r-10 supporting 'tsearchcache' from new Transients singleton
    test20r-12   - as test20r-11 supporting re-engineered use of None for null params and empty values
    test20r-13   - as test20r-12 but with _solveQuery() key list revisions supporting dual inferred/not inferred
                    querying of rules. However, (?s, ?p, ?o) returns all only supplied facts (NO inferred facts)
    test20r-14   - as test20r-13 but (?s, ?p, ?o) returns all supplied AND inferred facts
                    query variables bound to rule values.
    test20r-15   - as test20r-14 but supports:
                    1. NOT clauses in queries and rules (via negated QueryLists in QueryEquations)
                    2. automated NOT clause re-ordering
                    3. automated recursive lhs rule clause re-ordering
                    4. fast solution to multi-rule queries (such as critical path rules). Exploiting _solveQuery():
                        - better index determination,
                        - boolean query success breaking and
                        - avoiding re-running previously failed boolean queries
                 - note: fully generic rules fail (such as generic 3 variable synonym and antonym rules)
    test20r-16   - as test20r-15 but supports fully generic rules (such as generic 3 variable synonym and antonym rules)
    test20r-17   - as test20r-16 but supports chained fully generic rules (ie. syn of syn of ant of syn...)
    test20r-18   - as test20r-17 but supports queries with nested triples requiring rules to solve
    test20r-19   - as test20r-18 but using refactored Queryables
    test20r-20   - as test20r-19 but with extended handling of:
                    1. nested QueryExpression Queries - testing latest userexit02.py
                    2. QueryExpressions QueryValueExpression lists not confused with nested Query lists
    test20r-21   - as test20r-20 but supports non-inferable QueryExpression comperands
    test20r-22   - as test20r-21 but exploits new representation of rules in DDL as dicts, supporting:
                    1. nesting of rules within triples
                    2. round tripping of rendered rules for immediate or subsequent instantiation
    test20r-23   - as test20r-22 but exploits refactored Queryables._solve()
    test20r-24   - as test20r-23 but exploits refactored mtstores for DistSimpleTripleStore (DSTS) support
                    1. tests DSTS comprising 2 STS and DSTS itself with data. (triples and rules shared and overlapping between the 3)
                    2. other Variations:
                       (a) tests SimpleTripleStore (STS) only
                       (b) tests DSTS comprising just 1 STS with data (algorithm detects this and processes as (a) above.
                       (c) tests DSTS comprising 2 STS and DSTS itself with data. (triples and rules shared and overlapping between the 3)
    test20r-25   - as test20r-24 but exploits re-engineered STS._processTriple() and multiple rule variants in query handling
                    1. tests DSTS comprising 2 STS and DSTS itself with data. (rules merged from the 3)
                    2. other Variations:
                       (a) tests SimpleTripleStore (STS) only
                       (b) tests DSTS comprising just 1 STS with data (algorithm detects this and processes as (a) above.
                       (c) tests DSTS comprising 2 STS and DSTS itself with data. (triples and rules shared and overlapping between the 3)
                       (d) as (c) above but tests variety of rules instantiation syntax
                       (e) as (d) above but tests unload/load - ie. earlier tests on unloaded and reloaded DSTS
    test20r-26   - as test20r-25 but exploits re-engineered TS/DTS with optional persistence via ODBMS
                    1. tests DTS comprising 2 TS and DTS itself with data. (rules merged from the 3)
                    2. other Variations:
                       (a) tests TripleStore (TS) only
                       (b) tests DTS comprising just 1 TS with data (algorithm detects this and processes as (a) above.
                       (c) tests DTS comprising 2 TS and DTS itself with data. (triples and rules shared and overlapping between the 3)
                       (d) as (c) above but tests variety of rules instantiation syntax
                       (e) as (d) above but tests unload/load - ie. earlier tests on unloaded and reloaded DTS
                       (f1/f2) as (e) but tests Persistent DTS. (f1) - instantiate and close. (f2) re-open and query
                       (g1/g2) as (e) but tests DTS with 2 Persistent TS. (g1) - instantiate and close. (g2) re-open and query
    test20r-27    - as test20r-26 but exploits URI support
                       (e1) tests mixed URI bases (none,system base,third party base) without namespaces
                       (e2) tests mixed URI bases (none,system base,third party base) with namespaces
    test20r-28    - as test20r-27 but exploits alias_ontology01.dat
                       (e1) tests mixed URI bases (none,system base,third party base) plus aliased reserved keywords in URI generation without namespaces
                       (e2) tests mixed URI bases (none,system base,third party base) plus aliased reserved keywords in URI generation with namespaces
    test20r-29    - as test20r-28 but also outputting new query trace
    test20r-30    - as test20r-29 but exploiting new folder structure and new config variables
                       (e0) as (e2) without DTS
                       (e1) tests mixed URI bases (none,system base,third party base) plus aliased reserved keywords in URI generation without namespaces
                       (e2) tests mixed URI bases (none,system base,third party base) plus aliased reserved keywords in URI generation with namespaces
                       (e3a) persistent store set-up and 2 queries repeated
                       (e3b) persistent store open and 2 queries repeated
                       (e4) tests query outcomes pre-emptive cache.
                            A fact provides a successfull query outcome before its corresponding rule can be invoked to extract the remainder.
                            Tests if the cached fact interferes with the rule.
                       (e5) EQL with 2 not EQs one of which a variable is bound to a triple.
                            Comprises two runs. Each should yield same results - testing (internally bound and unbound support):
                              1. bound to internally unbound triple
                              2. bound to internally bound triple
    test20r-b    - rules via stack, not working - avenue rejected 07/12/09

@author: Administrator
'''
import metabulate.stores.stores         as mtstores
import metabulate.facades.facade        as mtfacade
import metabulate.utils.utils           as mtutils
import metabulate.utils.debug           as mtdebug
import metabulate.renderers.render      as mtrender
import metabulate.rules.rules           as mtrules
import metabulate.singletons.singleton  as mtsingleton

if __name__ == "__main__":
    # get default file paths and types
    mtconfig   = mtsingleton.Settings()._getItem('config')
    debug_path = mtconfig._getItem('debugfile_path','%configfilesbase%Debug\\',mtconfig)
    debug_type = mtconfig._getItem('debugfile_type','txt',mtconfig)
    result_path = mtconfig._getItem('resultsfile_path','%configfilesbase%Results\\',mtconfig)
    result_type = mtconfig._getItem('resultsfile_type','txt',mtconfig)
    unload_path = mtconfig._getItem('stores_unloadfile_path','%configfilesbase%Unloads\\',mtconfig)
    unload_type = mtconfig._getItem('stores_unloadfile_type','pyo',mtconfig)
    # set debug criteria
    dc0 = mtdebug.Criteria(methods=['_solveEquationList','_solveEquation'])
    dc1 = mtdebug.Criteria(classes=['Sequence'],methods=['_generate'],vars=['bound','s'],lines=[[471,485]])
    dc2 = mtdebug.Criteria(classes=['Sequence','RecursiveDepthFirst'],notes=['inputs','returns','yields'])
    dc3 = mtdebug.Criteria(notes=['interpret'])
    dc4 = mtdebug.Criteria(methods=['_expandTriple'],
                           targets=[mtutils.Flatfile(path=debug_path,
                                                     name='DebugOutput_dc4',
                                                     type=debug_type)])
    dc5 = mtdebug.Criteria(classes=['Sequence','Content','Transformation'],methods=['_generate','_interpolate','_interpetVar'])
    dc5f = mtdebug.Criteria(classes=['Sequence','Content','Transformation'],
                            targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc5',
                                                      type=debug_type)])
    dc6 = mtdebug.Criteria(classes=['Facade'])
    dc6f = mtdebug.Criteria(classes=['Facade'],
                            targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc6',
                                                      type=debug_type)])
    dc7 = mtdebug.Criteria(methods=['_setPattern','_prepareVars','_deliver'])
    dc7f = mtdebug.Criteria(methods=['_setPattern','_prepareVars','_deliver','_peel'],
                            targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc3_new',
                                                      type=debug_type)])
    dc8f = mtdebug.Criteria(methods=['_actionTriple','_processTriple'],
                            targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc4',
                                                      type=debug_type)])
    dc9f = mtdebug.Criteria(methods=['_deepUnion'],
                            targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc8',
                                                      type=debug_type)])
    dc10f = mtdebug.Criteria(methods=['_solveTriple','_solveTriple1'],
                            targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc10',
                                                      type=debug_type)])
    dc11f = mtdebug.Criteria(methods=['_solve','_solveTriple','_solveTriple1'],
                            targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc11c',
                                                      type=debug_type)])
    dc12f = mtdebug.Criteria(methods=['_solveQuery','_solveQueryList','_solveEquation','_solveEquationList','_interpolate1','_solve'],
                            targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc8',
                                                      type=debug_type)])
    dc13f = mtdebug.Criteria(methods=['_solveEquation','_solveEquationList','_generate','_interpolate'],
                            targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc13',
                                                      type=debug_type)])
    dc14f = mtdebug.Criteria(methods=['_solveEquation','_solveEquationList','_solveQueryList','_solve'],
                             targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc14_new',
                                                      type=debug_type)])
    dc15f = mtdebug.Criteria(classes=['QueryExpression','QueryElement','QueryValueExpression'],
                             targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc15a',
                                                      type=debug_type)])
    dc16f = mtdebug.Criteria(methods=['_setMatch','_collateMatch','_makeKey','_solveQuery','_solve','_interpolate','_solveEquation','_solveQueryList','_solveEquationList'],
                             targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc16_new3b2',
                                                      type=debug_type)])
    dc17f = mtdebug.Criteria(methods=['_solveEquation'],lines=[[105,119]],
                             targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc17_new',
                                                      type=debug_type)])
    dc18f = mtdebug.Criteria(methods=['_solveQuery'],notes=['OK query'],
                             targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_query_results',
                                                      type=debug_type)])
    dc19f = mtdebug.Criteria(classes=['Solution','RecursiveDepthFirst','Rule','TripleStore','Equation','QueryList','Query','QueryElement','QueryExpression','QueryValueExpression'],
                             targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_test20r-19_dc19f',
                                                      type=debug_type)])
    dc20f_dup = mtdebug.Criteria(methods=['_solveEquationList'],notes=['dup'],
                            targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc20_dup18',
                                                      type='txt')])
    dc20f_ok = mtdebug.Criteria(methods=['_solveEquationList'],notes=['ok'],
                            targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc20_ok18',
                                                      type=debug_type)])
    dc20f = mtdebug.Criteria(methods=['_solveEquationList'],notes=['ok','dup'],
                            targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc20_18',
                                                      type=debug_type)])
    dc21f = mtdebug.Criteria(methods=['_solveTriple1'],notes=['interpret'],
                            targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc21',
                                                      type=debug_type)])
    dc22f = mtdebug.Criteria(methods=['_actionPredicate','_actionTriple','_processTriple','_addTriple'],
                            targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc22',
                                                      type=debug_type)])
    dc28 = mtdebug.Criteria(classes=['Query'],methods=['_solve'],notes=['trace'])
    # set debug
  #  d = mtdebug.Debug()
    # assign it the criteria
#    d._update(criteria=[dc8f,dc12f,dc7f,dc13f,dc10f,dc14f,dc15f])
 #   d._update(criteria=[dc6,dc20f_dup,dc20f_ok])
  #  d._update(criteria=[dc11f])
  #  d._update(criteria=[dc21f])
 #   d._update(criteria=[dc6,dc20f])
    # files
    fu = mtutils.Flatfile(path=unload_path,
                          name='test20r-30_unload_s1',
                          type=unload_type)
    f1 = mtutils.Flatfile(path=result_path,
                          name='genealogy_test1',
                          type=result_type)
    f3 = mtutils.Flatfile(path=result_path,
                          name='test20r-30_triples',
                          type=result_type)
    f4 = mtutils.Flatfile(path=result_path,
                          name='test20r-30_rules',
                          type=result_type)
    f5 = mtutils.Flatfile(path=result_path,
                          name='test20r-30_queries',
                          type=result_type)
    f6 = mtutils.Flatfile(path=result_path,
                          name='test20r-30_results',
                          type=result_type)
    # stores
    s1 = mtstores.DistTripleStore(dbname='test20r-30e3_1')                 # DTS s1
    sr = mtstores.DistTripleStore()                                                     # DTS s1
    sa = mtstores.TripleStore(dbname='test20r-30e3_a')                     #  TS sa persistent
    sb = mtstores.TripleStore(dbname='test20r-30e3_b')                     #  TS sb persistent
    s1 += [sb,sa]                                                                       # add sa and sb to DTS (as queryStores)
    print ('s1=',s1)
    print ('s1._getQueryStores()=',s1._getQueryStores())
    s2 = mtstores.TripleStore()
    s3 = mtstores.TripleStore()
    s4 = mtstores.TripleStore()
    # add namespaces in source stores
 #    Test Load/Unload
 #    s1._unload(file=f1)
 #    s0 = s1._load(file=f1)
 #    print (s0._toString())
 #    print
    print (s1._toString())
    print
  #  print ('unloading DSTS s1 to fu')
  #  s1._unload()
  #  print ('reloading DSTS from fu as sr')
  #  sr = sr._load()
  #  print
  #  print (sr._toString())
  #  print
#    print (s0._toString())
#    d = mtdebug.Debug()
    # assign it the criteria
#    d._update(criteria=[dc19f])
    # set Result requests
#    rlt01 = mtrules.Result(request=[[('  ?person1  ', "desc_of", '?person2')]])                               # pass
#    rlt01 = mtrules.Result(request=[[(('?person1', 'from', 'Truro'), "child_of", '?person2')]])               # pass
#    rlt01 = mtrules.Result(request=[[([('?person1', 'from', 'Truro')], "child_of", '?person2')]])             # pass
#    rlt01 = mtrules.Result(request=[[(['?person1=eve','?person1=eve2'], "child_of", '?person2')]])            # pass
#    rlt01 = mtrules.Result(request=[[(('?person1', 'from', 'Truro'), "desc_of", '?person2')]])                # pass
#    rlt01 = mtrules.Result(request=[[([('?person1', 'from', 'Truro')], "desc_of", '?person2')]])              # pass
#    rlt02 = mtrules.Result(request=[[('?person2','from','Truro')]])                                           # pass
#    rlt02 = mtrules.Result(request=[[('?person2','from',['London','Truro'])]])                                # pass
#    rlt01 = mtrules.Result(request=[[('?person1', "desc_of", ('?person2','from','Truro'))]])                  # pass - nested Query
#    rlt01 = mtrules.Result(request=[[('?person1', "desc_of", "('?person2','from','Truro')")]])                # pass - nested QueryExpression Query
#    rlt01 = mtrules.Result(request=[[('?person1', "desc_of", ('?person2','from',['Truro','London']))]])       # pass - nested Query with QueryElement list
    rlt01 = mtrules.Result(request=[[('?person1', "desc_of", "('?person2','from',['London','Truro'])")]])     # pass - nested QueryExpression Query with QueryElement list
#    rlt01 = mtrules.Result(request=[[('?person1', "desc_of", ('?person2','from','London|Truro'))]])           # pass - nested Query with QueryExpression list
#    rlt01 = mtrules.Result(request=[[('?person1', "desc_of", "('?person2','from','London|Truro')")]])         # pass - nested QueryExpression Query with QueryExpression list
#    rlt01 = mtrules.Result(request=[[(['?person1=eve','?person1=eve2'], "desc_of", '?person2')]])             # pass
#    rlt00 = mtrules.Result(request=[[("?son=mike|dan", 'son_of', '?person')]])                                # pass
    rlt00 = mtrules.Result(request=[[("?son=mike", 'son_of', '?person')]])                                    # pass
#    rlt04 = mtrules.Result(request=[[('?sub=eve','?pred=child_of','?obj=dan')]])                              # pass
#    rlt04 = mtrules.Result(request=[[("?sub='*'","?pred='*'","?obj='*'")]])                                   # pass
#    rlt04 = mtrules.Result(request=[[('?sub="*"','?pred="*"','?obj="*"')]])                                   # pass
#    rlt04 = mtrules.Result(request=[[('?sub="?"','?pred','?obj="?"')]])                                       # FAIL - NO RULES RETURNED (MAYBE OK?)
#    rlt04 = mtrules.Result(request=[[("?sub='?'","?pred","?obj='?'")]])                                       # FAIL - NO RULES RETURNED (MAYBE OK?)
#    rlt04 = mtrules.Result(request=[[('?sub=eve', "?pred=desc_of", '?obj=alice')]])                           # pass
#    rlt04 = mtrules.Result(request=[[('?sub=eve', "?pred=des_of", '?obj=alice')]])                           # pass
 #   rlt04 = mtrules.Result(request=[[('?sub', "?pred=desc_of", '?obj')]])                                     # pass
 #   rlt04 = mtrules.Result(request=[[('?sub', "?pred=ancs_of", '?obj')]])                                     # pass
#    rlt04 = mtrules.Result(request=[[('?sub', "?pred=des_of", '?obj')]])                                      # pass
#    rlt04 = mtrules.Result(request=[[('?sub=?','?pred','?obj')
#                                      ,('?sub','?pred=?','?obj')
#                                      ,('?sub','?pred','?obj=?')]])                                             # pass - all inferences
#    rlt04 = mtrules.Result(request=[[('?sub == ?','?pred','?obj')
#                                      ,('?sub','?pred = =?','?obj')
#                                      ,('?sub','?pred','?obj==?')]])                                            # pass - all rules
    rlt04 = mtrules.Result(request=[[('?sub','?pred','?obj')]])                                               # pass
#    rlt04 = mtrules.Result(request=[[('?sub','?pred','?obj')],[('?sub','child_of','dan')]])                   # FAIL
#    rlt04 = mtrules.Result(request=[[('?sub','?pred','?obj')],['not',('?sub','child_of','dan')]])             # pass
#    rlt04 = mtrules.Result(request=[['not',('?sub','child_of','comtriples#dan')],[('?sub','?pred','?obj')]])             # pass
#    rlt04 = mtrules.Result(request=[[('?sub','?pred','?obj')],['not',('?sub','child_of','dan')]
#                                                               ,['not',('?sub','from','London')]])              # pass
#    rlt04 = mtrules.Result(request=[[('?sub','?pred=ancestor3_of','?obj')]])                                               # pass
    rlt05 = mtrules.Result(request=[[("?s","?r=?r1='child_of'","?o")]])                                       # pass
#    rlt02 = mtrules.Result(request=[[('eve', "desc_of", '?person2')]])                                        # pass
#    rlt02 = mtrules.Result(request=[[(('ender', 'from', 'Truro'), "desc_of", '?person2')]])                   # pass
#    rlt02 = mtrules.Result(request=[[(('ender|eddy', 'from', 'Truro'), "desc_of", '?person2')]])              # pass
#    rlt02 = mtrules.Result(request=[[(('?person1', 'from', 'Truro'), "desc_of", '?person2')]])                # pass
#    rlt02 = mtrules.Result(request=[[('eve', "desc_of", '?person2')]
#                                     ,[('?person2', "desc_of", 'alice')]])                                      # pass
#    rlt02 = mtrules.Result(request=[[('eve', "des_of", '?person2')]
#                                     ,[('?person2', "des_of", 'alice')]])                                       # pass - syn of recursed rule
#    rlt02 = mtrules.Result(request=[[('eve', "descr_of", '?person2')]
#                                     ,[('?person2', "descr_of", 'alice')]])                                     # pass - reversed syn of recursed rule
#    rlt02 = mtrules.Result(request=[[('alice', "ancs_of", '?person2')]
#                                     ,[('?person2', "ancs_of", 'eve')]])                                        # pass - ant of recursed rule
#    rlt02 = mtrules.Result(request=[[('alice', "ancsr_of", '?person2')]
#                                     ,[('?person2', "ancsr_of", 'eve')]])                                       # pass - reversed ant of recursed rule
#    rlt02 = mtrules.Result(request=[[('alice', "anc_of", '?person2')]
#                                     ,[('?person2', "anc_of", 'eve')]])                                         # pass - ant of syn of recursed rule
#    rlt02 = mtrules.Result(request=[[('alice', "ancestor1_of", '?person2')]
#                                     ,[('?person2', "ancestor1_of", 'eve')]])                                   # pass - syn of ant of recursed rule
    rlt02 = mtrules.Result(request=[[('alice', "ancestor2_of", '?person2')]
                                     ,[('?person2', "ancestor2_of", 'eve')]])                                   # pass - syn of ant of syn of recursed rule
#    rlt02 = mtrules.Result(request=[[('alice', "ancestor3_of", '?person2')]
#                                     ,[('?person2', "ancestor3_of", 'eve')]])                                   # pass - syn of syn of ant of syn of recursed rule
    print ('queries defined')
    # rendering submission
    p0t = mtrender.Sequence(pattern=['?!triples'], # via variable notation
                           targets=[s3,f3],
                           render='py')
    p0r = mtrender.Sequence(pattern=['?!rules'], # via variable notation
                           targets=[s4,f4],
                           render='py')
    p0q = mtrender.Sequence(pattern=['?!queries'], # via variable notation
                           targets=[f5],
                           render='py')
    p1 = mtrender.Sequence(pattern=[('?son', 'son_of', '?person')], # triple propogation
                           targets=[s2,'display'],
                           render='csv')
    p2 = mtrender.Sequence(pattern=[('?person1', 'desc_of', '?person2')], # triple propogation
                           targets=[s2,'display'],
                           render='csv')
    p3 = mtrender.Sequence(pattern=['?person2'],
                           targets=['display'],
                           render='csv')
    p4 = mtrender.Sequence(pattern=[('?sub', '?pred', '?obj')],
                           targets=[s2,'display'],
                           render='csv',
                           URImode='nativealias')
    p4a = mtrender.Sequence(pattern=[('?sub', '?pred', '?obj'),('results', 'contain', ('?sub', '?pred', '?obj'))],
                           targets=[s2,'display'],
                           render='csv',
                           URImode='nativealias')
    p6 = mtrender.Transformation(pattern=['!!og!!','/^(.)(.*?)(.)$/$3$2$1/'],id='?p6')
    #p5 = mtrender.Sequence(pattern=[({('np2',p2):{'og':'?o'}},'is known by','?s')])
    p5 = mtrender.Sequence(pattern=[({('np6','!p6'):{'?og':'?o'}},'is known by','?s')],
                           targets=['display'],
                           render='csv')
    print ('Renders defined')
#    d = mtdebug.Debug()
    # assign it the criteria
#    d._update(criteria=[dc16f])
    # set query
    rlt00._update(outputs=[p1])
    face00 = mtfacade.Facade(store=s1,
                             results=[rlt00])
    rlt01._update(outputs=[p2,p0t,p0r,p0q])
    face01 = mtfacade.Facade(store=s1,
                             results=[rlt01])
    rlt02._update(outputs=[p3])
    face02 = mtfacade.Facade(store=s1,
                             results=[rlt02])
#    rlt04._update(outputs=[p4,p0t,p0r,p0q])
    rlt04._update(outputs=[p4])
    face04 = mtfacade.Facade(store=s1,
                             results=[rlt04])
    rlt05._update(outputs=[p5])
    face05 = mtfacade.Facade(store=s1,
                             results=[rlt05])
    print ('results and facades defined')
    # reset dubug criteria
    # execute the query
#    s1._update(infer=False)
    print '## 1st Query iteration'
    face04._generate()
    print
    # check output channelled to a store
    print ('results instantiated')
    print (s2._toString())
    print ('contributory triples instantiated')
    print (s3._toString())
    print ('contributory rules instantiated')
    print (s4._toString())
    print
    print '## 2nd Query iteration'
    face04._generate()
    print
    # check output channelled to a store
    print ('results instantiated')
    print (s2._toString())
    print ('contributory triples instantiated')
    print (s3._toString())
    print ('contributory rules instantiated')
    print (s4._toString())
#    print
#    print ('##------------DTS S1-------------##')
#    print (s1._toString())
#    print
    s1._close()

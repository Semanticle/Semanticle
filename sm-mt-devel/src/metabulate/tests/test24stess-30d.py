'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

Created on 09 Aug 2010
Last Updated on 10 Aug 2010

Stress tests - situations, scalability

Related:
    test24stress-30a - tests indirect relationships from generated data
                        OK for around 500 generated with 2 degrees of freedom
    test24stress-30b - tests indirect relationship query on circular triples
                        OK circular links are detected
                        FAIL only 8 of 9 possible infered triples delivered ('pc', 'desc_of', 'pc') not returned.
    test24stress-30c - tests generic representation of recursive relationships            OK
    test24stress-30d - tests generic representation of fully recursive relationships
                       also tests like matching with(out) recursion
                       also test discontiguous full text matching support
    test24stress-30e - tests generic representation of reciprocol relationships

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
    dc29f = mtdebug.Criteria(methods=['_solve','_solveTriple1'],
                            targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc29',
                                                      type=debug_type)])
    dc29af = mtdebug.Criteria(methods=['_solve','_solveTriple1'],
                            targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc29b',
                                                      type=debug_type)])
    dc29bf = mtdebug.Criteria(methods=['_solve','_solveTriple1','_makeKey'],
                            targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc29b1',
                                                      type=debug_type)])
    dc29cf = mtdebug.Criteria(methods=['_solve','_solveTriple1','_makeKey','_collateMatch'],
                            targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc29c2',
                                                      type=debug_type)])
    dc29df = mtdebug.Criteria(methods=['_solve','_solveTriple1','_makeKey'],
                            targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc29d',
                                                      type=debug_type)])
    dc29ef = mtdebug.Criteria(methods=['_solveTriple1'],notes=['inputs','yields']
                             ,targets=[mtutils.Flatfile(path=debug_path,
                                                        name='DebugOutput_dc29e',
                                                        type=debug_type)])
    dc29ff = mtdebug.Criteria(methods=['_solve'],classes=['Equation']
                             ,targets=[mtutils.Flatfile(path=debug_path,
                                                        name='DebugOutput_dc29f1',
                                                        type=debug_type)])
    dc30e = mtdebug.Criteria(classes=['QueryElement'],notes=['summary']
                             ,targets=[mtutils.Flatfile(path=debug_path,
                                                        name='DebugOutput_dc30e',
                                                        type=debug_type)])
    dc30f = mtdebug.Criteria(methods=['_makeKey'],notes=['summary']
                             ,targets=[mtutils.Flatfile(path=debug_path,
                                                        name='DebugOutput_dc30fnx',
                                                        type=debug_type)])
    # set debug
  #  d = mtdebug.Debug()
    # assign it the criteria
#    d._update(criteria=[dc8f,dc12f,dc7f,dc13f,dc10f,dc14f,dc15f])
 #   d._update(criteria=[dc6,dc20f_dup,dc20f_ok])
  #  d._update(criteria=[dc11f])
  #  d._update(criteria=[dc30f])
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
    s1 = mtstores.DistTripleStore(unloadfile=fu)                                        # DTS s1
    sr = mtstores.DistTripleStore(loadfile=fu)                                          # DTS s1
    sa = mtstores.TripleStore()                                                         #  TS sa
    sb = mtstores.TripleStore()                                                         #  TS sb
    s1 += [sb,sa]                                                                       # add sa and sb to DTS (as queryStores)
    print ('s1=',s1)
    print ('s1._getQueryStores()=',s1._getQueryStores())
    s2 = mtstores.TripleStore()
    s3 = mtstores.TripleStore()
    s4 = mtstores.TripleStore()
    # add namespaces in source stores
    sa._addNamespace('mytriples', 'http://www.semanticle.org/triples/')
    sb._addNamespace('mytriples', 'http://www.semanticle.org/triples/')
    sa._addNamespace('comtriples', 'http://www.semanticle.com/triples/')
    sb._addNamespace('comtriples', 'http://www.semanticle.com/triples/')
    # triples for recursion test
#    sa._actionTriple('add', 'Jill', 'desc_of', 'Kyle')
    sa._actionTriple('add', 'Kyle', 'desc_of', 'Liam')
    sb._actionTriple('add', 'Liam', 'desc_of', 'Milly')
    sa._actionTriple('add', 'Milly', 'desc_of', 'Niel')
    sb._actionTriple('add', 'Niel', 'desc_of', 'Olly Simon')
    sa._actionTriple('add', 'Olly Simon', 'desc_of', 'Polly')
#    sa._actionTriple('add', {('?desc', 'desc_of', '?ancs'):
#                           [[[('?desc', '?any=child_of', '?ancs')]]
#                           ,[[('?desc', '?any=child_of', '?par')],[('?par', 'desc_of', '?ancs')]]
#                           ]})                                                          # add rule clause 2 to DTS._queryStore b (or change to DTS s1)
 #   sa._actionTriple('add', {('?desc', 'desc_of', '?ancs'):
 #                          [[[('?desc=!=?', '?any==desc_of', '?ancs=!=?')]]
 #                          ,[[('?desc', 'desc_of', '?par')],[('?par', 'desc_of', '?ancs')]]
 #                          ]})                                                          # add rule clause 2 to DTS._queryStore b (or change to DTS s1)
#    sa._actionTriple("add ('?desc', 'desc_of', '?ancs') :- [[[('?desc=!=?', '?any==desc_of', '?ancs=!=?')]]]")    # add rule clause 1 to DTS._queryStore b (or change to DTS s1)
#    sa._actionTriple("add","{('?desc', 'desc_of', '?ancs'):[[[('?desc=!=?', '?any==desc_of', '?par=!=?')],[('?par', 'desc_of', '?ancs')]]]}")                   # add rule clause 2 to DTS._queryStore b (or change to DTS s1)
    sb._actionTriple('add', 'desc_of', 'instance_of', 'fully_recursive_relationship')                 # ok
    sa._actionTriple("add",{('?obj', '?inv', '?sub'):
                          [
                              [[('?inv', 'rev_of', '?forw'),('?forw', 'rev_of', '?inv')]
                              ,[('?sub', "?forw", '?obj')]]
                             ,[[('?inv', 'syn_of', '?inv1'),('?inv1', 'syn_of', '?inv')]
                              ,[('?obj', "?inv1", '?sub')]]
                             ,[[('?inv', 'instance_of', 'fully_recursive_relationship')]
                              ,[('?obj=!=?', '?inv==*', '?sub=!=?')]]                               # OK - fully_recursive terminator condition
                             ,[[('?inv', 'instance_of', 'fully_recursive_relationship')]
                              ,[('?obj=!=?', '?inv==*', '?int=!=?')],[('?int', '?inv',' ?sub')]]    # OK - fully recursive recursion condition
                             ,[[('?inv', 'instance_of', 'recursive_relationship')],[('?inv1', 'solves', '?inv')]
                              ,[('?obj', '?inv1', '?sub')]]
                             ,[[('?inv', 'instance_of', 'recursive_relationship')],[('?inv1', 'solves', '?inv')]
                              ,[('?obj', '?inv1', '?int')],[('?int', '?inv',' ?sub')]]
                           ]})                                                        # add rule to DTS._queryStore a (or change to DTS s1)
    sa._actionTriple("add", 'ancs_of', 'rev_of', 'desc_of')                               # ant
#    s1._actionTriple("add", 'desc_of', 'rev_of', 'ancsr_of')                              # rev ant
    sb._actionTriple("add", 'des_of_this', 'syn_of', 'desc_of')                                # syn
#    s1._actionTriple("add", 'desc_of', 'syn_of', 'descr_of')                              # rev syn
    sa._actionTriple("add", 'anc_of', 'rev_of', 'des_of_this')                                 # ant of syn
#    s1._actionTriple("add", 'ancestor1_of', 'syn_of', 'ancs_of')                          # syn of ant
    sb._actionTriple("add", 'ancestor2_of', 'syn_of', 'anc_of')                           # syn of ant of syn
#    s1._actionTriple("add", 'ancestor3_of', 'syn_of', 'ancestor2_of')                     # syn of syn of ant of syn

    # triples for nested rules test
#    s1._actionTriple("add", 'bob', 'is_sex', 'male')
#    s1._actionTriple("add", 'cev', 'is_sex', 'male')
#    s1._actionTriple("add", 'dan', 'is_sex', 'male')
#    s1._actionTriple("add", 'eve', 'is_sex', 'female')
#    s1._actionTriple("add", 'nancy', 'mother_of', 'mike')
#    s1._actionTriple("add", 'niel', 'father_of', 'mike')
#    s1._actionTriple("add", 'mike', 'is_sex', 'male')
#    s1._actionPredicate(action="add",
#                        fact=('?child', 'son_of', '?parent'),
#                        rule=[[[('?child', 'child_of', '?parent')],
#                               [('?child', "'is_sex'", "'male'")]]])
#    s1._actionPredicate(action="add",
#                        fact=('?child', 'child_of', '?parent'),
#                        rule=[[[('?parent', 'father_of', '?child')]],
#                              [[('?parent', "'mother_of'", '?child')]]])
 #    Test Load/Unload
 #    s1._unload(file=f1)
 #    s0 = s1._load(file=f1)
 #    print (s0._toString())
 #    print
    print (s1._toString())
    print
    print ('unloading DSTS s1 to fu')
    s1._unload()
    print ('reloading DSTS from fu as sr')
    sr = sr._load()
    print
    print (sr._toString())
    print
#    print (s0._toString())
#    d = mtdebug.Debug()
    # assign it the criteria
#    d._update(criteria=[dc19f])
    # set Result request
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
#    rlt04 = mtrules.Result(request=[[('?sub', "?pred=desc_of", '?obj')]])                                     # pass
 #   rlt04 = mtrules.Result(request=[[('?sub=!=?', '?pred==desc_of', '?obj=!=?')]])                            # pass
 #   rlt04 = mtrules.Result(request=[[('?sub', "?pred=ancs_of", '?obj')]])                                     # pass
 #   rlt04 = mtrules.Result(request=[[('?sub', "?pred=anc_of", '?obj')]])                                      # pass
 #   rlt04 = mtrules.Result(request=[[('?sub', "?pred=desc_of", '?obj="Olly Simon"')]])                        # pass
 #   rlt04 = mtrules.Result(request=[[('?sub=!=?', '?pred==desc_of', '?obj=!=?')]])                        # pass
 #   rlt04 = mtrules.Result(request=[[('?sub', "?pred~des_this", '?obj~simon')]])                                # pass - recursing on a like match
#    rlt04 = mtrules.Result(request=[[('?sub=?','?pred','?obj')
#                                      ,('?sub','?pred=?','?obj')
#                                      ,('?sub','?pred','?obj=?')]])                                           # pass - all inferences
#    rlt04 = mtrules.Result(request=[[('?sub == ?','?pred','?obj')
#                                      ,('?sub','?pred = =?','?obj')
#                                      ,('?sub','?pred','?obj==?')]])                                          # pass - all rules
    rlt04 = mtrules.Result(request=[[('?sub','?pred','?obj')]])                                               # pass
#    rlt04 = mtrules.Result(request=[[('?sub','?pred','?obj')],[('?sub','child_of','dan')]])                   # FAIL
#    rlt04 = mtrules.Result(request=[[('?sub','?pred','?obj')],['not',('?sub','child_of','dan')]])             # pass
#    rlt04 = mtrules.Result(request=[['not',('?sub','child_of','comtriples#dan')],[('?sub','?pred','?obj')]])  # pass
#    rlt04 = mtrules.Result(request=[[('?sub','?pred','?obj')],['not',('?sub','child_of','dan')]
#                                                               ,['not',('?sub','from','London')]])            # pass
#    rlt04 = mtrules.Result(request=[[('?sub','?pred=ancestor3_of','?obj')]])                                  # pass
    rlt05 = mtrules.Result(request=[[("?s","?r=?r1='child_of'","?o")]])                                       # pass
#    rlt02 = mtrules.Result(request=[[('eve', "desc_of", '?person2')]])                                        # pass
#    rlt02 = mtrules.Result(request=[[(('ender', 'from', 'Truro'), "desc_of", '?person2')]])                   # pass
#    rlt02 = mtrules.Result(request=[[(('ender|eddy', 'from', 'Truro'), "desc_of", '?person2')]])              # pass
#    rlt02 = mtrules.Result(request=[[(('?person1', 'from', 'Truro'), "desc_of", '?person2')]])                # pass
#    rlt02 = mtrules.Result(request=[[('eve', "desc_of", '?person2')]
#                                     ,[('?person2', "desc_of", 'alice')]])                                    # pass
#    rlt02 = mtrules.Result(request=[[('eve', "des_of", '?person2')]
#                                     ,[('?person2', "des_of", 'alice')]])                                     # pass - syn of recursed rule
#    rlt02 = mtrules.Result(request=[[('eve', "descr_of", '?person2')]
#                                     ,[('?person2', "descr_of", 'alice')]])                                   # pass - reversed syn of recursed rule
#    rlt02 = mtrules.Result(request=[[('alice', "ancs_of", '?person2')]
#                                     ,[('?person2', "ancs_of", 'eve')]])                                      # pass - ant of recursed rule
#    rlt02 = mtrules.Result(request=[[('alice', "ancsr_of", '?person2')]
#                                     ,[('?person2', "ancsr_of", 'eve')]])                                     # pass - reversed ant of recursed rule
#    rlt02 = mtrules.Result(request=[[('alice', "anc_of", '?person2')]
#                                     ,[('?person2', "anc_of", 'eve')]])                                       # pass - ant of syn of recursed rule
#    rlt02 = mtrules.Result(request=[[('alice', "ancestor1_of", '?person2')]
#                                     ,[('?person2', "ancestor1_of", 'eve')]])                                 # pass - syn of ant of recursed rule
    rlt02 = mtrules.Result(request=[[('alice', "ancestor2_of", '?person2')]
                                     ,[('?person2', "ancestor2_of", 'eve')]])                                 # pass - syn of ant of syn of recursed rule
#    rlt02 = mtrules.Result(request=[[('alice', "ancestor3_of", '?person2')]
#                                     ,[('?person2', "ancestor3_of", 'eve')]])                                 # pass - syn of syn of ant of syn of recursed rule
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
    face00 = mtfacade.Facade(store=sr,
                             results=[rlt00])
    rlt01._update(outputs=[p2,p0t,p0r,p0q])
    face01 = mtfacade.Facade(store=sr,
                             results=[rlt01])
    rlt02._update(outputs=[p3])
    face02 = mtfacade.Facade(store=sr,
                             results=[rlt02])
#    rlt04._update(outputs=[p4,p0t,p0r,p0q])
    rlt04._update(outputs=[p4])
    face04 = mtfacade.Facade(store=sr,
                             results=[rlt04])
    rlt05._update(outputs=[p5])
    face05 = mtfacade.Facade(store=sr,
                             results=[rlt05])
    print ('results and facades defined')
    # reset dubug criteria
    # execute the query
#    s1._update(infer=False)
    face04._generate()
    print
    # check output channelled to a store
    print ('results instantiated')
    print (s2._toString())
    print ('should be 82 results')
    print
    print ('contributory triples instantiated')
    print (s3._toString())
    print ('contributory rules instantiated')
    print (s4._toString())
#    print ('source Store again')
#    print (sr._toString())

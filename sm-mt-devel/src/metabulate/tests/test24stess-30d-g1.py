'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

Created on 09 Aug 2010
Last Updated on 10 Aug 2010

Stress tests - situations, scalability

Related:
    test24stress-30a   - tests indirect relationships from generated data
                         OK for around 500 generated with 2 degrees of freedom
    test24stress-30b   - tests indirect relationship query on circular triples
                         OK circular links are detected
                         FAIL only 8 of 9 possible infered triples delivered ('pc', 'desc_of', 'pc') not returned.
    test24stress-30c   - tests generic representation of recursive relationships            OK
    test24stress-30d   - tests generic representation of fully recursive relationships
                         also tests like matching with(out) recursion
                         also test discontiguous full text matching support
    test24stress-30d_g - as test24stress-30d but tests persistence (with full text index) run in 2 steps:
                         - 30d_g1 resets the database and instantiates
                         - 30d_g2 loads from database and runs queries
    test24stress-30e   - tests generic representation of reciprocol relationships

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
                                                      name='DebugOutput_dc29c',
                                                      type=debug_type)])
    dc29df = mtdebug.Criteria(methods=['_solve','_solveTriple1','_makeKey'],
                            targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc29d',
                                                      type=debug_type)])
    # set debug
  #  d = mtdebug.Debug()
    # assign it the criteria
#    d._update(criteria=[dc8f,dc12f,dc7f,dc13f,dc10f,dc14f,dc15f])
 #   d._update(criteria=[dc6,dc20f_dup,dc20f_ok])
  #  d._update(criteria=[dc11f])
  #  d._update(criteria=[dc29f])
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
    sa = mtstores.TripleStore(dbname='test24stress-30d_g-sa',dbreset=True)              #  TS sa
    sb = mtstores.TripleStore(dbname='test24stress-30d_g-sb',dbreset=True)              #  TS sb
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
    sa._actionTriple('add', 'Kyle', 'desc_of', 'mytriples#Liam')
    sb._actionTriple('add', 'mytriples#Liam', 'desc_of', 'Milly')
    sa._actionTriple('add', 'Milly', 'desc_of', 'comtriples#Niel')
    sb._actionTriple('add', 'comtriples#Niel', 'desc_of', 'Olly Simon')
    sa._actionTriple('add', 'Olly Simon', 'desc_of', 'Polly')
#    sa._actionTriple('add', {('?desc', 'desc_of', '?ancs'):
#                           [[[('?desc=!=?', '?any==desc_of', '?ancs=!=?')]]
#                           ,[[('?desc=!=?', '?any==desc_of', '?par=!=?')],[('?par', 'desc_of', '?ancs')]]
#                           ]})                                                          # add rule clause 2 to DTS._queryStore b (or change to DTS s1)
 #   sa._actionTriple("add ('?desc', 'desc_of', '?ancs') :- [[[('?desc=!=?', '?any==desc_of', '?ancs=!=?')]]]")    # add rule clause 1 to DTS._queryStore b (or change to DTS s1)
 #   sa._actionTriple("add","{('?desc', 'desc_of', '?ancs'):[[[('?desc=!=?', '?any==desc_of', '?par=!=?')],[('?par', 'desc_of', '?ancs')]]]}")                   # add rule clause 2 to DTS._queryStore b (or change to DTS s1)
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
    print (s1._toString())
#    print
#    print ('unloading DSTS s1 to fu')
#    s1._unload()
#    print ('reloading DSTS from fu as sr')
#    sr = sr._load()
#    print
#    print (sr._toString())
    print
    s1._close()
    print ('TripleStores sa and sb instantiated closed')

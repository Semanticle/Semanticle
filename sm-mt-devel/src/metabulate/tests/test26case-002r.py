'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

Created on 28 Jan 2009
Last Updated on 10 July 2010

As test20 with tests of:
    rules instantiation and query inference

Related:
    single dict TS recursion rule plus generic rule + minimal data:
        test20simple-001d   - unmerged recursive rule EQ order correct   QL order correct
        test20simple-002d   - unmerged recursive rule EQ order correct   QL order incorrect
        test20simple-003d   - merged   recursive rule EQ order correct   QL order correct   variables consistent
        test20simple-004d   - merged   recursive rule EQ order correct   QL order correct   variables inconsistent (03)
        test20simple-005d   - merged   recursive rule EQ order correct   QL order incorrect variables consistent
        test20simple-006d   - merged   recursive rule EQ order correct   QL order incorrect variables inconsistent (04)
        test20simple-007d   - unmerged recursive rule EQ order incorrect QL order correct                          (05)
        test20simple-008d   - unmerged recursive rule EQ order incorrect QL order incorrect                        (06)
        test20simple-009d   - merged   recursive rule EQ order incorrect QL order correct   variables consistent
        test20simple-010d   - merged   recursive rule EQ order incorrect QL order correct   variables inconsistent (07)
        test20simple-011d   - merged   recursive rule EQ order incorrect QL order incorrect variables consistent
        test20simple-012d   - merged   recursive rule EQ order incorrect QL order incorrect variables inconsistent (08)
    single rbtree TS recursion rule plus generic rule + minimal data:
        test20simple-001r   - unmerged recursive rule EQ order correct   QL order correct
        test20simple-002r   - unmerged recursive rule EQ order correct   QL order incorrect
        test20simple-003r   - merged   recursive rule EQ order correct   QL order correct   variables consistent
        test20simple-004r   - merged   recursive rule EQ order correct   QL order correct   variables inconsistent (03)
        test20simple-005r   - merged   recursive rule EQ order correct   QL order incorrect variables consistent
        test20simple-006r   - merged   recursive rule EQ order correct   QL order incorrect variables inconsistent (04)
        test20simple-007r   - unmerged recursive rule EQ order incorrect QL order correct                          (05)
        test20simple-008r   - unmerged recursive rule EQ order incorrect QL order incorrect                        (06)
        test20simple-009r   - merged   recursive rule EQ order incorrect QL order correct   variables consistent
        test20simple-010r   - merged   recursive rule EQ order incorrect QL order correct   variables inconsistent (07)
        test20simple-011r   - merged   recursive rule EQ order incorrect QL order incorrect variables consistent
        test20simple-012r   - merged   recursive rule EQ order incorrect QL order incorrect variables inconsistent (08)

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
    sa = mtstores.TripleStore(structure='rbtree')                                       #  TS sa rbtree
    sr = mtstores.TripleStore()                                                         #  TS sr
    s2 = mtstores.TripleStore()
    s3 = mtstores.TripleStore()
    s4 = mtstores.TripleStore()
    # add namespaces in source stores
    sa._addNamespace('mytriples', 'http://www.semanticle.org/triples/')
    sa._addNamespace('comtriples', 'http://www.semanticle.com/triples/')
    # triples for recursion test
    sa._actionTriple("add [('mytriples#bob', 'child_of', 'alice'),('http://www.semanticle.com/triples/#dan', 'child_of', 'cev')]")
    sa._actionTriple("add", [('cev', 'child_of', 'http://www.semanticle.org/triples/#bob'),"('http://www.semanticle.com/triples/#dan', 'child_of', 'cev')"])
    sa._actionTriple("add", 'eve', 'child_of', 'comtriples#dan')
    sa._actionTriple("add",{('?desc', 'desc_of', '?ancs'):
                          [
                           [[('?desc', 'child_of', '?ancs')]]
#                          ,[[('?child', 'child_of', '?ancs')],[('?desc', 'desc_of', '?child')]]
                          ,[[('?desc', 'desc_of', '?child')],[('?child', 'child_of', '?ancs')]]
                           ]})
 #   sa._actionTriple("add ('?desc', 'desc_of', '?ancs') :- [[[('?desc', 'child_of', '?ancs')]]]")    # add rule clause 1 to DTS._queryStore b (or change to DTS s1)
    sa._actionTriple("add",{('?obj', '?inv', '?sub'):
                          [
                              [[('?inv', 'rev_of', '?forw'),('?forw', 'rev_of', '?inv')]
                              ,[('?sub', "?forw", '?obj')]]
                             ,[[('?inv', 'syn_of', '?inv1'),('?inv1', 'syn_of', '?inv')]
                              ,[('?obj', "?inv1", '?sub')]]
                           ]})                                                        # add rule to DTS._queryStore a (or change to DTS s1)
 #   sa._actionTriple("add","{('?desc1', 'desc_of', '?ancs'):[[[('?child', 'child_of', '?ancs')],[('?desc1', 'desc_of', '?child')]]]}")                   # add rule clause 2 to DTS._queryStore b (or change to DTS s1)
 #   sa._actionTriple("add","{('?desc1', 'desc_of', '?ancs'):[[[('?desc1', 'desc_of', '?child')],[('?child', 'child_of', '?ancs')]]]}")                   # add rule clause 2 to DTS._queryStore b (or change to DTS s1)
    sa._actionTriple("add", 'ancs_of', 'rev_of', 'desc_of')                               # ant
#    s1._actionTriple("add", 'desc_of', 'rev_of', 'ancsr_of')                              # rev ant
    sa._actionTriple("add", 'des_of', 'syn_of', 'desc_of')                                # syn
#    s1._actionTriple("add", 'desc_of', 'syn_of', 'descr_of')                              # rev syn
    sa._actionTriple("add", 'anc_of', 'rev_of', 'des_of')                                 # ant of syn
#    s1._actionTriple("add", 'ancestor1_of', 'syn_of', 'ancs_of')                          # syn of ant
    sa._actionTriple("add", 'ancestor2_of', 'syn_of', 'anc_of')                           # syn of ant of syn
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
    print (sa._toString())
  #  print
  #  print ('unloading DSTS s1 to fu')
  #  sa._unload()
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
    rlt02._update(outputs=[p3])
    face02 = mtfacade.Facade(store=sa,
                             results=[rlt02])
#    rlt04._update(outputs=[p4,p0t,p0r,p0q])
    rlt04._update(outputs=[p4])
    face04 = mtfacade.Facade(store=sa,
                             results=[rlt04])
    rlt05._update(outputs=[p5])
    face05 = mtfacade.Facade(store=sa,
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
    print ('should be 60 results')
    print
    print ('contributory triples instantiated')
    print (s3._toString())
    print ('contributory rules instantiated')
    print (s4._toString())
#    print ('source Store again')
#    print (sr._toString())

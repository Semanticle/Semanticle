'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

Created on 28 Jan 2009
Last Updated on 10 July 2010

As test20 with tests of:
    rules instantiation and query inference

Related:
    single dict TS recursion rule plus generic rule + minimal data:
        test20simple-001d    - unmerged recursive rule EQ order correct   QL order correct
        test20simple-001d_g  - unmerged recursive rule EQ order correct   QL order correct                          >  match
        test20simple-001d_ge - unmerged recursive rule EQ order correct   QL order correct                          >= match
        test20simple-001d_l  - unmerged recursive rule EQ order correct   QL order correct                          <  match
        test20simple-001d_le - unmerged recursive rule EQ order correct   QL order correct                          <= match
        test20simple-002d    - unmerged recursive rule EQ order correct   QL order incorrect
        test20simple-003d    - merged   recursive rule EQ order correct   QL order correct   variables consistent
        test20simple-004d    - merged   recursive rule EQ order correct   QL order correct   variables inconsistent
        test20simple-005d    - merged   recursive rule EQ order correct   QL order incorrect variables consistent
        test20simple-006d    - merged   recursive rule EQ order correct   QL order incorrect variables inconsistent
        test20simple-007d    - unmerged recursive rule EQ order incorrect QL order correct
        test20simple-008d    - unmerged recursive rule EQ order incorrect QL order incorrect
        test20simple-009d    - merged   recursive rule EQ order incorrect QL order correct   variables consistent
        test20simple-010d    - merged   recursive rule EQ order incorrect QL order correct   variables inconsistent
        test20simple-011d    - merged   recursive rule EQ order incorrect QL order incorrect variables consistent
        test20simple-012d    - merged   recursive rule EQ order incorrect QL order incorrect variables inconsistent
        test20simple-012d_g  - merged   recursive rule EQ order incorrect QL order incorrect variables inconsistent >  match
        test20simple-012d_ge - merged   recursive rule EQ order incorrect QL order incorrect variables inconsistent >= match
        test20simple-012d_l  - merged   recursive rule EQ order incorrect QL order incorrect variables inconsistent <  match
        test20simple-012d_le - merged   recursive rule EQ order incorrect QL order incorrect variables inconsistent <= match
    single rbtree TS recursion rule plus generic rule + minimal data:
        test20simple-001r    - unmerged recursive rule EQ order correct   QL order correct
        test20simple-001r_g  - unmerged recursive rule EQ order correct   QL order correct                          >  match
        test20simple-001r_ge - unmerged recursive rule EQ order correct   QL order correct                          >= match
        test20simple-001r_l  - unmerged recursive rule EQ order correct   QL order correct                          <  match
        test20simple-001r_le - unmerged recursive rule EQ order correct   QL order correct                          <= match
        test20simple-002r    - unmerged recursive rule EQ order correct   QL order incorrect
        test20simple-003r    - merged   recursive rule EQ order correct   QL order correct   variables consistent
        test20simple-004r    - merged   recursive rule EQ order correct   QL order correct   variables inconsistent
        test20simple-005r    - merged   recursive rule EQ order correct   QL order incorrect variables consistent
        test20simple-006r    - merged   recursive rule EQ order correct   QL order incorrect variables inconsistent
        test20simple-007r    - unmerged recursive rule EQ order incorrect QL order correct
        test20simple-008r    - unmerged recursive rule EQ order incorrect QL order incorrect
        test20simple-009r    - merged   recursive rule EQ order incorrect QL order correct   variables consistent
        test20simple-010r    - merged   recursive rule EQ order incorrect QL order correct   variables inconsistent
        test20simple-011r    - merged   recursive rule EQ order incorrect QL order incorrect variables consistent
        test20simple-012r    - merged   recursive rule EQ order incorrect QL order incorrect variables inconsistent
        test20simple-012r_g  - merged   recursive rule EQ order incorrect QL order incorrect variables inconsistent >  match
        test20simple-012r_ge - merged   recursive rule EQ order incorrect QL order incorrect variables inconsistent >= match
        test20simple-012r_l  - merged   recursive rule EQ order incorrect QL order incorrect variables inconsistent <  match
        test20simple-012r_le - merged   recursive rule EQ order incorrect QL order incorrect variables inconsistent <= match
    inverted synonyms and or antonyms tests single stores
        test26case-020d_ge   - standard order syn/antonyms dict   structure >= match
        test26case-020d      - standard order syn/antonyms dict   structure
        test26case-020r_ge   - standard order syn/antonyms rbtree structure >= match
        test26case-020r      - standard order syn/antonyms rbtree structure
        test26case-021d_ge   - reversed order syn/antonyms dict   structure >= match
        test26case-021d      - reversed order syn/antonyms dict   structure
        test26case-021r_ge   - reversed order syn/antonyms rbtree structure >= match
        test26case-021r      - reversed order syn/antonyms rbtree structure
    inverted synonyms and or antonyms tests distribued stores (same queries/results as above set)
        test26case-022d_ge   - standard order syn/antonyms dict   structure >= match
        test26case-022r_ge   - standard order syn/antonyms rbtree structure >= match
        test26case-023d_ge   - reversed order syn/antonyms dict   structure >= match
        test26case-023d      - reversed order syn/antonyms dict   structure
        test26case-023r_ge   - reversed order syn/antonyms rbtree structure >= match
        test26case-023r      - reversed order syn/antonyms rbtree structure
    re-ordered triples, inverted synonyms and or antonyms tests single stores
        test26case-030d_ge   - standard order syn/antonyms dict   structure >= match
        test26case-030d      - standard order syn/antonyms dict   structure
        test26case-030r_ge   - standard order syn/antonyms rbtree structure >= match
        test26case-030r      - standard order syn/antonyms rbtree structure
        test26case-031d      - reversed order syn/antonyms dict   structure
        test26case-031r      - reversed order syn/antonyms rbtree structure
    re-ordered triples, inverted synonyms and or antonyms tests distrubuted stores
        test26case-032d_ge   - standard order syn/antonyms dict   structure >= match
        test26case-032r_ge   - standard order syn/antonyms rbtree structure >= match
        test26case-033d_ge   - reversed order syn/antonyms dict   structure >= match
        test26case-033d      - reversed order syn/antonyms dict   structure
        test26case-033r_ge   - reversed order syn/antonyms rbtree structure >= match
        test26case-033r      - reversed order syn/antonyms rbtree structure
    DTS mixed triple ordering, inverted synonyms and or antonyms tests distrubuted stores
        reversed order syn/antonyms dict   structure >= match
            test26case-043d_ge-1  - mixed order facts
            test26case-043d_ge-2  - mixed order facts, rules
            test26case-043d_ge-3  - mixed order facts, rule fragments (with mixed variables)
        reversed order syn/antonyms dict   structure
            test26case-043d-1     - mixed order facts
            test26case-043d-2     - mixed order facts, rules
            test26case-043d-3     - mixed order facts, rule fragments (with mixed variables)
        reversed order syn/antonyms rbtree structure >= match
            test26case-043r_ge-1  - mixed order facts
            test26case-043r_ge-2  - mixed order facts, rules
            test26case-043r_ge-3  - mixed order facts, rule fragments (with mixed variables)
        reversed order syn/antonyms rbtree structure
            test26case-043r-1     - mixed order facts
            test26case-043r-2     - mixed order facts, rules
            test26case-043r-3     - mixed order facts, rule fragments (with mixed variables)
    DTS mixed triple ordering, import and export tests
        inverted synonyms and or antonyms tests distrubuted stores
        mixed order facts, rule fragments (with mixed variables)
        reversed order syn/antonyms dict   structure >= match
            test26case-043d_ge-3_ie01 - various export orders, re-import
            test26case-043d_ge-3_ie02 - various export orders, re-import, store IO ordering,      triple store, facade IO ordering requery
            test26case-043d_ge-3_ie03 - various export orders, re-import, store IO ordering, dist triple store, facade IO ordering requery


@author: Administrator
'''
import copy
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
    export_path = mtconfig._getItem('stores_exportfile_path','%configfilesbase%Results\\',mtconfig)
    export_type = mtconfig._getItem('stores_exportfile_type','txt',mtconfig)
    # set debug criteria
    dc22f = mtdebug.Criteria(methods=['_actionPredicate','_actionTriple','_processTriple','_addTriple'],
                            targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc22',
                                                      type=debug_type)])
    dc26_021d_ge = mtdebug.Criteria(methods=['_solve'],notes=['summary']
                                ,targets=[mtutils.Flatfile(path=debug_path
                                                          ,name='DebugOutput_dc26-021d_ge'
                                                          ,type=debug_type)])
    dc28 = mtdebug.Criteria(classes=['Query'],methods=['_solve'],notes=['trace'])
    # set debug
   # d = mtdebug.Debug()
    # assign it the criteria
#    d._update(criteria=[dc8f,dc12f,dc7f,dc13f,dc10f,dc14f,dc15f])
 #   d._update(criteria=[dc6,dc20f_dup,dc20f_ok])
  #  d._update(criteria=[dc11f])
   # d._update(criteria=[dc26_021d_ge])
 #   d._update(criteria=[dc6,dc20f])
    # files
    fu = mtutils.Flatfile(path=unload_path,
                          name='test20r-30_unload_s1',
                          type=unload_type)
    xp = mtutils.Flatfile(path=export_path,
                          name='test26case_ie01-parent',
                          type=export_type)
    xs = mtutils.Flatfile(path=export_path,
                          name='test26case_ie01-sources',
                          type=export_type)
    xi = mtutils.Flatfile(path=export_path,
                          name='test26case_ie01-identified',
                          type=export_type)
    xl = mtutils.Flatfile(path=export_path,
                          name='test26case_ie01-bespokelist',
                          type=export_type)
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
    s1 = mtstores.DistTripleStore(structure='dict',tripleOrder=['s','o','p'],ioTripleOrder=['p','s','o'])              #  TS sa dict
#    sr = mtstores.DistTripleStore(structure='dict',tripleOrder=['s','o','p'],ioTripleOrder=['p','s','o'])             #  TS sr dict
    sa = mtstores.TripleStore(tripleOrder=['s','o','p'],ioTripleOrder=['p','s','o'])
    sb = mtstores.TripleStore(tripleOrder=['s','p','o'],ioTripleOrder=['p','s','o'])
 #   sb = mtstores.TripleStore(tripleOrder=['s','o','p'],ioTripleOrder=['p','s','o'])
    s1 += [sb,sa]                                                                       # add sa and sb to DTS (as queryStores)
    print ('s1=',s1)
    print ('s1._getQueryStores()=',s1._getQueryStores())
    s2 = mtstores.TripleStore()
    s3 = mtstores.TripleStore()
    s4 = mtstores.TripleStore()
    # add namespaces in source stores
    sa._addNamespace('mytriples', 'http://www.semanticle.org/triples/')
    sa._addNamespace('comtriples', 'http://www.semanticle.com/triples/')
    # triples for recursion test
    sa._actionTriple("add [('child_of', 'mytriples#bob', 'alice'),('child_of', 'http://www.semanticle.com/triples/#dan', 'cev')]")
    sa._actionTriple("delete [('child_of', 'mytriples#bob', 'alice'),('child_of', 'http://www.semanticle.com/triples/#dan', 'cev')]")
    sa._actionTriple("add [('child_of', 'mytriples#bob', 'alice'),('child_of', 'http://www.semanticle.com/triples/#dan', 'cev')]")
    sa._actionTriple("add", [('child_of', 'cev', 'http://www.semanticle.org/triples/#bob')])
    sa._actionTriple("add", 'child_of', 'eve', 'comtriples#dan')
   # sa._actionTriple("add",{('desc_of', '?desc', '?ancs'):
   #                       [
   #                        [[('child_of', '?desc', '?ancs')]]
   #                       ,[[('child_of', '?child', '?ancs')],[('desc_of', '?desc', '?child')]]
#  #                        ,[[('desc_of', '?desc', '?child')],[('child_of', '?child', '?ancs')]]
   #                        ]})
    #sb._actionTriple("add",{('desc_of', '?desc', '?ancs'):
    #                      [
    #                       [[('child_of', '?desc', '?ancs')]]
    #                      ,[[('child_of', '?child', '?ancs')],[('desc_of', '?desc', '?child')]]
#   #                       ,[[('desc_of', '?desc', '?child')],[('child_of', '?child', '?ancs')]]
    #                       ]})
    sa._actionTriple("add ('desc_of', '?desc', '?ancs') :- [[[('child_of', '?desc', '?ancs')]]]")    # add rule clause 1 to DTS._queryStore b (or change to DTS s1)
    sb._actionTriple("add","{('desc_of', '?desc1', '?ancs'):[[[('child_of', '?child', '?ancs')],[('desc_of', '?desc1', '?child')]]]}") # add rule clause 2 to DTS._queryStore b (or change to DTS s1)
 #   sa._actionTriple("add","{('desc_of', '?desc1', '?ancs'):[[[('desc_of', '?desc1', '?child')],[('child_of', '?child', '?ancs')]]]}") # add rule clause 2 to DTS._queryStore b (or change to DTS s1)
    sa._actionTriple("add",{('?inv', '?obj', '?sub'):
                          [
                              [[('rev_of', '?inv', '?forw'),('rev_of', '?forw', '?inv')]
                              ,[("?forw", '?sub', '?obj')]]
                             ,[[('syn_of', '?inv', '?inv1'),('syn_of', '?inv1', '?inv')]
#                             ,[[('syn_of', '?inv1', '?inv'),('syn_of', '?inv', '?inv1')]
                              ,[("?inv1", '?obj', '?sub')]]
                           ]})                                                        # add rule to DTS._queryStore a (or change to DTS s1)
    sa._actionTriple("add", 'rev_of', 'ancs_of', 'desc_of')                               # ant
#    s1._actionTriple("add", 'rev_of', 'desc_of', 'ancsr_of')                              # rev ant
    sa._actionTriple("add", 'syn_of', 'des_of', 'desc_of')                                # syn
#    s1._actionTriple("add", 'syn_of', 'desc_of', 'descr_of')                              # rev syn
 #   sa._actionTriple("add", 'rev_of', 'anc_of', 'des_of')                                 # ant of syn
    sb._actionTriple("add", 'rev_of', 'des_of', 'anc_of')                                 # ant of syn
#    s1._actionTriple("add", 'syn_of', 'ancestor1_of', 'ancs_of')                          # syn of ant
#    sa._actionTriple("add", 'syn_of', 'anc_of', 'ancestor2_of')                           # syn of ant of syn
    sa._actionTriple("add", 'syn_of', 'ancestor2_of', 'anc_of')                           # syn of ant of syn
#    s1._actionTriple("add", 'syn_of', 'ancestor3_of', 'ancestor2_of')                     # syn of syn of ant of syn

 #    Test Load/Unload
 #    s1._unload(file=f1)
 #    s0 = s1._load(file=f1)
 #    print (s0._toString())
 #    print
    print (s1._toString())
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
    rlt04 = mtrules.Result(request=[[('?pred','?sub','?obj>=cev')]])                                               # pass
#    rlt04 = mtrules.Result(request=[[('?sub','?pred','?obj')],[('?sub','child_of','dan')]])                   # FAIL
#    rlt04 = mtrules.Result(request=[[('?sub','?pred','?obj')],['not',('?sub','child_of','dan')]])             # pass
#    rlt04 = mtrules.Result(request=[['not',('?sub','child_of','comtriples#dan')],[('?sub','?pred','?obj')]])             # pass
#    rlt04 = mtrules.Result(request=[[('?sub','?pred','?obj')],['not',('?sub','child_of','dan')]
#                                                               ,['not',('?sub','from','London')]])              # pass
#    rlt04 = mtrules.Result(request=[[('?sub','?pred=ancestor3_of','?obj')]])                                               # pass
    rlt05 = mtrules.Result(request=[[("?r=?r1='child_of'","?s","?o")]])                                       # pass
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
    rlt02 = mtrules.Result(request=[[("ancestor2_of", 'alice', '?person2')]
                                     ,[("ancestor2_of", '?person2', 'eve')]])                                   # pass - syn of ant of syn of recursed rule
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
    face02 = mtfacade.Facade(store=s1
                            ,results=[rlt02])
#    rlt04._update(outputs=[p4,p0t,p0r,p0q])
    rlt04._update(outputs=[p4])
    face04 = mtfacade.Facade(store=s1
                            ,results=[rlt04]
                            ,order=['p','s','o'])
    rlt05._update(outputs=[p5])
    face05 = mtfacade.Facade(store=s1,
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
    print ('should be 40 results')
    print
    print ('contributory triples instantiated')
    print (s3._toString())
    print ('contributory rules instantiated')
    print (s4._toString())
    print
    print ('Exporting store s1 in')
    s1._export(file=xp)
    print ('1. parent store triple order - done.')
    s1._export(file=xs,order='source')
    print ('2. source stores triple orders - done.')
    s1._export(file=xi,order=sb)
    print ('3. identified store triple order - done.')
    s1._export(file=xl,order=['p','o','s'])
    print ('4. bespoke listed triple order - done.')
    print
    print ('Importing from above export files:')
    sxp = mtstores.TripleStore(structure='dict',tripleOrder=['p','o','s'])                                         #  TS sa dict
    sxp._import(file=xp,mode='merge')
    print ('1. from parent store order file -> pos')
    print(sxp._toString())
    print
    sxs = mtstores.TripleStore(structure='dict',tripleOrder=['p','o','s'])                                         #  TS sa dict
    sxs._import(file=xs,mode='merge')
    print ('2. from sources store orders file -> pos')
    print(sxs._toString())
    print
    sxi = mtstores.TripleStore(structure='dict',tripleOrder=['p','o','s'])                                         #  TS sa dict
    sxi._import(file=xi,mode='merge')
    print ('3. from identified store order file -> pos')
    print(sxi._toString())
    print
    sxl = mtstores.TripleStore(structure='dict',tripleOrder=['p','o','s'])                                         #  TS sa dict
    sxl._import(file=xl,mode='merge')
    print ('3. from identified store order file -> pos')
    print(sxi._toString())
    print
#    print ('Query each imported store: Query(pso) -> Stores(pos) -> Result(spo)')
    face04._update(store=sxp)
    s2._reset()
    face04._generate()
    print
    print (s2._toString())
    print 'Should be 40 results'
    print 'End query Store imported from "Parent" ordered export file'
    print
#    face04._update(store=sxs)
#    s2._reset()
#    face04._generate()
#    print
#    print (s2._toString())
#    print 'Should be 40 results'
#    print 'End query Store imported from "Sources" ordered export file'
#    print
#    face04._update(store=sxi)
#    s2._reset()
#    face04._generate()
#    print
#    print (s2._toString())
#    print 'Should be 40 results'
#    print 'End query Store imported from "Identified Store" ordered export file'
#    print
#    face04._update(store=sxl)
#    s2._reset()
#    face04._generate()
#    print
#    print (s2._toString())
#    print 'Should be 40 results'
#    print 'End query Store imported from "List" ordered export file'
#    print
    print ('End Test')

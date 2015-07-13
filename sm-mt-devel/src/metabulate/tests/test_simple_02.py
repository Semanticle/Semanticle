'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

Created on 01 Aug 2010
Last Updated on 01 Aug 2010

Simple instantiation and Query tests
Uses new all in query support:
    query = mtrules.Result(equations={lhs:rhs})             # specify a query
    face  = mtfacade.Facade(store=store,results=[query])    # submit one or more queries to a store
    face._generate()                                        # generate the results

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
    simple_02 = mtdebug.Criteria(methods=['_makeKey','_solve','_getTIDB'],notes=['summary'],
                            targets=[mtutils.Flatfile(path=debug_path,
                                                      name='simple_02_new',
                                                      type=debug_type)])
 #   d = mtdebug.Debug()
 #   d._update(criteria=[simple_02])
    # stores
    s1 = mtstores.TripleStore()                                        # DTS s1
    # triples for recursion test
    s1._actionTriple("add", (['eddy','ender'], 'from', 'Truro'), 'child_of', 'http://www.semanticle.com/triples/#dan')       # add fact to DTS._queryStore b
    s1._actionTriple("add", (['eddyl','enderl'], 'from', 'London'), 'child_of', 'http://www.semanticle.com/triples/#dan')    # add fact to DTS._queryStore a
    s1._actionTriple("add", 'http://www.semanticle.org/triples/#bob', 'child_of', (['andrew','andy'], 'from', 'London'))
    s1._actionTriple("add", 'http://www.semanticle.org/triples/#bob', 'child_of', (['alex','arny'], 'from', 'Truro'))
    s1._actionTriple("add [('http://www.semanticle.org/triples/#bob', 'child_of', 'alice'),('http://www.semanticle.com/triples/#dan', 'child_of', 'cev')]")
    s1._actionTriple("add", [('cev', 'child_of', 'http://www.semanticle.org/triples/#bob'),"('http://www.semanticle.com/triples/#dan', 'child_of', 'cev')"])
    s1._actionTriple("add", 'eve', 'child_of', 'http://www.semanticle.com/triples/#dan')
    s1._actionTriple("add", 'eve1', 'child_of', 'http://www.semanticle.com/triples/#dan')
    s1._actionTriple("add", 'eve2', 'child_of', 'http://www.semanticle.com/triples/#dan')                                    # add fact to DTS (default _updateStore)
    s1._actionTriple("delete", 'cev', 'child_of', 'http://www.semanticle.org/triples/#bob')
    s1._actionTriple("delete", 'cev', 'child_of', 'http://www.semanticle.org/triples/#bob')
    s1._actionTriple("add", 'cev', 'child_of', 'http://www.semanticle.org/triples/#bob')
    s1._actionTriple("add ('?desc', 'desc_of', '?ancs') :- [[[('?desc', 'child_of', '?ancs')]]]")    # add rule clause 1 to DTS._queryStore b (or change to DTS s1)
    s1._actionTriple("add",{('?obj', '?inv', '?sub'):
                          [
                              [[('?inv', 'rev_of', '?forw'),('?forw', 'rev_of', '?inv')]
                              ,[('?sub', "?forw", '?obj')]]
                             ,[[('?inv', 'syn_of', '?inv1'),('?inv1', 'syn_of', '?inv')]
                              ,[('?obj', "?inv1", '?sub')]]
                           ]})                                                        # add rule to DTS._queryStore a (or change to DTS s1)
    s1._actionTriple("add","{('?desc1', 'desc_of', '?ancs'):[[[('?child', 'child_of', '?ancs')],[('?desc1', 'desc_of', '?child')]]]}")                   # add rule clause 2 to DTS._queryStore b (or change to DTS s1)
    s1._actionTriple("add", 'ancs_of', 'rev_of', 'desc_of')                               # ant
#    s1._actionTriple("add", 'desc_of', 'rev_of', 'ancsr_of')                              # rev ant
    s1._actionTriple("add", 'des_of', 'syn_of', 'desc_of')                                # syn
#    s1._actionTriple("add", 'desc_of', 'syn_of', 'descr_of')                              # rev syn
    s1._actionTriple("add", 'anc_of', 'rev_of', 'des_of')                                 # ant of syn
#    s1._actionTriple("add", 'ancestor1_of', 'syn_of', 'ancs_of')                          # syn of ant
    s1._actionTriple("add", 'ancestor2_of', 'syn_of', 'anc_of')                           # syn of ant of syn
#    s1._actionTriple("add", 'ancestor3_of', 'syn_of', 'ancestor2_of')                     # syn of syn of ant of syn
 #    print
    print (s1._toString())
    print
    # set Queries
#    request1={('?sub','?pred','?obj'):[[('?sub=eve','?pred=child_of','?obj=dan')]]}    # pass
#    request1={('?sub','?pred','?obj'):[[("?sub='*'","?pred='*'","?obj='*'")]]}         # pass
#    request1={('?sub','?pred','?obj'):[[('?sub="*"','?pred="*"','?obj="*"')]]}         # pass
#    request1={('?sub','?pred','?obj'):[[('?sub="?"','?pred','?obj="?"')]]}             # FAIL - NO RULES RETURNED (MAYBE OK?)
#    request1={('?sub','?pred','?obj'):[[("?sub='?'","?pred","?obj='?'")]]}             # FAIL - NO RULES RETURNED (MAYBE OK?)
#    request1={('?sub','?pred','?obj'):[[('?sub=eve', "?pred=desc_of", '?obj=alice')]]} # pass
#    request1={('?sub','?pred','?obj'):[[('?sub=eve', "?pred=des_of", '?obj=alice')]]}  # pass
#    request1={('?sub','?pred','?obj'):[[('?sub', "?pred=desc_of", '?obj')]]}           # pass
#    request1={('?sub','?pred','?obj'):[[('?sub', "?pred=des_of", '?obj')]]}            # pass
#    request1={('?sub','?pred','?obj'):[[('?sub=?','?pred','?obj')
#                                       ,('?sub','?pred=?','?obj')
#                                       ,('?sub','?pred','?obj=?')]]}                   # pass - all inferences
#    reques1t={('?sub','?pred','?obj'):[[('?sub == ?','?pred','?obj')
#                                       ,('?sub','?pred = =?','?obj')
#                                       ,('?sub','?pred','?obj==?')]]}                  # pass - all rules
#    request1={('?sub','?pred','?obj'):[[('?sub','?pred','?obj')]])                     # pass
#    request2={'?person2':[[('eve', "desc_of", '?person2')]]}                                        # pass
#    request2={'?person2':[[(('ender', 'from', 'Truro'), "desc_of", '?person2')]]}                   # pass
#    request2={'?person2':[[(('ender|eddy', 'from', 'Truro'), "desc_of", '?person2')]]}              # pass
#    request2={'?person2':[[(('?person1', 'from', 'Truro'), "desc_of", '?person2')]]}                # pass
#    request2={'?person2':[[('eve', "desc_of", '?person2')]
#                         ,[('?person2', "desc_of", 'alice')]]}                                      # pass
#    request2={'?person2':[[('eve', "des_of", '?person2')]
#                         ,[('?person2', "des_of", 'alice')]]}                                       # pass - syn of recursed rule
#    request2={'?person2':[[('eve', "descr_of", '?person2')]
#                         ,[('?person2', "descr_of", 'alice')]]}                                     # pass - reversed syn of recursed rule
#    request2={'?person2':[[('alice', "ancs_of", '?person2')]
#                         ,[('?person2', "ancs_of", 'eve')]]}                                        # pass - ant of recursed rule
#    request2={'?person2':[[('alice', "ancsr_of", '?person2')]
#                         ,[('?person2', "ancsr_of", 'eve')]]}                                       # pass - reversed ant of recursed rule
#    request2={'?person2':[[('alice', "anc_of", '?person2')]
#                         ,[('?person2', "anc_of", 'eve')]]}                                         # pass - ant of syn of recursed rule
#    request2={'?person2':[[('alice', "ancestor1_of", '?person2')]
#                         ,[('?person2', "ancestor1_of", 'eve')]]}                                   # pass - syn of ant of recursed rule
    request2={('?person2'):[[('alice', "ancestor2_of", '?person2')]
                           ,[('?person2', "ancestor2_of", 'eve')]]}                                   # pass - syn of ant of syn of recursed rule
#    request2={'?person2':[[('alice', "ancestor3_of", '?person2')]
#                         ,[('?person2', "ancestor3_of", 'eve')]]}                                   # pass - syn of syn of ant of syn of recursed rule
    # generate results
    mtfacade.Facade(store=s1                                                                                # store
                   ,author=None
                   ,title='Simple Test 2'
                   ,results=[request2                                                                       # request variable
                            ,{('?sub','?pred','?obj'):[[('?sub','?pred','?obj')]]                           # ad hoc request 1
                             ,('?sub','my_desc_of','?obj'):[[('?sub','desc_of','?obj')]]                    # ad hoc request 2
                              }                                                                             # end ad hoc requests dict
                             ]                                                                              # end requests dict
                    )._generate()                                                                           # invoke generation

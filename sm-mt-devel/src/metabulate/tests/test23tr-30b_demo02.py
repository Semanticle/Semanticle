'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

Created on 04 Feb 2010
Last Updated on 13 Jul 2010

Serves as demo02

Related:
    test18             - initial Rendering transformations and sequences tests
    test23tr01/02      - as with test18 re-testing Rendering transformations and sequences
    test23tr03         - as with test23tr02 but regression tests version supporting chained generic rules
    test23tr04         - as with test23tr03 but supports queries with nested triples requiring rules to solve
    test23tr05         - as with test23tr04_demo02.py but tests refactored Queryables (from mtstores and mtsuss to mtquery)
    test23tr06         - as with test23tr04_demo02.py but tests further refactored Queryables
    test23tr_24        - as with test23tr05_demo02 but tests source supporting Distributed Triple Stores
                          - a) TS only
                          - b) DTS comprising 2 TS but behaving as TS only (ie all data in one TS)
                          - c) DTS comprising 2 TS with data in both
    test23tr_25        - as with test23tr_24 but tests source supporting merged queried rules
                          - a) TS only
                          - b) DTS comprising 2 TS but behaving as TS only (ie all data in one TS)
                          - c) DTS comprising 2 TS with data in both
    test23tr_30        - as with test23tr_25 but tests source supporting:
                                            1) query trace
                                            2) URIs and URI modelling including namespaces
                                            3) refactored folder structure
                          - a) TS only
                          - b) DTS comprising 2 TS but behaving as TS only (ie all data in one TS)
                          - c) DTS comprising 2 TS with data in both

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
    # set debug
 #   d = mtdebug.Debug()
    # assign it the criteria
#    d._update(criteria=[dc8f,dc12f,dc7f,dc13f,dc10f,dc14f,dc15f])
 #   d._update(criteria=[dc5f])
    # stores
    s1 = mtstores.DistTripleStore()
    sa = mtstores.TripleStore()
    sb = mtstores.TripleStore()
    s2 = mtstores.TripleStore()
    s1 += [sa,sb]
    # triples
    sa._actionTriple("add", 'fred', 'knows', 'bob')
    sa._actionTriple("add", ['fred','simone'], 'instance_of', 'person')
    sa._actionTriple("add", 'fido', 'instance_of', 'dog')
    sa._actionTriple("add", 'fred', 'has_job_title', 'manager')
    sa._actionTriple("add", 'fred', 'instance_of', 'person')
    sa._actionTriple("add", 'fred', 'instance_of', 'christian_name')
    sa._actionTriple("add", 'jill', 'says', [('fred', 'likes', 'simone'),
                                           ('simon', 'likes', 'simone'),
                                           ('fred', 'likes', 'fred'),
                                           ('fred', 'likes', 'fido')])
    sa._actionTriple("add", ('steven', 'from', 'London'), 'knows', ('fred', 'likes', 'janice'))
    sa._actionTriple("add", (['steven','simon'], 'from', 'London'), 'knows', ('fred', 'likes', 'simone'))
#    s1._actionTriple("add", (['?p1','?p2'], '?r1', 'London'), 'knows', ('fred', 'likes', '?p3'))
    print (s1._toString())
    print
    # set result request
    rlt01 = mtrules.Result(request=("?s"," ?r = ?r1 = 'knows'|likes|/.*?job.*?/ ","?o"))            # pass
#    rlt01 = mtrules.Result(request=("?s","?r=?r1#='knows'|likes|/.*?job.*?/","?o"))           # pass - tests generation of errorlog
    # set Content file target
    t1 = mtutils.Flatfile(path=result_path
                         ,name='Generated_t1'
                         ,type=result_type)
    # rendering submission
    p2 = mtrender.Transformation(pattern=['?o','/^(.)(.*?)(.)$/$3$2$1/'],id='?p2',targets=[t1],URImode='nativealias')
    # note1: nested content may be referenced directly or via a variable notation
    # note2: URImode controls the uri form upon which this rendering type takes place
    # p1 = mtrender.Sequence(pattern=[(p2,'is known by','?s')],targets=[t1,'display'])    # direct
    p1 = mtrender.Sequence(pattern=[('?p2','is known by','?s')] # via variable notation
                          ,targets=[s2,t1,'display']
                          ,render='csv'
                          ,URImode='nativealias')
    p4 = mtrender.Transformation(
#                                 pattern=['??og??','/^(.)(.*?)(.)$/$3$2$1/']                    # pass
                                 pattern=['?og','/^(.)(.*?)(.)$/$3$2$1/']                       # pass
#                                 pattern=['!og','/^(.)(.*?)(.)$/$3$2$1/']                       # pass - var fails correctly
#                                 pattern=['?og?','/^(.)(.*?)(.)$/$3$2$1/']                      # pass - var fails correctly
                                 ,id='?p4'
                                 ,URImode='nativealias')
    p3 = mtrender.Sequence(pattern=[
#                                    ({('?np4','?p4'):{'?og':'?o'}}                              # pass
                                    ({('np4','p4'):{'og':'?o'}}                                 # pass
#                                    ({('np4','??p4??'):{'?og':'?o'}}                            # pass
#                                    ({('??np4??','??p4??'):{'??og??':'?o'}}                     # pass
#                                    ({('?np4','?p4'):{'?og?':'?o'}}                             # pass - var ?og? fails > therefore ?og correctly interpretted as a string
#                                    ({('?np4?','?p4'):{'?og':'?o'}}                             # pass - but ?np4? correctly unusable
#                                    ({('?np4','?p4?'):{'?og':'?o'}}                             # pass - correctly issues nothing as ?p4 cannot be interpolated
                                     ,'is known by','?s')]
                          ,targets=[t1,'display']
                          ,render='csv'
                          ,URImode='nativealias')
    # set query
    rlt01._update(outputs=[p1])
#    rlt01._update(outputs=[p3])
    face01 = mtfacade.Facade(store=s1,
                             results=[rlt01])
    # execute the query
    face01._generate()
    print
    # check output channelled to a store
#    print (s2._toString())

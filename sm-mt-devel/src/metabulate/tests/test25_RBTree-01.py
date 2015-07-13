'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

Created on 23 Aug 2010
Last Updated on 23 Aug 2010

rbtree tests without the TripleStore

@author: Administrator
'''

import metabulate.utils.utils    as mtutils
import random

if __name__ == "__main__":
    tree = mtutils.srbtree()
    print '## TEST 1 ## (simple addition and reporting including nested instantiation)'
    print
    tree['b'] = 'b1'
    tree['d'] = 'd1'
    tree['e'] = 'e1'
    tree['c']['m'] = 'm1'
    print tree
    print ('comprehension: ',[k for k in tree])
    print ('comprehension: ',[(k,v) for (m,k,v) in tree._walkSubTree(tree._root)])
    for k,v in iter(tree.items()): print k,v
    print '----------------',len(tree)
    print
    print '## TEST 2 ## (adding, extracting and deleting)'
    print
    tree = mtutils.srbtree()
#    for c,k in enumerate([22,63,99,482,221,389,175]):
    for c,k in enumerate([421,423,211,199,17,212,121,295,423,189]):
        print ('adding:',c,k)
        tree[k] = c
        for c1,(n,k,v) in enumerate(tree._walkSubTree(tree._root)): print c1,'-->',n,n._getData()
        print '----------------',len(tree)
    print
    print '## TEST 2a ## (getting a sub tree matching a relative key. ie where k > 212)'
    print
    tree1 = tree._extractSubTree('>',212)
    print
    print 'iterating extracted subtree'
    for c1,(n,k,v) in enumerate(tree1._walkSubTree(tree1._root)): print c1,'-->',n,n._getData()
    print '----------------',len(tree1)
    print
    print '## TEST 2b ## (getting a sub tree matching a relative key. ie where k < 212)'
    print
    tree1 = tree._extractSubTree('<',212)
    print
    print 'iterating extracted subtree'
    for c1,(n,k,v) in enumerate(tree1._walkSubTree(tree1._root)): print c1,'-->',n,n._getData()
    print '----------------',len(tree1)
    print
    print '## TEST 2c ## (getting a sub tree matching a relative key. ie where k >= 212)'
    print
    tree1 = tree._extractSubTree('>=',212)
    print
    print 'iterating extracted subtree'
    for c1,(n,k,v) in enumerate(tree1._walkSubTree(tree1._root)): print c1,'-->',n,n._getData()
    print '----------------',len(tree1)
    print
    print '## TEST 2d ## (getting a sub tree matching a relative key. ie where k <= 212)'
    print
    tree1 = tree._extractSubTree('<=',212)
    print
    print 'iterating extracted subtree'
    for c1,(n,k,v) in enumerate(tree1._walkSubTree(tree1._root)): print c1,'-->',n,n._getData()
    print '----------------',len(tree1)
    print
    for k,v in tree1.items(): print (k,v)
    for c,k in enumerate([189,423,295,121,212,17,199,211,423,421]):
        print ('deleting:',c,k)
        del tree[k]
        for c1,(n,k,v) in enumerate(tree._walkSubTree(tree._root)): print c1,'-->',n,n._getData()
        print '----------------',len(tree)
    print
    print '## TEST 3 ## (bulk adding and iteration)'
    print
    tree = mtutils.srbtree()
    x = 5000
    print 'adding '+str(x)+' random nodes'
    print
    for c,i in enumerate(range(x)):
        k = None
        while k is None or k in tree: k = random.randint(0, 50000000)
        tree[k] = c
    print 'iterating '+str(x)+' random nodes'
    for c1,(n,k,v) in enumerate(tree._walkSubTree(tree._root)): print c1,'-->',n,n._getData()
    print '----------------',len(tree)
    print
    print '## TEST 4 ## (getting a sub tree matching a relative key. ie where k > 40000000)'
    print
    tree1 = tree._extractSubTree('>',40000000)
    print
    print 'iterating extracted subtree'
    for c1,(n,k,v) in enumerate(tree1._walkSubTree(tree1._root)): print c1,'-->',n,n._getData()
    print '----------------',len(tree1)
    for k,v in tree1.items(): print (k,v)


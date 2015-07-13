'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

fti.py Created on 21 Aug 2010
Last Updated 27 Aug 2010

Self balancing Red Black dictionary Tree
maintains indexed key:value pairs fully compatibly with Python dictionaries

References: (for specific usages see method header references)
    - http://en.wikipedia.org/wiki/Red-black_tree (V. 25-July-2010 at 05:54)
    - http://en.wikipedia.org/wiki/Tree_rotation  (V. 18-June-2010 at 23:09)

Further enhancements:
    - overloading Python dictionary methods
    - additional value added methods

24/08/2010: further compatability methods
    - with dict and between P2.6/7 and P3
    - rbtree.keys()/items()/values()

26/08/2010: rbtree._extractSubTree():
    - minor changes to op processing to handle >=/<= selections

27/08/2010: rbtree._extractSubTree():
    - bug fix to handle no extracted Sub Tree
      where self is too small to extract a pre-balanced sub tree

@author: Administrator
'''

class Node:
    def __init__(self,parent=None):
        # usage:
        #    initialise as a black leaf
        self._key    = None
        self._value  = None
        self._isRed  = False
        self._left   = None
        self._right  = None
        self._parent = parent
    def _setData(self,k,v):
        # usage:
        #    turn a leaf into a red Node containing data
        self._isRed  = True
        self._key    = k
        self._value  = v
        self._left   = Node(parent=self)
        self._right  = Node(parent=self)
    def _getData(self):
        # usage:
        #    for testing: gets tree data for self
        if self._parent is None: p = None
        else: p = self._parent._key
        if self._left is None: l = None
        else: l = self._left._key
        if self._right is None: r = None
        else: r = self._right._key
        if self._isRed: c = 'red'
        else: c = 'black'
        return (self._key,c,l,r,p)
    def _reset(self):
        # usage:
        #     to delete self by making self a leaf
        del self._left                                                          # therefore delete its leaves
        del self._right
        self._key    = None                                                     # and reset its variables to leaf values
        self._value  = None
        self._isRed  = False
        self._left   = None
        self._right  = None
    def _getGrandparent(self):
        # usage:
        #    get grandparent of self
        if self._parent: return self._parent._parent
        else: return None
    def _getUncle(self):
        # usage:
        #    get uncle of self
        g = self._grandparent
        if g is not None:
            if self._parent == g._left: return g._right
            else: return g._left
        else: return None
    def _getSibling(self):
        # usage:
        #    get sibling of self
        p = self._parent
        if p is not None:
            if self == p._left: return p._right
            else: return p._left
        else: return None
    _grandparent = property(_getGrandparent)                                    # _grandparent instance variable
    _uncle       = property(_getUncle)                                          # _uncle instance variable
    _sibling     = property(_getSibling)                                        # _sibling instance variable

class rbtree:
    def __init__(self):
        self._root = Node()
        self._size = 0
    def __len__(self):
        # usage:
        #    overrides Python len(tree)
        return self._size
    def __contains__(self,k):
        # usage:
        #    overrides Python "in" keyword
        if (not isinstance(k,int)
        and not isinstance(k,basestring)
        and not isinstance(k,tuple)
            ): raise TypeError(k)
        n = self._root
        while n._key is not None and n._key != k:
            if k > n._key: n = n._right
            else: n = n._left
        if n._key == k: return True
        else: return False
    def __setitem__(self,k,v):
        # usage:
        #    overrides Python value setting ie: tree[key] = value
        if (not isinstance(k,int)
        and not isinstance(k,basestring)
        and not isinstance(k,tuple)
            ): raise TypeError(k)
        # find the node
        n = self._root
        while n._key is not None and n._key != k:
            if k > n._key: n = n._right
            else: n = n._left
        if n._key is not None: n._value = v                                     # if node has a value reset that value
        else:                                                                   # else node is leaf: (proceed to instantiate)
            n._setData(k,v)                                                     #  turn leaf into Node with data
            self._size += 1                                                     #  increment the tree size
            self._insert(n)                                                     #  insert Node into tree
    def __getitem__(self,k):
        # usage:
        #    overrides Python value retrieval ie: value = tree[key]
        if (not isinstance(k,int)
        and not isinstance(k,basestring)
        and not isinstance(k,tuple)
            ): raise TypeError(k)
        n = self._getNode(k)
        if n is not None: return n._value
        else: raise KeyError(k)
    def __delitem__(self,k):
        # usage:
        #    overrides Python key deletion ie: del tree[key]
        if (not isinstance(k,int)
        and not isinstance(k,basestring)
        and not isinstance(k,tuple)
            ): raise TypeError(k)
        # find node to be deleted
        n = self._root
        while n is not None and n._key != k:
            if k > n._key: n = n._right
            else: n = n._left
        if n is not None:
            # find its nearest sub-tree relacement key and value (if any)
            r = None
            if n._left._key is not None: r = self._getMax(n._left)
            elif n._right._key is not None: r = self._getMin(n._right)
            if r is not None:
                # replacement found use its key and value in node to be deleted
                n._key = r._key
                n._value = r._value
            else: r = n
            # now delete the replacement (which always has at most one non-leaf child)
            # selecting the non-leaf child if available, otherwise any leaf child
            if r._left._key is not None: c = r._left
            elif r._right._key is not None: c = r._right
            else: c = r._left
            # substitute the child for the replacement, rebalance the tree, and delete the replacement
            self._replace(r,c)
            if not r._isRed:
                if c._isRed: c._isRed = False
                else: self._delete(c)
            del r
            self._size -= 1                                                     #  decrement tree size
    def __iter__(self):
        # usage:
        #    overrides Python iteration ie: for k,v in tree: ...
        n = self._root
        for (m,k,v) in self._walkSubTree(n): yield k
    def __reversed__(self):
        n = self._root
        for (m,k,v) in self._walkSubTree(n,reverse=True): yield k
    def keys(self):
        # usage:
        #    compatability with dict.keys()
        # returns
        #    list of keys (sorted in ascending order)
        # notes:
        #    in P3 dict.keys() returns a view which is a dynamic list updated as its source dict is updated
        #    for safety list(dict.keys()) will always be equivalent
        n = self._root
        return [k for (m,k,v) in self._walkSubTree(n)]
    def values(self):
        # usage:
        #    compatability with dict.values()
        # returns
        #    list of values
        # notes:
        #    in P3 dict.values() returns a view which is a dynamic list updated as its source dict is updated
        #    for safety list(dict.values()) will always be equivalent
        n = self._root
        return [v for (m,k,v) in self._walkSubTree(n)]
    def items(self):
        # usage:
        #    compatability with dict.items()
        # returns:
        #    list of (key,value) pairs (sorted in ascending key order)
        # notes:
        #    in P3 dict.items() returns a view which is a dynamic list updated as its source dict is updated
        #    for safety list(dict.items()) will always be equivalent
        n = self._root
        return [(k,v) for (m,k,v) in self._walkSubTree(n)]
    def __str__(self): return repr(self)
    def __repr__(self):
        s = ''
        n = self._root
        for (m,k,v) in self._walkSubTree(n):
            if isinstance(k,basestring): k = "'"+k+"'"
            else: k = str(k)
            if isinstance(v,basestring): v = "'"+v+"'"
            else: v = str(v)
            s += k+':'+v+',';
        if s: return '{'+s[:-1]+'}'
        else: return '{}'
    def _insert(self,n):
        # usage:
        #    inserts a Node n into self rebalancing as needed
        # references:
        #    algorithm adapted from http://en.wikipedia.org/wiki/Red-black_tree (V. 25-July-2010 at 05:54)
        #    commented case numbers match those of the above article
        # case 1
        p = n._parent
        if p is None: n._isRed = False
        # case 2
        elif p._isRed:
        # case 3
            u = n._uncle
            g = n._grandparent
            if u is not None and u._isRed:
                p._isRed = False
                u._isRed = False
                g._isRed = True
                self._insert(g)
            elif g is not None:
                # case 4
                if n == p._right and p == g._left:
                    self._rotateLeft(p)
                    n = n._left
                elif n == p._left and p == g._right:
                    self._rotateRight(p)
                    n = n._right
                # case 5
                p = n._parent
                g = n._grandparent
                p._isRed = False
                if g is not None:
                    g._isRed = True
                    if n == p._left and p == g._left: self._rotateRight(g)
                    elif n == p._right and p == g._right: self._rotateLeft(g)
    def _delete(self,n):
        # usage:
        #    removes a Node n from self rebalancing as necessary
        # references:
        #    algorithm adapted from http://en.wikipedia.org/wiki/Red-black_tree (V. 25-July-2010 at 05:54)
        #    commented case numbers match those of the above article
        # case 1
        if n._parent is not None:
            # case 2
            s = n._sibling
            p = n._parent
            if s._isRed:
                s._isRed = False
                p._isRed = True
                if n == p._left: self._rotateLeft(p)
                else: self._rotateRight(p)
                s = n._sibling                                                  # rotation will have changed this
                p = n._parent                                                   # rotation will have changed this
            # case 3
            if (s._key is not None
            and not p._isRed
            and not s._isRed
            and not s._left._isRed
            and not s._right._isRed
                ):
                s._isRed = True
                self._delete(p)
            # case 4
            elif (s._key is not None
              and p._isRed
              and not s._isRed
              and not s._left._isRed
              and not s._right._isRed
                  ):
                s._isRed = True
                p._isRed = False
            # case 5
            elif not s._isRed:
                if (n == p._left
                and s._key is not None
                and not s._right._isRed
                and s._left._isRed
                    ):
                    s._isRed = True
                    s._left._isRed = False
                    self._rotateRight(s)
                    s = n._sibling                                              # rotation will have changed this
                    p = n._parent                                               # rotation will have changed this
                elif (n == p._right
                  and s._key is not None
                  and not s._left._isRed
                  and s._right._isRed
                      ):
                    s._isRed = True
                    s._right._isRed = False
                    self._rotateLeft(s)
                    s = n._sibling                                              # rotation will have changed this
                    p = n._parent                                               # rotation will have changed this
            # case 6
            if s._key is not None:
                s._isRed = p._isRed
                p._isRed = False
                if n == p._left:
                    s._right._isRed = False
                    self._rotateLeft(p)
                else:
                    s._left._isRed = False
                    self._rotateRight(p)
    def _getPrev(self,n):
        # usage:
        #    gets the node with nearest preceeding key to that of n
        # inputs:
        #    n - current node
        # returns:
        #    node with nearest preceeding key (if one exists) or None
        if n._left._key is not None: return self._getMax(n._left)
        else:
            p = n._parent
            while p is not None and p._left == n:
                n = p
                p = n._parent
            return p
    def _getNext(self,n):
        # usage:
        #    gets the node with nearest succeeding key to that of n
        # inputs:
        #    n - current node
        # returns:
        #    node with nearest succeeding key (if one exists) or None
        if n._right._key is not None: return self._getMin(n._right)
        else:
            p = n._parent
            while p is not None and p._right == n:
                n = p
                p = n._parent
            return p
    def _getMax(self,n):
        # usage:
        #    gets the the node with the maximum key in the subtree of node n
        while n._right._key is not None: n = n._right
        return n
    def _getMin(self,n):
        # usage:
        #    gets the the node with the minimum key in the subtree of node n
        while n._left._key is not None: n = n._left
        return n
    def _rotateLeft(self,p):
        # usage:
        #    rotates tree nodes left as follows:
        #       p             q
        #      / \           / \
        #     a   q    =>   p   c
        #        / \       / \
        #       b   c     a   b
        # references:
        #    algorithm designed from http://en.wikipedia.org/wiki/Tree_rotation  (V. 18-June-2010 at 23:09)
        if p is not None:
            g = p._parent
            q = p._right
            b = q._left
            p._right = b
            b._parent = p
            q._left = p
            p._parent = q
            q._parent = g
            if g is not None:
                if p == g._left: g._left = q
                else: g._right = q
            if self._root == p:
                self._root = q
                q._isRed = False
    def _rotateRight(self,q):
        # usage:
        #    rotates tree nodes left as follows:
        #         q           p
        #        / \         / \
        #       p   c  =>   a   q
        #      / \             / \
        #     a   b           b   c
        # references:
        #    algorithm designed from http://en.wikipedia.org/wiki/Tree_rotation  (V. 18-June-2010 at 23:09)
        if q is not None:
            g = q._parent
            p = q._left
            b = p._right
            p._right = q
            q._parent = p
            q._left = b
            b._parent = q
            p._parent = g
            if g is not None:
                if q == g._left: g._left = p
                else: g._right = p
            if self._root == q:
                self._root = p
                p._isRed = False
    def _replace(self,n,m):
        # usage:
        #    replaces node n with node m
        #    fixes child link from parent of n to re-point to m
        if isinstance(n,Node) and isinstance(m,Node):
            p = n._parent
            if p is not None:
                if p._left == n: p._left = m
                else: p._right = m
            else: self._root = m
    def _getNode(self,k):
        # usage:
        #    gets a node matching a key value
        # inputs:
        #    k - key value
        # returns:
        #    n - node with key = k (if any) or None
        n = self._root
        while n._key is not None and n._key != k:
            if k > n._key: n = n._right
            else: n = n._left
        if n._key == k: return n
        else: return None
    def _walkSubTree(self,n,reverse=False):
        # usage:
        #    sorted traversing iterator of the subtree of node n yielding its node, keys and values
        # inputs:
        #    n       - subtree "root" node
        #    reverse - walk backwards [True|False]
        # yields: (in ascending key order)
        #    (m,k,v) - (node,node._key,node._value) of all non-leaf nodes
        if n._key is not None:
            if reverse: p1 = n._right; p2 = n._left
            else: p1 = n._left; p2 = n._right
            for (m,k,v) in self._walkSubTree(p1,reverse=reverse): yield (m,k,v)
            yield (n,n._key,n._value)
            for (m,k,v) in self._walkSubTree(p2,reverse=reverse): yield (m,k,v)
    def _extractSubTree(self,op,key,node=None):
        # usage:
        #    returns a new rbtree comprising only those node whose keys match op key
        # inputs:
        #    op    - operand to match key with
        #    key   - key value to match via operand
        #    node  - root node of (sub)tree
        # returns:
        #    t     - new rbtree comprising selected subset of modes from self
        # algorithm:
        #    - finds the largest in tact sub-tree matching the selection criteria
        #    - walks the remainder of self outside this sub-tree finding nodes to add to the extracted sub-tree
        def est(op,k,n):
            # usage:
            #    internal method for finding largest in tact sub-tree of self matching op key
            #    returns a copy of this sub-tree as a new rbtree
            # inputs:
            #    op - op for comparing k against node keys
            #    k  - k to compare node keys against
            #    n  - sub-tree root node
            # returns:
            #    t  - extracted sub tree as new rbtree
            if   op[0] == '>': c = n._right
            else: c = n._left
            if c._key is None: return rbtree()
            elif not (eval('c._key'+op+'k')
                  and eval('n._key'+op+'k')
                      ): return est(op,k,c)
            else:
                t = rbtree()
                import copy
                c1 = copy.deepcopy(c)
                t._root = c1
                t._size = self._subSize(c)
                c1._parent = None
                c1._isRed = False
                return t
        if isinstance(op,basestring):                                           #  validate the op
            if (op[0] != '>' and op[0] != '<'
             or (len(op) == 2 and op[1] != '=')
                ): return None
        if node is None: n = self._root                                         # start with self._root node
        else: n = node                                                          # else use sub-tree root node
        t = est(op,key,n)                                                       # get the largest compliant sub-tree
        # check if more nodes need adding from self
        if op[0] == '>':                                                        # if > search:
            if t._size:                                                         #  if sub_tree holds data:
                n = self._getPrev(self._getNode(t._getMin(t._root)._key))       #   get the predecessor node to this sub tree from self
            else: n = self._getMax(n)                                           #  else: get the node with the highest key
            while n is not None and eval('n._key'+op+'key'):                    #  while node key in range and node not None:
                t[n._key] = n._value                                            #   add it to the extract tree
                n = self._getPrev(n)                                            #   get its next predecessor from self
        else:                                                                   # else < search: (do inverse of above)
            if t._size:                                                         #  if sub_tree holds data:
                n = self._getNext(self._getNode(t._getMax(t._root)._key))       #   get the successor node to this sub tree from self
            else: n = self._getMin(n)                                           #  else: get the node with the lowest key
            while n is not None and eval('n._key'+op+'key'):                    #  while node key in range and node not None:
                t[n._key] = n._value                                            #   add it to the extract tree
                n = self._getNext(n)                                            #   get its next successor from self
        return t                                                                # return the full new extracted sub-tree
    def _subSize(self,n):
        # usage:
        #    returns the number of nodes in a subtree
        # inputs:
        #    n - subtree "root" node
        # returns:
        #    number of nodes under and including n
        if n._key is None: return 0
        else: return self._subSize(n._left) + 1 + self._subSize(n._right)
    def _maxDepth(self):
        return self._maxSubDepth(self._root)
    def _maxSubDepth(self,n):
        if n._key is None: return 0
        else: return max(self._maxSubDepth(n._left)
                        ,self._maxSubDepth(n._right)
                         )+1
    def _minDepth(self):
        return self._minSubDepth(self._root)
    def _minSubDepth(self,n):
        if n._key is None: return 0
        else: return min(self._minSubDepth(n._left)
                        ,self._minSubDepth(n._right)
                         )+1

'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

Created on 16 Feb 2010
Last Updated on 13 Jul 2010

Same as test10e.py with
    Tests parse14.py support for listed triple value expressions - parsed using a userexit

10/03/2010:
    tests added for mixed triples and vals QueryValueExpressions exploiting userexits02.py and eexp_test04.bnf

13/07/2010: updated for SVN versioning configuration and exploiting config variables

@author: Administrator
'''
import metabulate.parsers.parse         as mtparse
import metabulate.utils.utils           as mtutils
import metabulate.utils.debug           as mtdebug
import metabulate.utils.errors          as mterrors
import metabulate.singletons.singleton  as mtsingleton

if __name__ == "__main__":
    # get default file paths and types
    mtconfig   = mtsingleton.Settings()._getItem('config')
    debug_path = mtconfig._getItem('debugfile_path','%configfilesbase%Debug\\',mtconfig)
    debug_type = mtconfig._getItem('debugfile_type','txt',mtconfig)
    dc1f = mtdebug.Criteria(methods=['_deepUnion'],
                            targets=[mtutils.Flatfile(path=debug_path,
                                                      name='DebugOutput_dc1a',
                                                      type=debug_type)])
#    d = mtdebug.Debug()
#    d._update(criteria=[dc1f])
    p1 = mtparse.Parser()
    p1._setSelect(['<vop>','<var>','<val>','<sval>','<eop>','<op>','<valexp>','<vallist>','<triples>','<top>'])
    try:
        [match,bound] = p1._parse(sentence="'*'"); print ('match=',match,'bound=',bound)
        [match,bound] = p1._parse(sentence="?"); print ('match=',match,'bound=',bound)
        [match,bound] = p1._parse(sentence="'?'"); print ('match=',match,'bound=',bound)
        [match,bound] = p1._parse(sentence='"?"'); print ('match=',match,'bound=',bound)
        [match,bound] = p1._parse(sentence='?'); print ('match=',match,'bound=',bound)
        [match,bound] = p1._parse(sentence='"http://www.semanticle.org/triples#june"'); print ('match=',match,'bound=',bound)
        [match,bound] = p1._parse(sentence='fred|june'); print ('match=',match,'bound=',bound)
        #[match,bound] = p1._parse(sentence="?test='fred'"); print ('match=',match,'bound=',bound)
        #[match,bound] = p1._parse(sentence="?test"); print ('match=',match,'bound=',bound)
        #[match,bound] = p1._parse(sentence="?test=?test1"); print ('match=',match,'bound=',bound)
        [match,bound] = p1._parse(sentence='?r=?o=*|"*"|?|"?"| knows|"http://www.semanticle.org/triples#likes"|/(.*?job.*?)/'); print ('match=',match,'bound=',bound)
        #[match,bound] = p1._parse(sentence="?test='*'"); print ('match=',match,'bound=',bound)
        #[match,bound] = p1._parse(sentence="'fred'"); print ('match=',match,'bound=',bound)
        #[match,bound] = p1._parse(sentence="?test=/^?/ >=   /?$/"); print ('match=',match,'bound=',bound)
        [match,bound] = p1._parse(sentence="?test=?test1=/^?/ >=   /?$/"); print ('match=',match,'bound=',bound)
        #[match,bound] = p1._parse(sentence="?test=?test1=('a','b','c')"); print ('match=',match,'bound=',bound)
        #[match,bound] = p1._parse(sentence="?test=?test1=(('a','b','c'),'b','c')|('a','b','c')"); print ('match=',match,'bound=',bound)
        [match,bound] = p1._parse(sentence="?test=?test1!=jill|jack|(('a','b','c'),'b','c')|('a','b','c')|eve"); print ('match=',match,'bound=',bound)
        [match,bound] = p1._parse(sentence="jill|jack|(('a','b','c'),'b','c')|('a','b','c')|simon|(('a1','b1','c1'),'b1','c1')|('a','b','c')"); print ('match=',match,'bound=',bound)
        [match,bound] = p1._parse(sentence="jill|jack|(('a|a1','b','c'),'b','c')|('a','b','c')|simon|(('a1','b1','c1'),'b1','c1')|('a','b','c')"); print ('match=',match,'bound=',bound)
        [match,bound] = p1._parse(sentence='?r=?o=*|"*"|?|"?"| mine#knows-it_all | "http://www.semanticle.org/triples#likes"|/(.*?job.*?)/'); print ('match=',match,'bound=',bound)
        [match,bound] = p1._parse(sentence='http://www.semanticle.org/triples'); print ('match=',match,'bound=',bound)
        [match,bound] = p1._parse(sentence=' http://www.semanticle.org/test1/test2/triples?q=xyz&y=ghh#fragment | base#fragment'); print ('match=',match,'bound=',bound)
    except mterrors.ParseError, X:
        X._notify(c='test10h',
                  m='__main__()')                                          #   notify ParseErrors

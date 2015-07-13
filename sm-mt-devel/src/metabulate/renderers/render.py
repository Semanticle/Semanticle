'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

Created on 20 Dec 2009
render10.py Cloned from render09.py on 02 Mar 2010
render11.py Cloned from render10.py on 18 Mar 2010
render12.py Cloned from render11.py on 23 Mar 2010
render13.py Cloned from render12.py on 02 Apr 2010
render14.py Cloned from render13.py on 19 Apr 2010
render15.py Cloned from render14.py on 04 May 2010
render16.py Cloned from render15.py on 12 May 2010
render17.py Cloned from render16.py on 12 Jun 2010
render.py Cloned from render17.py on 07 Jul 2010
Last Updated 22 Oct 2010

As render09 with:
    version re-engineered with undefined setters = None
    and defaults with null setters
    also mtutils.empty() = None

04/01/2010:
    uses singleton settings['errors']

14/01/2010:
    _interpolate() minor bug fix from failed var extraction/interpolation from strings
    _extractVarID() minor bug fix where string has var prefix but fails exact pattern - now returns null
    _getValues/_prepareVars()/_generate() all set default arguments to sentinel None for extra safety

16/01/2010:
    Configurable Exception Handling - exploits mterrors

26/01/2010:
    - supports reserved variable keywords as a global (in future these could be preferences)
    - including new ?!rules variable

02/03/2010 render10.py cloned from render09.py with:
    - singleton03 exploited

18/03/2010 render11.py cloned from render10.py with:
    - exploits non-infered QueryExpression comperands

23/03/2010 render12.py cloned from render11.py with:
    - exploits new mtstores._expandTriple(expandRules=True)

25/03/2010 explots new mtprotocols _factory method

02/04/2010 render13.py cloned from render12.py with:
    - exploits refactored mtstores for DistSimpleTripleStore support

06/04/2010 exploits mtutils._genericSetter()/_genericGetter() for just in time attribute instantiation

08/04/2010 config and prefs updates:
    - several new softcoded prefs defined
    - hardcoded config and prefs also defined

09/04/2010 standardisation of getter/setter and attribution syntax:
    _get(), _set(), _update() and __init__() methods checked regarding attribution.
    General rule is to reserve getters and setters to externally accessible and decorated attributes.
    These can also be used for just in time attribution (though this isn't currently so outside of the former criteria).
    Attribute setting via _update and __init__ strictly for external accessible attributes.
    Code changed throughout to access all other undecorated attributes directly.
    Python property not currently used to map _get/_set to direct attribute access syntax.

10/04/2010:
    - Content._setRender() exploits Protocols._getAvailable() for membership validation

15/04/2010:
    - _deliver() invokes STS._actionTriple(item) not *item otherwise values get dropped from dict args used for rules

19/04/2010 render14.py cloned from render13.py with:
    - Persistent Triple Stores supported

04/05/2010 render15.py cloned from render14.py with:
    - URI's supported.

11/05/2010 supports choice of URI output generations:
    - preference setting and local Content instance overriding supporting URI formats [export|native|nativenamespace]
    - outputs exploit mtstores._expandTriple() passing the UID mode and target store:
       - rendered outputs in specified or prefered URI format
       - instantiated outputs in URI format native to the target store

12/05/2010 render16.py cloned from render15.py with:
    - explicit alias_ontology support (via imports)

12/06/2010 render17.py cloned from render16.py with:
    - folders re-configured

07/07/2010 render.py cloned from render17.py for SVN versioning

12/07/2010 settings support interpetation of config variables

13/07/2010 Transformation._generate():
    - exploits stores._expandTriple with URImode for local URImode rendering
    - as per Sequence._generate(), but old code left in commented out for time being

02/08/2010 Content._termination():
    - generation of output termination string
    - inheritted from Facade or Result (if not False)
    - but can be overridden by Output terminator or Target terminator (if a file)
    - file target terminator may be overidden by ResultsFileTerminator pref if False

03/08/2010 enhanced headers and footers:
    - terminator renamed as footer
    - headers added
    - both headers and footers support various optional variable substitutions

06/08/2010 ad-hoc "sticky" header footer string and variable updates supported

24/08/2010:
    - Forwards compatability updates between P2.6/7 and P3
      in handling support of keys(), iteritems(), sort(), map(), itemgetter() and has_key().

27/08/2010 Towards handling of invalid default settings:
    - all defaults used only by _genericSetter() are now obtained in dual format comprising:
        - the supplied default via settings
        - a backup last resort hardcoded default if this is invalid

20/10/2010 Compliance with mtstores refactoring

22/10/2010: Stage 5:  Mixed triple ordering support: Optional re-ordering for IO
    _deliver ensures TripleStore._actionTriple() won't re-order triples to be instantiated

@author: Administrator
'''

import re
import copy
import time
import metabulate.stores.structured     as mtstruct
import metabulate.renderers.protocol    as mtprotocol
import metabulate.utils.utils           as mtutils
import metabulate.utils.debug           as mtdebug
import metabulate.utils.errors          as mterrors
import metabulate.singletons.singleton  as mtsingleton

i_ids = mtutils.sdict()                                                         # Python equivalent of a class variable - index of ids to Content objects
mtprefs  = mtsingleton.Settings()._getItem('prefs')
reserved = ['?!triples','?!rules','?!equations']
mtdft = mtutils.sdict()
mtdft['header'] = mtutils._logical(mtprefs._interpretItem('ResultsHeader_for_Files','None')) # Default file output header
mtdft['footer'] = mtutils._logical(mtprefs._interpretItem('ResultsFooter_for_Files','None')) # Default file output footer

class Content:
    _default_id       = ''                                                      # variable id
    _default_mode     = mtprefs._interpretItem('ContentDefaultMode'             # generation mode [all|any|triples|relations] where:
                                              ,'triples',2)                     #  - triples ensures all tuples have 3 elements
                                                                                #  - other modes not yet exploited
    _default_render   = mtprefs._interpretItem('ContentDefaultRender','py',2)   # rendering Protocol [whatever is supported by mtprotocol]
    _default_URImode  = mtprefs._interpretItem('ContentDefaultURI'
                                              ,'nativealias',2)                 # URI mode for rendered outputs [export|native|nativealias]
    _default_targets  = []                                                      # list of target objects accumilating values (string|file|triplestore,relstore,display)
    _default_source   = None                                                    # source object (where this Content is defined - e.g. a file, maybe later a TripleStore query?)
    _default_prefix   = mtprefs._interpretItem('ContentDefaultPrefix','',2)     # prefix Sequences with sequence action (add|delete) MAY NOT BE USED
    _default_unique   = mtprefs._interpretItem('ContentDefaultUnique','on',2)   # filter to output unique patterns (on(yes)|off(no)) - default = on
    _default_pattern  = mtutils.slist()                                         # the pattern for generation
    _default_header   = None                                                    # default output header (IE. use Result or Facade header)
    _default_footer   = None                                                    # default output footer (IE. use Result or Facade footer)
    _default_author   = None                                                    # author variable for value substitution in headers and footers
    _default_title    = None                                                    # title variable for value substitution in headers and footers
    # internal just in time variable settings
    def __init__(self
                ,id=None
                ,prefix=None
                ,pattern=None
                ,mode=None
                ,unique=None
                ,render=None
                ,source=None
                ,targets=None
                ,URImode=None
                ,header=None
                ,footer=None
                ,author=None
                ,title=None
                 ):
        self._map      = mtutils.sdict()                                         # dict mapping generic to specific variables
        self._luw      = str(time.time())                                        # luw id as a millisecond timestamp (used for logical results aggregation in various target types)
        self._instance = 0                                                       # instance id
        self._update(id=id
                    ,prefix=prefix
                    ,pattern=pattern
                    ,mode=mode
                    ,unique=unique
                    ,render=render
                    ,source=source
                    ,targets=targets
                    ,URImode=URImode
                    ,header=header
                    ,footer=footer
                    ,author=author
                    ,title=title
                    )
    def _update(self
               ,id=None
               ,prefix=None
               ,pattern=None
               ,mode=None
               ,unique=None
               ,render=None
               ,source=None
               ,targets=None
               ,URImode=None
               ,header=None
               ,footer=None
               ,author=None
               ,title=None
                ):
        if id         is not None: self._setId(id)
        if prefix     is not None: self._setPrefix(prefix)
        if mode       is not None: self._setMode(mode)
        if render     is not None: self._setRender(render)
        if source     is not None: self._setSource(source)
        if targets    is not None: self._setTargets(*targets)
        if pattern    is not None: self._setPattern(pattern)
        if unique     is not None: self._setUnique(unique)
        if URImode    is not None: self._setURImode(URImode)
        if header     is not None: self._setHeader(header)
        if footer     is not None: self._setFooter(footer)
        if author     is not None: self._setAuthor(author)
        if title      is not None: self._setTitle(title)
    def copy(self): return copy.copy(self)
    def _getObject(self,id):
        if isinstance(id,basestring) and id in i_ids: return i_ids[id]
        else: return 0
    def _showDebug(self
                  ,clas=''
                  ,method=''
                  ,note=''
                  ,vars=[]
                  ,line=''
                  ,level=2
                   ):
        mtdebug.Debug()._notify(clas=clas,method=method,note=note,line=line,level=level,vars=vars)
    def _setId(self,*args):
        v = mtutils._genericSetter(self,'id',args,t=basestring
                                  ,f='_extractVarID(i,"?")',fobj=self
                                   )
        if v: i_ids[v] = self
        return v
    def _getId(self,default=True):
        return mtutils._genericGetter(self,'id',default)
    def _setMode(self,*args):                                                   # generation mode (all|any|triples|relations) - default = triples
        return mtutils._genericSetter(self,'mode',args,m=['all','any','triples','relations'])
    def _getMode(self,default=True):
        return mtutils._genericGetter(self,'mode',default)
    def _setPrefix(self,*args):
        return mtutils._genericSetter(self,'prefix',args,m=['add','delete'])
    def _getPrefix(self,default=True):
        return mtutils._genericGetter(self,'prefix',default)
    def _setURImode(self,*args):
        return mtutils._genericSetter(self,'URImode',args,m=['export','native','nativealias'])
    def _getURImode(self,default=True):
        return mtutils._genericGetter(self,'URImode',default)
    def _setHeader(self,*args):
        return mtutils._genericSetter(self,'header',args)
    def _getHeader(self,default=True):
        return mtutils._genericGetter(self,'header',default)
    def _setFooter(self,*args):
        return mtutils._genericSetter(self,'footer',args)
    def _getFooter(self,default=True):
        return mtutils._genericGetter(self,'footer',default)
    def _setAuthor(self,*args):
        return mtutils._genericSetter(self,'author',args)
    def _getAuthor(self,default=True):
        return mtutils._genericGetter(self,'author',default)
    def _setTitle(self,*args):
        return mtutils._genericSetter(self,'title',args)
    def _getTitle(self,default=True):
        return mtutils._genericGetter(self,'title',default)
    def _setRender(self,*args):
        return mtutils._genericSetter(self,'render',args
                                     ,m=mtprotocol.Protocols()._getAvailable()
                                     ,f='_factory(i)',fobj=mtprotocol.Protocols()
                                      )
    def _getRender(self,default=True):
        return mtutils._genericGetter(self,'render',default)
    def _setSource(self,*args):                                                 # source object (where this Content is defined - e.g. a file, maybe later a TripleStore query?)
        v = mtutils._genericSetter(self,'source',args,t=mtutils.Flatfile)
        if v:
            fn = v._getFullname()
            if fn:
                f = open(fn,'r')
                pattern = f.read()
                pattern = self._setPattern(pattern)
                fn.close()
        return v
    def _getSource(self,default=True):
        return mtutils._genericGetter(self,'render',default)
    def _setTargets(self,*args):
        # usage:
        #    sets a list of targets of type:
        #     (TestStore|Flatfile|TripleStore|RelationalStore|'display'|'render')
        #     where 'render' doesn't get delivered anywhere but renderedValue may be used by parent Content
        #    sets doRender where targets include types requiring the renderedValue
        if not args:
            self._targets  = self._default_targets
            self._doRender = ''
        else:
            t1 = []
            dr = ''
            for t in args:
                if t not in t1:
                    ok = 1
                    if (t=='display' or
                        t=='render' or
                        isinstance(t,mtutils.FlatStore)
                        ): dr = 'y'
                    elif not isinstance(t,mtstruct.StructuredStore):
                        ok = 0
                    if ok: t1 += [t]
            self._targets = t1
            self._doRender = dr
        return self._targets
    def _getTargets(self,default=True):
        return mtutils._genericGetter(self,'targets',default)
    def _setUnique(self,*args):                                                 # filter to output unique patterns (on(yes)|off(no)) - default = on
        return mtutils._genericSetter(self,'unique',args,m=[True,False],logical=True)
    def _getUnique(self,default=True):
        return mtutils._genericGetter(self,'unique',default)
    def _getPattern(self,default=True):                                         # the pattern for generation
        v = mtutils._genericGetter(self,'pattern',default)
        self._showDebug(clas='Content',method='_getPattern',note='returns',line=319,level=0,vars=[['v',v]])
        return v
    def _getValues(self, instance=None, bound=None, store=None):
        # usage:
        #    gets value, renderedValue and bound if these already exist for this instance
        #    otherwise it generates and sets the renderedValue (by calling _generate()) then gets it
        self._showDebug(clas='Content',method='_getValue',note='inputs',line=325,level=0,vars=[['instance',instance],['bound',bound],['store',store]])
        if not instance or instance != self._instance:
            self._value,self._renderedValue,bound = self._generate(instance=instance, bound=bound, store=store)
        self._showDebug(clas='Content',method='_getValue',note='returns',line=328,level=0,vars=[['self._value',self._value],['self._renderedValue',self._renderedValue],['bound',bound]])
        return self._value,self._renderedValue,bound
    def _extractVarID(self,s,y):
        # usage
        #    utility routine for extracting a variable ID from a candidate variable string
        # inputs:
        #    s = string
        #    y = symbol identifying variable
        # returns:
        #    the variable if ok or
        #    false if not
        self._showDebug(clas='Content',method='_extractVarID',note='inputs',line=339,level=0,vars=[['s',s],['y',y]])
        s1 = 0
        if s[0] == y and len(s) > 1:                                            #  if a query variable
            if (s[:2] == y*2 and
                  s[-2:] == y*2 and
                  len(s) > 4): s1 = s[2:-2]                                     #   set from full form or
            elif s[-1] != y: s1 = s[1:]                                         #   set from short form
        self._showDebug(clas='Content',method='_extractVarID',note='returns',line=346,level=0,vars=[['s1',s1]])
        return s1
    def _interpetVar(self,s):
        # usage:
        #    Utility method to interpret one variable at a time in Content objects for later value interpolation
        #    Variables may be query or Content variables denoted in full or short notation
        #    Variables may also be generic variables denoted in full or short notation
        #    Finally variables may map a Generic Content variable to a specific one
        #     using a dictionary entry for the Variable in the Cobject as follows:
        #     {(Id,genericObject):{genericVariable1:mappedSpecicVariable1,..,genericVariableN:mappedSpecicVariableN}}
        # inputs:
        #    i  - slot string which may comprise a variable binding
        #            ?queryvar|??queryvar??|
        #            !generic_mapped_var|!!generic_mapped_var!!|
        #            [?]contentvar|string|
        #            mapping: {(Id,genericObject):{genericVariable1:mappedSpecicVariable1,..,genericVariableN:mappedSpecicVariableN}}
        #            where: genericObject may be supplied as the Python object or its id with or without variable notation
        # returns:
        #    original object or specialised copy of a mapped generic Content object
        self._showDebug(clas='Content',method='_interpetVar',note='inputs',line=365,level=0,vars=[['s',s]])
        s1 = 0
        if isinstance(s,basestring):                                            # if candidate variable is a string
            s1 = self._extractVarID(s,'?')                                      #  try getting the variable ID
            if s1:                                                              #  if variable found:
                g1 = self._getObject(s1)                                        #   check if represents a nested Content object
                if g1: s1 = self._interpetVar(g1)                               #   if it does interpret it
            elif (s[0] == '{' and                                               #  else try a dict for evaluation
                s[-1] == '}' and
                len(s) > 13):
                try:                                                            #  top level try:
                    try:                                                        #   try escalating lower exceptions
                        s1 = eval(s)
                        if isinstance(s,dict): s1 = self._interpetVar(s1)       #    if its a dictionary recurse to process
                    except: raise mterrors.PatternDictionaryError(s)            #    except: escalate with PatternException
                except mterrors.PatternDictionaryError, X:
                    X._notify(c='Content',
                              m='_interpetVar()')                               #  notify PatternDictionaryError
        elif isinstance(s,dict):                                                # elif candidate dict specifying generic mappings
            self._showDebug(clas='Content',method='_interpetVar',line=384,level=1,vars=[['s',s]])
            for g in s:                                                         #  get id tuple and mappings (should be just one)
                if (isinstance(g,tuple) and                                     #   check its a tuple
                    len(g) == 2 and                                             #             length 2
                    isinstance(s[g],dict)):                                     #             indexing a dict:
                    if isinstance(g[1],basestring):                             #   if generic object is a string:
                        g1 = self._extractVarID(g[1],'?')                       #    try extracting id from var notations
                        if not g1: g1 = g[1]                                    #    if not then assume id without notation
                        g1 = self._getObject(g1)                                #    try getting the Content object from its id
                    else: g1 = g[1]                                             #   else assume this is the object itself
                    if isinstance(g1,Content):                                  #   test object exists
                        s1 = g1.copy()                                          #    instantiate a generic Content object copy
                        s1._setId(g[0])                                         #    and specialise: update its id to the new id
                        s1._luw = self._luw                                     #                    update luw to parent luw
                        map = s1._map                                           #    get its variable map
                        self._showDebug(clas='Content',method='_interpetVar',line=399,level=2,vars=[['s1',s1],['s1._id',s1._id],['s1._map',s1._map]])
                        for gv in s[g]:                                         #    for each supplied generic mapped variable:
                            s2 = self._interpetVar(s[g][gv])                    #     try getting its mapped query/content variable
                            if s2:                                              #     if found:
                                g2 = self._extractVarID(gv,'?')                 #      try extracting id from var notations
                                if not g2: g2 = gv                              #      if not then assume id without notation
                                map[g2] = s2                                    #     map generic to specific variable ids
                        s1._map = map                                           #    set the updated map
                        self._showDebug(clas='Content',method='_interpetVar',line=407,level=2,vars=[['s1._id',s1._id],['s1._map',s1._map]])
        elif isinstance(s,Content):                                             # elif its a Content object:
            s._luw = self._luw                                                  #  set luw of child Content to that of its Parent
            s1 = s                                                              #  prepare to return this object
        self._showDebug(clas='Content',method='_interpetVar',note='returns',line=411,level=0,vars=[['s1',s1]])
        return s1
    def _interpolate(self,i,b,id,s):
        # usage:
        #    Utility method to interpolate a variable in a Content object
        #     by supplying its value and binding this to the variable
        #    Variables may be query or Content variables denoted in full or short notation
        #    Variables may also be generic variables denoted in full or short notation
        #    The values for generic variables are obtained from the Query or Content
        #     variables then generic variable is mapped to
        # inputs:
        #    i  - slot string which may comprise a variable binding
        #            ?queryvar|??queryvar??|
        #            !generic_mapped_var|!!generic_mapped_var!!|
        #            [?]contentvar|string
        #    b  = variable bindings for variable substitutions
        #    id = instance id
        #    s  = expand id store
        # returns:
        #    interpolated value and
        #    updated variable bindings
        self._showDebug(clas='Content',method='_interpolate',note='inputs',line=432,level=0,vars=[['i',i],['b',b],['id',id],['s',s]])
        rv = v = None
        if isinstance(i,Content):                                               # if item is a nested Content object:
            v,dummy,b = i._getValues(bound=b,                                   #  get value of this Content object
                                     instance=id,                               #  get updated/supplemented bindings
                                     store=s)
            if i._getId(): b[i._getId()] = v                                    #  if item has an id: bind its value to this
        elif isinstance(i,basestring):                                          # elif item is a string:
            i1 = self._extractVarID(i,'?')                                      #  try getting a variable
            if i1:                                                              #  if a variable:
                if i1 in b: v = b[i1]                                           #   if var is bound get its value
                else:                                                           #   else:
                    map = self._map                                             #    get the map
                    if i1 in map:                                               #    if generic var mapped to specific variable
                        if map[i1] in b: v = b[map[i1]]                         #     get its value from this via the map
            if v is None: rv = v = i                                            #  otherwise treat as literal string
        if (v is not None and                                                   # test to see if item is a triple ID needing expansion
            isinstance(s,mtstruct.A_TripleStore)):                              #  if a query store is supplied:
            rv = self._getRender()._translate(s._expandTriple(v,uri=self._getURImode())
                                             ,endline='no'
                                              )                                 #  expand any triple ids from the query store
        self._showDebug(clas='Content',method='_interpolate',note='returns',line=453,level=0,vars=[['v',v],['rv',rv],['b',b]])
        return v,rv,b
    def _deliver(self,v,rv,instance,store):
        # usage:
        #    deliver generated values to targets
        #    updating the current instance variable
        # inputs:
        #    v        = Content value (unrendered) with URIs expressed in terms of store
        #    rv       = Rendered Content Value (rendered) with URIs expressed in terms of store
        #    instance = The current instance
        #    store    = source store
        self._showDebug(clas='Content',method='_deliver',note='inputs',line=464,level=0,vars=[['v',v],['rv',rv],['instance',instance]])
        self._instance = instance                                               # update this instance
        if v is not None:                                                       # if result not None
            v1 = copy.deepcopy(v)
            if isinstance(v,mtutils.slist): v1 = v1._peel(leave=1)              # if a list: normalise its nesting
            elif not isinstance(v1,list): v1 = [v1]
            self._showDebug(clas='Content',method='_deliver',line=470,level=1,vars=[['v1',v1]])
            for t in self._getTargets():                                        #  generate outputs
                if isinstance(t,mtstruct.StructuredStore):                      #   if target is a store: (proceed to instantiate it)
                    for i in v1:                                                #    for each current result:
                        if (isinstance(store,mtstruct.A_TripleStore)            #     represent triples in native URIs of target TripleStore
                        and isinstance(t,mtstruct.A_TripleStore)                #     if both source and target stores are TripleStores:
                            ): i1 = store._expandTriple(i                       #     expand result with native URIs for target store
                                                       ,expandRules=True
                                                       ,uri='native'
                                                       ,target=t
                                                        )
                        else: i1 = i
                        self._showDebug(clas='Content',method='_deliver',line=482,level=2,vars=[['i1',i1],['i',i]])
                        t._tioTripleOrder = 'forceNone'                         #    Content pattern specifies order. So don't re-order!
                        t._actionTriple(i1)                                     #    instantiate (remember v contains list of triples)
                        t._tioTripleOrder = None                                #    clear mandatory non re-ordering
                elif isinstance(t,mtutils.FlatStore):                           #   else update FlatStore (TextStore or Flatfile)
                    t._setValue(rv+'\n',luw=self._luw)                          #    passing root deliverable luw (remember deliverables may share targets, therefore they mustn't overwrite eachother because of differing luws)
                elif t == 'display': print rv                                   #   else update display with display rv
        return v
    def _defaultheadfooter(self
                          ,role
                          ,hfstring
                          ,hfvars
                          ,header=None
                          ,footer=None
                          ,author=None
                          ,title=None
                          ):
        # usage:
        #    outputs terminator checking if Result term is overidden by:
        #    1. An output specific terminator
        #    2. A target specific terminator (in the case of file outputs - for example to switch off)
        # inputs:
        #    role     - header or footer
        #    hfstring - header or footer string depending on role
        #    hfvars   - dict indexing header footer variable values by name
        #    header   - updated Content header string or False (if any)
        #    footer   - updated Content footer string or False (if any)
        #    author   - updated Content author (if any)
        #    title    - updated Content title (if any)
        # returns:
        #    output specific terminator
        self._update(header=header                                              # instantiate ad-hoc Content instance variables
                   ,footer=footer                                               #  as "sticky" updates
                   ,author=author
                   ,title=title
                    )
        if role == 'header':   term1 = self._getHeader()                        # based on role get Content specific header or footer
        elif role == 'footer': term1 = self._getFooter()
        else: return None                                                       # if role is wrong quit
        if term1 is None: term1 = hfstring                                      # if its None: use the supplied Result string
        if term1 is not False:                                                  # only proceed if resulting string is not False
            hfvars1 = copy.deepcopy(hfvars)                                     # ensure variable index updates are local
            author = self._getAuthor()                                          #  get Content specific author
            if author is not None: hfvars1['author'] = author                   #  if not None: use it
            title = self._getTitle()                                            #  get Content specific title
            if title is not None: hfvars1['title'] = title                      #  if not None: use it
            for t in self._getTargets():                                        #  get each target:
                if (isinstance(t,mtutils.FlatStore)                             #   if target is a file
                and mtdft[role] is not False):                                  #   and default role specific file string not False:
                    if role == 'header': term2 = t._getHeader()                 #    get role specific ad-hoc string (if any)
                    else: term2 = t._getFooter()
                    if term2 is None:                                           #    if its None:
                        if mtdft[role] is not None: term2 = mtdft[role]         #     use default file output terminator if not None
                        else: term2 = term1                                     #     else: revert to Result or Output terminator
                    if term2 is not False and term2 is not None:                #    if its not None or False:
                        term2 = hfvars1._doSubs(term2)                          #     do variable substitutions on curr File string
                        t._setValue(term2+'\n',luw=self._luw)                   #     output it
                elif t == 'display' and term1 is not None:                      #   else not None display output:
                    term2 = hfvars1._doSubs(term1)                              #    do variable substitions on display string
                    print term2                                                 #    and print to display
        return term1
    def _getDoRender(self):
        self._getTargets()
        return self._doRender
class Output(Content): pass
class Input(Content): pass
class Sequence(Output, Input):
    _default_render = mtprefs._interpretItem('SequenceDefaultRender','text',2)  # rendering Protocol
    def __init__(self
                ,id=None                                                        # variable id
                ,prefix=None                                                    # prefix Sequences with sequence action (add|delete) MAY NOT BE USED
                ,pattern=None                                                   # the pattern for generation
                ,mode=None                                                      # generation mode (all|any|triples|relations) - default = triples
                ,unique=None                                                    # filter to output unique patterns (on(yes)|off(no)) - default = on
                ,render=None                                                    # rendering Protocol
                ,source=None                                                    # source object (where this Content is defined - e.g. a file, maybe later a TripleStore query?)
                ,targets=None                                                   # list of target objects accumilating values (string|file|triplestore,relstore,display)
                ,URImode=None                                                   # URImode for this output
                ,header=None                                                    # header for this output
                ,footer=None                                                    # footer for this output
                ,author=None
                ,title=None
                 ):
        Content.__init__(self
                        ,id=id
                        ,prefix=prefix
                        ,pattern=pattern
                        ,mode=mode
                        ,unique=unique
                        ,render=render
                        ,source=source
                        ,targets=targets
                        ,URImode=URImode
                        ,header=header
                        ,footer=footer
                        ,author=author
                        ,title=title
                         )
    def _setPattern(self, pattern):
        # usage:
        #    checks pattern syntax, sets the pattern instance variable and
        #    submits to _prepareVars() to interpret specific Query/Content variables
        #    or Generic variables mapped to these
        # inputs:
        #    CSV Sequence of query or Content variables, or nested Content or Sequences
        # item syntax:
        #    ?queryvariablename
        #    ?ContentVariable
        #    ContentVariable
        #    Sequence
        # note:
        #    NOTE the notes for _perpareVars() on support for list propogation notation.
        self._showDebug(clas='Sequence',method='_setPattern',note='inputs',line=592,level=0,vars=[['pattern',pattern]])
        if not pattern: self._pattern = self._default_pattern
        else:
            newspec = mtutils.slist()
            if not (isinstance(pattern,list) or
                    isinstance(pattern,tuple)): pattern = [pattern]
            self._showDebug(clas='Sequence',method='_setPattern',line=598,level=1,vars=[['pattern',pattern]])
            for s in pattern:                                                   # for each sub-sequence:
                self._showDebug(clas='Sequence',method='_setPattern',line=600,level=1,vars=[['s',s],['pattern',pattern]])
                try: s = self._prepareVars(spec=s)                              #  try preparing variables
                except mterrors.PatternError, X:
                    X._notify(c='Sequence',
                              m='_setPattern()')                                # notify PatternError
                self._showDebug(clas='Sequence',method='_setPattern',line=605,level=1,vars=[['s',s],['pattern',pattern],['newspec',newspec]])
                newspec += [s]
            self._pattern = newspec
        self._showDebug(clas='Sequence',method='_setPattern',note='returns',line=608,level=0,vars=[['self._pattern',self._pattern]])
        return self._pattern
    def _prepareVars(self, spec=None):
        # usage:
        #    prepares variables for later interpolation
        # inputs:
        #    sub-Sequence of raw variables
        # outputs:
        #    sub-Sequence of prepared variables
        # notes: IMPORTANT
        #    This method complies with requirements of stores._actionTriple()/_processTriple()
        #     for supporting triple propogation from list notation by preserving
        #     supplied tuple and list structures.
        #     Therefore it does not need to implement this propogation itself.
        #    Indeed if the sequence is required to output propogated triples, pre-propogated
        #     patterns can be supplied direct to the Sequence by the user for this purpose.
        self._showDebug(clas='Sequence',method='_prepareVars',note='inputs',line=624,level=0,vars=[['spec',spec]])
        if isinstance(spec,tuple) or isinstance(spec,list):
            if isinstance(spec,tuple):
                if self._getMode() == 'triples' and len(spec) != 3:
                    raise mterrors.PatternTripleSizeError(spec,len(spec))
                if len(spec) < 1: raise mterrors.PatternEmptyError()
            newspec = mtutils.slist([self._prepareVars(spec=s) for s in spec])
            if isinstance(spec,tuple): newspec = tuple(newspec)
        else:
            newspec = self._interpetVar(spec)
            if not isinstance(newspec,Content): newspec = spec                              # flip returned binding if a Content variable - ie it might be a copy of a generic one.
        self._showDebug(clas='Sequence',method='_prepareVars',note='returns',line=635,level=0,vars=[['newspec',newspec]])
        return newspec
    def _generate(self, bound=None, instance=None, store=None):
        # usage:
        #    expands nested webs into nested triples for display
        #    called from _getValues
        # inputs
        #    bound     = variable bindings for variable substitutions
        #    instance  = result instance
        #    store     = TripleStore for expanding ids of nested triples
        # note:
        #    bound['!unique']    = is this result unique? true(y)|false
        #                          this is the overall result uniqueness
        #                          not the uniqueness of the bindings applying to this Content object
        #    bound['!triples']   = matching triples
        #    bound['!rules']     = matching rules
        #    bound['!equations'] = equations solved
        def generate(l,b,id,s,m):
            # 'private method'
            # inputs
            #    l  = list of web patterns to generate
            #    b  = variable bindings for variable substitutions
            #    id = instance id
            #    s  = expand id store
            #    m  = content completeness mode
            r = mtutils.slist()                                                 # default return sequence
            rv = mtutils.slist()                                                # default rendered return sequence
            if len(l) > 0:                                                      # only proceed if list contains something:
                for p in l:                                                     #  for each item in sequence
                    if isinstance(p,list):                                      #   if item is a list:
                        i,ri,b = generate(p,b,id,s,m)                           #    get value by generating this item
                    elif isinstance(p,tuple):                                   #   if item is a tuple:
                        i,ri,b = generate(p,b,id,s,m)                           #    get value by generating this item
                        if i is not None:
                            i = tuple(i); ri = tuple(ri)                        #    ensure results are tuples
                    else: i,ri,b = self._interpolate(p,b,id,s)                  #   else interpolate value and updated bindings
                    if i is None:                                               #   if completeness fails:
                        if m == 'all':
                            rv = r = i                                          #    escalate None return value
                            break
                    else:                                                       #   else: append value to return sequence
                        if p in reserved: r += i                                #    if a reserved variable its already a list
                        else: r += [i]                                          #    else append as a list
                        rv += [ri]
            return r,rv,b                                                       # return the sequence
        self._showDebug(clas='Sequence',method='_generate',note='inputs',line=680,level=0,vars=[['bound',bound],['instance',instance],['store',store]])
        rv = v = None                                                           # default None new value and renderedValue
        self._showDebug(clas='Sequence',method='_generate',note='inputs',line=682,level=0,vars=[["bound['!unique']",bound['!unique']],['self._getUnique()',self._getUnique()]])
        if bound['!unique'] or not self._getUnique():                           # proceed only if uniqueness constraint satisfied
            mode = self._getMode()                                              # now get Completeness mode
            if mode == 'triples': mode = 'all'                                  # re-express as 'all'|not 'all'
            self._showDebug(clas='Sequence',method='_generate',line=686,level=1,vars=[['mode',mode],['self._getPattern()',self._getPattern()]])
            if self._getPattern():                                              # if pattern:
                i,ri,bound = generate(self._getPattern(),                       #  generate the new temp value and (potentially) updated bindings
                                      bound,
                                      instance,
                                      store,
                                      mode)
                self._showDebug(clas='Sequence',method='_generate',line=693,level=1,vars=[['i',i],['ri',ri],['bound',bound]])
                if not (mode == 'all' and i is None):                           #  if new temp value satisfies completeness test                                                    #  if a new temp value:
                    v = i; rv = ri                                              #   default new renderedValue
                    p = self._getPrefix()                                       #  get prefix
                    if p: v.insert(0,p)                                         #  if a prefix insert it
                    if (self._getDoRender() and
                        isinstance(store,mtstruct.A_TripleStore)):              #  if rendering required:
                        rv = self._getRender()._translate(store._expandTriple(v,expandRules=True,uri=self._getURImode())
                                                         ,endline='no')         #   set rendered value to rendered result
                    else: rv = v                                                #  else render value is value
        v = self._deliver(v,rv,instance,store)                                  # deliver generations to targets
        self._showDebug(clas='Sequence',method='_generate',note='returns',line=704,level=0,vars=[['rv',rv],['bound',bound]])
        return v,rv,bound                                                       # return new rendered value (or None if failed) and updated bindings
class Transformation(Output, Input):
    _default_render = mtprefs._interpretItem('TransformationDefaultRender'
                                            ,'text',2)                          # rendering Protocol
    def __init__(self
                ,id=None                                                        # variable id
                ,prefix=None                                                    # prefix Sequences with sequence action (add|delete) MAY NOT BE USED
                ,pattern=None                                                   # the pattern for generation
                ,mode=None                                                      # generation mode (all|any|triples|relations) - default = triples
                ,unique=None                                                    # filter to output unique patterns (on(yes)|off(no)) - default = on
                ,render=None                                                    # rendering Protocol
                ,source=None                                                    # source object (where this Content is defined - e.g. a file, maybe later a TripleStore query?)
                ,targets=None                                                   # list of target objects accumilating values (string|file|triplestore,relstore,display)
                ,URImode=None                                                   # URImode for this output
                ,header=None                                                    # header for this output
                ,footer=None                                                    # footer for this output
                ,author=None
                ,title=None
                 ):
        self._re=''
        self._ep=[]
        Content.__init__(self
                        ,id=id
                        ,prefix=prefix
                        ,pattern=pattern
                        ,mode=mode
                        ,unique=unique
                        ,render=render
                        ,source=source
                        ,targets=targets
                        ,URImode=URImode
                        ,header=header
                        ,footer=footer
                        ,author=author
                        ,title=title
                        )
    def _getRe(self): return self._re
    def _getEp(self): return self._ep
    def _setPattern(self, pattern):
        self._showDebug(clas='Transformation',method='_setPattern',note='inputs',line=744,level=0,vars=[['pattern',pattern]])
        if not pattern: self._pattern = self._default_pattern
        elif (isinstance(pattern,list) and
            len(pattern) == 2 and
            pattern[0]):
            self._showDebug(clas='Transformation',method='_setPattern',line=749,level=2,vars=[['pattern',pattern]])
            if (isinstance(pattern[1],basestring) and
                pattern[1].startswith('/') and
                pattern[1].endswith('/')):                                      # if its a regex value
                self._showDebug(clas='Transformation',method='_setPattern',line=753,level=2,vars=[['pattern',pattern]])
                ep = mtutils._splitRegex(pattern[1])                            #  split regex pattern into its parts
                self._showDebug(clas='Transformation',method='_setPattern',line=755,level=2,vars=[['ep',ep]])
                if len(ep) == 2:                                                #  provided 3 parts exist:
                    try:                                                        #   try processing transformation:
                        ec,pc = mtutils._pdepth(ep[0])                          #    count and validate inner parenthesis
                        if ec == 1: raise mterrors.UnbalancedParenthesisError(ep[0])#test error code to raise errors
                        elif ec == 2: raise mterrors.UnspecifiedParenthesisError()
                        pattern[0] = self._prepareVars(spec=pattern[0])         #     get bound variable from part 0
                        r = re.compile(ep[0])                                   #     compile part 1
                        self._showDebug(clas='Transformation',method='_setPattern',line=763,level=2,vars=[['r',r]])
                        if r:
                            self._re = r                                        #      set compiled regex
                            self._ep = ep                                       #      set list of expression parts[1,2]
                            self._pattern = pattern                             #      set Transformation pattern
                            self._showDebug(clas='Transformation',method='_setPattern',line=768,level=2,vars=[['self._re',self._re],['self',self]])
                    except mterrors.MTerror, X:
                        X._notify(c='Transformation',
                                  m='_setPattern()')                            #   notify MTerror
        self._showDebug(clas='Transformation',method='_setPattern',note='returns',line=772,level=0,vars=[['pattern',pattern]])
        return self._pattern
    def _prepareVars(self, spec=None):
        # usage:
        #    extracts list of variables in Sequence bound to query variables
        # note:
        #    variables bound to Content objects are not bound (on purpose)
        self._showDebug(clas='Transformation',method='_prepareVars',note='inputs',line=779,level=0,vars=[['spec',spec]])
        s = self._interpetVar(spec)
        if isinstance(s,Content): spec = s                                      # flip returned binding if a Content variable - ie it might be a copy of a generic one.
        self._showDebug(clas='Transformation',method='_prepareVars',note='returns',line=782,level=0,vars=[['spec',spec]])
        return spec
    def _generate(self, bound=None, instance=None, store=None):
        # usage:
        #    expands nested webs into nested triples for display
        #    called from _getValues
        # inputs
        #    bound     = variable bindings for variable substitutions
        #    instance  = result instance
        #    store     = TripleStore for expanding ids of nested triples
        # note 1:
        #    bound['!unique']    = is this result unique? true(y)|false
        #                          this is the overall result uniqueness
        #                          not the uniqueness of the bindings applying to this Content object
        #    bound['!triples']   = matching triples
        #    bound['!rules']     = matching rules
        #    bound['!equations'] = equations solved
        # note 2:
        #    completeness mode irrelevant as this only processes a single value
        self._showDebug(clas='Transformation',method='_generate',note='inputs',line=801,level=0,vars=[['bound',bound],['instance',instance],['store',store]])
        self._showDebug(clas='Transformation',method='_generate',line=802,level=1,vars=[['self._re',self._re],['self',self]])
        rv = v = None                                                           # default None new value and renderedValue
        if bound['!unique'] or not self._getUnique():                           # proceed only if uniqueness constraint satisfied
            i = self._getPattern()                                              #  get the slot pattern
            self._showDebug(clas='Transformation',method='_generate',line=806,level=1,vars=[['i',i]])
            if i:                                                               #  if pattern ok
                i,ri,bound = self._interpolate(i[0],bound,instance,store)       #   interpolate value and updated bindings
                self._showDebug(clas='Transformation',method='_generate',line=809,level=1,vars=[['i',i],['ri',ri],['self._re',self._re],['self._ep',self._ep]])
                dummy,v = mtutils._evalRegex(ri,self._getRe(),self._getEp())    #   perform the transform on the interpolation
                self._showDebug(clas='Transformation',method='_generate',line=811,level=1,vars=[['v',v],['dummy',dummy],['self._getDoRender()',self._getDoRender()],['self._getRender()',self._getRender()]])
#                if self._getDoRender():                                         #   if rendering required:
#                    rv = self._getRender()._translate(v,                        #    set rendered value to rendered result
#                                                      endline='no')
#                else: rv = v                                                    #   else render value is value
                if (self._getDoRender() and
                    isinstance(store,mtstruct.A_TripleStore)):              #  if rendering required:
                    rv = self._getRender()._translate(store._expandTriple(v,expandRules=True,uri=self._getURImode())
                                                     ,endline='no')         #   set rendered value to rendered result
                else: rv = v                                                #  else render value is value
                self._showDebug(clas='Transformation',method='_generate',line=821,level=1,vars=[['v',v],['rv',rv]])
        v = self._deliver(v,rv,instance,store)                                  # deliver generations to targets
        self._showDebug(clas='Transformation',method='_generate',line=823,level=0,vars=[['rv',rv],['bound',bound]])
        return v,rv,bound                                                       # return new rendered value (or None if failed) and updated bindings

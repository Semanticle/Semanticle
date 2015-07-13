'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

Created on 28 Nov 2009
structured02.py cloned from structured01.py on 30 Mar 2010
structured03.py cloned from structured02.py on 19 Apr 2010
structured04.py cloned from structured03.py on 01 May 2010
structured05.py cloned from structured04.py on 12 May 2010
structured06.py cloned from structured05.py on 12 Jun 2010
structured.py cloned from structured06.py on 07 Jul 2010
Last Updated on 22 Oct 2010

Abstract storage classes from which the concerte version in storesnn.py inherit.
To support existence verification without circular imports.

30/03/2010 structured02.py cloned from structured01.py with:
    - hierarchy change to reflect stores47.py distrubuted stores refactoring:
       - TripleStore < SimpleTripleStore < DistSimpleTripleStore

19/04/2010 structured03.py cloned from structured02.py with:
    - Persistent Triple Stores supported

01/05/2010 structured04.py cloned from structured03.py with URI support implemented:
    - _parseURI() and _setURImaps() moved here from mtstores so these methods may be exploited by mtquery to prepare query value expressions
    - _parseURI() inputs mode to interpret based on one or both of:
        - base URI - at stores instantiation or stores query execution time
        - preferred predicate labels - at stores instantiation or query instantiation time

10/05/2010 URI methods finalised:
    - _setBSNSmap(), _getBSfromNS(), _getNSfromBS and _setURImaps() sub-method of _parseURI() defined
    - _parseURI() support for 'has_unifyuri' generation dropped - not needed

11/05/2010 support for various URI render formats:
    - _parseURI() now tests base == base OR base == URIsystembase to detect system constructs
    - _regex for URI splitting nor supports base#fragement pairs where the fragment itself may be a base (as possible with rdf exports of URI or namespace models)

12/05/2010 variable handling in URIs:
    - URI parse regex minor update - fragment query variables can no longer have middle spaces

12/05/2010 structured05.py cloned from structured04.py with:
    - explicit alias_ontology support

13/05/2010:
    - _parseURI._setURImaps() unused indexes removed:
        _uri_sl_pv superceded by the alias_ontology singleton (mtalonto)
        _uri_bv_sl algorithmically avoided
    - _parseURI() supports rdf generation of base uri values for equivalent labels

05/06/2010:
    - _purseURI() bug fix: has_displayuri outputs preferred terms from alias_ontology01.dat

12/06/2010 structured06.py cloned from structured05.py with:
    - folders re-configured

07/07/2010 structured.py cloned from structured06.py for SVN versioning

12/07/2010 settings support interpetation of config variables

29/07/2010 _splitURI() bug fix: handles uri attribute errors for nested sub graph strings

12/10/2010 Stage 0. Mixed Triple ordering support. Any single order support
    - ensure system triples are generated in same order as user supplied triples.
    - _rt() defined and exploited:
        - reorders the elements within system generated and queried triples to match that of user supplied triples
        - specifically needed for cross querying of modelled URI data with user supplied data
        - exploited by _setBSNSmap()
        - store specific ordering overides system default if tripleOrder paramter is set. Applies to TripleStore and DistTripleStore.
    - All values tested for validity in the following order:
       - store specific value.
       - user preference (system wide).
       - hardcoded default (not tested).

19/10/2010 A_TripleStore._rt() enhanced:
    - support bi-directional re-ordering where self is either the source or the target
    - actually as it happens this was not needed - but enhancement left in case it is useful later

20/10/2010 Compliance with mtstores refactoring

22/10/2010: Stage 5:  Mixed triple ordering support: Optional re-ordering for IO:
    - _default_ioTripleOrder setting
    - _get/_setIoTripleOrder()

@author: Administrator
'''

import csv, re, copy
import metabulate.utils.utils           as mtutils
import metabulate.utils.errors          as mterrors
import metabulate.singletons.singleton  as mtsingleton

mtconfig = mtsingleton.Settings()._getItem('config')
mtprefs  = mtsingleton.Settings()._getItem('prefs')
mtalonto = mtsingleton.Settings()._getItem('alias_ontology')
#reuri = re.compile('^(?=[^&])(?:([^:/?#]+):)?(?://([^/?#]*))?(?:/[\w]([^/?#]*))?(?:/?\?([^#]*))?(?:(?:#(.*))|(^.*))?')
#reuri = re.compile('^(?=[^&])(?:([^:/?#]+):)?(?://([^?/#]*))?(?:/[^/#]*)*(?:\?([^#]*))?(?:(?:#(.*))|(^[a-zA-Z0-9][a-zA-Z0-9_ ]*[a-zA-Z0-9](#.*)?))?')
#1) reuri comment ... commplete match required, gr0=fullmatch, gr1=protocol, gr2=authority, gr3=path, gr4=query (on or more expressions), gr5=(fragment (id,or string), or value (id, word, namespace#word))
#reuri = re.compile('^(?=[^&])(?:([a-z]+):)?(?://([a-zA-Z0-9\-\.]*))?(?:/([a-zA-Z0-9\-\_\./]*))*(?:(\?[a-zA-Z0-9\-\_]=[a-zA-Z0-9\-\_\%](?:\&[a-zA-Z0-9\-\_]=[a-zA-Z0-9\-\_\%])*))?(?:(?:(?:\#((?:\#\#\d+)|(?:[^#]*)))|((?:\#\#\d+)|(?:\?(?:[a-zA-Z0-9][a-zA-Z0-9_ ]*[a-zA-Z0-9])?)|(?:\*)|(?:[a-zA-Z0-9][a-zA-Z0-9_ ]*[a-zA-Z0-9](?:\#.*)?))))?$')
#2) reuri comment ... same as (1) but fixes namespace#fragment to return in group 5 (same as fragment for a base) not group 6
#reuri = re.compile('^(?=[^&])(?:([a-z]+):)?(?://([a-zA-Z0-9\-\.]*))?(?:/([a-zA-Z0-9\-\_\./]*))*(?:(\?[a-zA-Z0-9\-\_]=[a-zA-Z0-9\-\_\%](?:\&[a-zA-Z0-9\-\_]=[a-zA-Z0-9\-\_\%])*))?(?:\#?((?:\#\#\d+)|(?:\?(?:[a-zA-Z0-9][a-zA-Z0-9_ ]*[a-zA-Z0-9])?)|(?:\*)|(?:[a-zA-Z0-9][a-zA-Z0-9_ ]*[a-zA-Z0-9](?:\#.*)?)))?$')
#3) reuri comment ... same as (2) but fixes base#fragment such that the fragment can be a uri base (such as may occur in an rdf representation of the uri or namespace models
#reuri = re.compile('^(?=[^&])(?:([a-z]+):)?(?://([a-zA-Z0-9\-\.]*))?(?:/([a-zA-Z0-9\-\_\./]*))*(?:(\?[a-zA-Z0-9\-\_]=[a-zA-Z0-9\-\_\%](?:\&[a-zA-Z0-9\-\_]=[a-zA-Z0-9\-\_\%])*))?(?:\#?((?:\#\#\d+)|(?:\?(?:[a-zA-Z0-9][a-zA-Z0-9_ ]*[a-zA-Z0-9])?)|(?:\*)|(?:[a-zA-Z0-9][a-zA-Z0-9_\/\:\.\?\&\=\%\- ]*[a-zA-Z0-9\/](?:\#.*)?)))?$')
#4) reuri comment ... same as (3) but variable name fragments cannot have a middle space
reuri = re.compile('^(?=[^&])(?:([a-z]+):)?(?://([a-zA-Z0-9\-\.]*))?(?:/([a-zA-Z0-9\-\_\./]*))*(?:(\?[a-zA-Z0-9\-\_]=[a-zA-Z0-9\-\_\%](?:\&[a-zA-Z0-9\-\_]=[a-zA-Z0-9\-\_\%])*))?(?:\#?((?:\#\#\d+)|(?:\?(?:[a-zA-Z0-9][a-zA-Z0-9_ ]*[a-zA-Z0-9])?)|(?:\*)|(?:[a-zA-Z0-9][a-zA-Z0-9_\/\:\.\?\&\=\%\- ]*[a-zA-Z0-9\/](?:\#.*)?)))?$')
reaut = re.compile('^([a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$')
rebse = re.compile('^ *(.*?)#')     # non-greedy uri base match

class StructuredStore: pass
class A_RelationalStore(StructuredStore): pass
class A_TripleStore(StructuredStore):
    # non updatable values for use if URIs are modelled
    _URIsystembase         = 'http://www.semanticle.org/'
    _sURIpreds             = ['has_uriprotocol','has_uriauthority','has_uripath','has_uriquery','has_urifragment','has_uribase']
    _URIpredsModelled      = mtutils._stripsplit(mtprefs._interpretItem('URIpredicatesModelled','has_uri_protocol,has_uri_authority,has_uri_path,has_uri_query,has_uri_fragment,has_uri_base'))
    _default_tripleOrder   = mtutils._stripsplit(mtprefs._interpretItem('tripleOrder','s,p,o'))
    _default_ioTripleOrder = mtutils._stripsplit(mtprefs._interpretItem('iotripleOrder','')) # default is null - interpretted as tripleOrder

    def _setBSNSmap(self):
        # usage:
        #    try to create the maps between namespaces and URI bases by querying the triple store has_urins relationships
        # Note:
        #    invoked just in time by _getBSfromNS() or _getNSfromBS() methods if the maps haven't yet been defined
        #    maps only get defined if triple store can be queried (whether or not this yields matching data)
        #    if store cannot be queried, maps remain undefined so later attempts may still be triggered
        def _initDicts():
            self._uri_ns_bs = mtutils.sdict()                                   # initialise namespace to URI base dict
            self._uri_bs_ns = mtutils.sdict()                                   # initialise URI base to namespace dict
        noMaps = True                                                           # assume noMaps have been defined
        try:                                                                    # try: (querying triple store to instantiate the map)
            for r in self._bindings([self._rt(('?b','has_urins','?n'))]):       #  query URI base namespace pairs
                if noMaps: _initDicts(); noMaps = False                         #   query yields results but no maps: so define them
                b1 = r['b']                                                     #   get a base and
                n1 = r['n']                                                     #   and namespace pair
                if b1 not in self._uri_bs_ns: self._uri_bs_ns[b1] = n1          #   if namespace not indexed by this URI base: do so
                if n1 not in self._uri_ns_bs: self._uri_ns_bs[n1] = b1          #   if URI base not indexed by this namespace: do so
            if noMaps: _initDicts(); noMaps = False                             #  no maps and no data but query not rejected: so define empty maps
        except: pass                                                            # could not initialise the indexes: so pass
    def _getBSfromNS(self,ns):
        # usage:
        #    get URI base from a Namespace
        #    attempts to access the namespace to Base map
        #    if its not yet defined it invokes _setBSNSmap() to attempt to create it
        # inputs:
        #    ns - candidate namespace
        # returns:
        #    bs - URI base of the namespace (if any) - if not returns None
        try: l = len(self._uri_ns_bs)                                           # try something using the map
        except AttributeError: self._setBSNSmap()                               # except no such map: try creating it (if maps exist but empty ignore)
        bs = None                                                               # by default there is no matching base
        try:                                                                    # try: (getting tha base via the relevant map)
            if ns in self._uri_ns_bs: bs = self._uri_ns_bs[ns]                  #  if namespace in the map: get the matching base
        except AttributeError: pass                                             # except still no map: ignore
        return bs                                                               # return the matching base (or None)
    def _getNSfromBS(self,bs):
        # usage:
        #    get Namespace from a URI base
        #    attempts to access the URI Base to Namespace
        #    if its not yet defined it invokes _setBSNSmap() to attempt to create it
        # inputs:
        #    bs - candidate URI base
        # returns:
        #    ns - namespace denoting the URI base (if any) - if not returns None
        try: l = len(self._uri_bs_ns)                                           # try something using the map
        except AttributeError: self._setBSNSmap()                               # except no such map: try creating it (if maps exist but empty ignore)
        ns = None                                                               # by default there is no matching namespace
        try:                                                                    # try: (getting tha namespace via the relevant map)
            if bs in self._uri_bs_ns:
                ns = self._uri_bs_ns[bs]                  #  if base in the map: get the matching namespace
        except AttributeError: pass                                             # except still no map: ignore
        return ns                                                               # return the matching namespace (or None)
    def _parseURI(self,target,uri,mode=['query']):
        # usage:
        #
        #    for storage: defining modelled URI data
        #    also now for query and delivery: replacing _expressURI()
        #
        #    validates and extracts data from a URI
        #    if URI matches current base+basesuffix then component labels are substituted for values
        # inputs:
        #    self   - the source store
        #    target - the target store
        #    uri    - the uri
        #    mode   - how to interpret the URI any one or more of [query|parts] as string or list of strings:
        #             - null  - set to 'off'
        #             - off   - treat as if URIsupport is off (if combined with other modes these will be dropped as they are meaningless)
        #             - query - get URI bits needed for query processing or results delivery (automatically also sets parts & preferred modes)
        #                       returns: has_nativeuri, fulluri, base, fragment and if supplied has_urifragment, has_uribase
        #                       where:
        #                        - has_nativeuri      (runtime)  - indexed uri value
        #                        - has_rdfuri         (runtime)  - uri for export (system labels prefixed with system base)
        #                        - has_uribase        (modelled) - uribase (how the uribase is labelled)
        #                        - has_properuribase  (runtime)  - literal uri base (what it is not how it is labelled)
        #                        - has_urifragment    (modelled) - stored uri fragment (either a value or system label)
        #             - parts - interpret modelled URI parts (otherwise just process the URI)
        #                        (if URIsupport is off an empty dict is returned
        #                        - has_uriprotocol    (modelled) - base protocol (typically http)
        #                        - has_uriauthority   (modelled) - base domain (e.g. www.semanticle.com)
        #                        - has_uripath        (modelled) - base domain path suffix (file path in unix notation)
        #                        - has_uriquery       (modelled) - base query (http GET parameters for a dynamic page)
        # returns:
        #    d     - dict of available (not None) result values indexed by their identifying system predicate labels
        #            ie. {uri_bit_system_predicate1:uri_bit_value1,..,uri_bit_system_predicateN:uri_bit_valueN}
        # Note: Also ensures initialisation of the 2 uri mapping indexes.
        #    - self._uri_sl_bv (for result element conversion) indexes URI part base values by their corresponding system labels
        #    - self._uri_pv_sl (for query elememt conversion)  indexes URI part system labels by their corresponding preferred values
        # Explanation:
        #    uri maps shouldn't persist since underlying uri preferences may change
        #    and if they do, updating the maps won't impact the integrity of existing data
        #    since all persistent data is essentially independent of uri preference settings.
        # validate the mode
        def _setURImaps():
            self._uri_sl_bv = mtutils.sdict()                                   #  baselabel:basevalue map
            self._uri_pv_sl = mtutils.sdict()                                   #  preferredvalue:systemlabel map
            for c,slp in enumerate(self._sURIpreds):
                sln = 'native_'+slp[4:]
                if base is not None:                                            #   map between base uri parts and system labels
                    try:
                        v = reuri.match(self._getURIbase()).group(c+1)
                        if v is not None:
                            v = v.strip()
                            if v: self._uri_sl_bv[sln] = v                      #    map uri base label:value
                    except: pass
            for sl,pv in mtalonto.items(): self._uri_pv_sl[pv] = sl       #  also map preferred to system ontology term
            for sl,pv in mtalonto.items():                                #  also be sure to index the system ontology terms in the preferred map
                if sl not in self._uri_pv_sl: self._uri_pv_sl[sl] = sl          #   if not already indexed: include system terms in the preferred map
        # END _setURImaps()
        if not mode: mode = ['off']                                             # null mode means mode = ['off']
        elif isinstance(mode,basestring): mode = [mode]                         # ensure mode is a list
        if 'off' not in mode:                                                   # if uri support is not off:
            try: supp = self._getURIsupport()                                   #  try getting URIsupport
            except: supp = 'off'                                                #  except default to 'off'
            if supp == 'off':
                if 'parts' in mode: return {}
                else: mode = ['off']
        else: mode = ['off']
        # get uri bases(s)
        try: base = self._getURIbase()                                          # try: getting the full uri base for the source store
        except AttributeError: base = None                                      # except: its None
        if target == self: tbase = base                                         # and use as target base if the same
        else:                                                                   # else: (get target base seperately)
            try: tbase = target._getURIbase()                                   #  try: getting the full uri base for the target store
            except: tbase = None                                                #  except: its None
        setmaps = False                                                         # assume map indexes exist
        # check uri maps
        try:                                                                    # try:
            if not self._uri_pv_sl: setmaps = True                              #  if map index empty: flag to set it
        except AttributeError: setmaps = True                                   # except no map index: also flag to set it
        if setmaps: _setURImaps()                                               # if map indexes not already set: (proceed to do so)
        # proceed to split the uri
        d = mtutils.sdict()                                                     # initialise results dict
        parts_done = False                                                      # parts not parsed
        is_label = False                                                        # assume fragment isn't a system label
        ns = f = b = bl = None                                                  # default fragment, base and base label are None
        if 'off' not in mode:                                                   # but if URIsupport not off:
            r = self._splitURI(uri)                                             #  is it a URI which can be split into base and fragment?
            if r is not None: b = bl = r[0]; f = r[1]                           #  if URI could be split: set base and fragment
            if f is None:                                                       #  if no valid fragment:authority pair found: (check if pairing with ns)
                try:                                                            #   try
                    ns = rebse.match(uri).group(1)                              #    parsing the namespace
                    if ns:                                                      #    parse hasn't failed so if namespace not null:
                        bs = self._getBSfromNS(ns)                              #     get base from namespace (if avail)
                        if bs is not None:                                      #     if base was available for the namespace:
                            b = b1 = bs                                         #      set it as base and base label
                            f = uri[len(ns)+1:]                                 #      also set the fragment
                except: pass                                                    #   except: keep defaults
        if f is None: f = uri                                                   # still no fragment: default to the uri
        if f:                                                                   # if fragment not null:
            if 'off' in mode or f[0] == '?':                                    #  if URI support is off or fragment is a query variable:
                d['has_nativeuri'] = f                                          #   set the native URI value to the fragment value
                d['has_rdfuri'] = f                                             #   set the export URI value to the fragment value
                d['has_displayuri'] = f                                         #   set the (native) display URI to the fragment value
                is_label = True                                                 #   flag labelled
            else:                                                               #  else fragment is a data value needing URI support:
                fp = mtalonto._getItem(f,f)                                     #    get the preferred value for the fragment (if any)
                if f in self._uri_pv_sl:                                        #   if fragment is a preferred label: (remember these also reverse indexed)
                    d['has_displayuri'] = fp                                    #    set the (native) display URI to the preferred fragment value
                    f = self._uri_pv_sl[f]                                      #    reset fragment to its corresponding system label
                    d['has_nativeuri'] = f                                      #    set the native URI value to the reset fragment value
                    is_label = True                                             #    flag labelled
                elif f[:2] == '##' and int(f[2:]) > 0:                          #   elif fragment is a validated internal triple id:
                    d['has_nativeuri'] = f                                      #    set the native URI value to the fragment value
                    d['has_displayuri'] = f                                     #    set the (native) display URI to the fragment value
                    is_label = True                                             #    flag labelled
                else:                                                           #   else fragment is neither a preferred label nor an internal triple id:
                    if b is None: bl = b = base                                 #    so if uri base ommitted assume its the source base
                    if b is not None:                                           #    if base exists:
                        if b == tbase or b == self._URIsystembase:              #     and its that of the target or the software:
                            d['has_nativeuri'] = f                              #      set the native URI value to the fragment value
                            d['has_displayuri'] = fp                            #      set the (native) display URI to the preferred fragment value
                            bl = 'uribase'                                      #      set URI base value to its system label
                            parts_done = True                                   #      flag component extraction done
                            if 'parts' in mode:                                 #      if remaining URI parts required:
                                for c in range(4):                              #       for each URI bit (except uri and base):
                                    pred = self._sURIpreds[c]                   #        get the predicate for this bit
                                    noun = 'native_'+pred[4:]                   #        derive the noun linked to the predicate
                                    if noun in self._uri_sl_bv:                 #        if corresponding fullbase bit value is not None:
                                        d[pred] = noun                          #         set uri system noun indexed by uri system pred
                        else:                                                   #     else base not of the target:
                            d['has_nativeuri'] = b+'#'+f                        #      so include it in has_nativeuri
                            if ns is None:                                      #      if ns is None:
                                try: ns = target._getNSfromBS(b)                #       try: to get it from URI base (if avail)
                                except: pass                                    #       except: leave as None
                            if ns is None: ns = b                               #      if ns is still None: use the base
                            d['has_displayuri'] = ns+'#'+fp                     #      form the displayuri from the namespace, seperator and pref fragment
            d['has_urifragment'] = f                                            #  set the URI fragment value
        if 'has_nativeuri' not in d: d['has_nativeuri'] = uri                   # catch_all default has_nativeuri instantiation
        if 'has_displayuri' not in d: d['has_displayuri'] = uri                 # catch_all default has_displayuri instantiation
        if bl is not None: d['has_uribase'] = bl                                # set the URI base label value
        # parse query values (if needed)
        if 'query' in mode:                                                     # if parsing for query:
            if f in self._uri_sl_bv: f = self._uri_sl_bv[f]                     #  if fragment a system label for base value: switch it to base value
            if is_label:                                                        #  if fragment is a system label:
                 if 'has_rdfuri' not in d:                                      #   if rdfuri not set:
                     d['has_rdfuri'] = self._URIsystembase+'#'+f                #    set rdfuri to the URI systembase + seperator + fragment value
            else:                                                               #  else its a value not a label: (so unification & rfd uri are equal)
                quri = uri                                                      #   use supplied uri as a default queryable uri
                if b is not None:                                               #   if base exists:
                    d['has_uribase'] = b                                        #    set it as the queryable base
                    if f: quri = b+'#'+f                                        #    and prefix to the fragment (if this exists) as the queryable uri
                d['has_rdfuri'] = quri                                          #   set has_rdfuri to the queryable uri
        # parse part value (if needed and not already done)
        if 'parts' in mode:                                                     # if parts mode:
            if 'has_uribase' in d and not parts_done:                           #  if uribase exists and parts not done: (proceed)
                for c in range(4):                                              #   for parts except has_uribase and has_urifragment:
                    p = reuri.match(uri).group(c+1)                             #    get the bit value
                    if p is not None:
                        p = p.strip()
                        if p: d[self._sURIpreds[c]] = p                         #    only if bit value exists instantiate it in results dict
            for p in d:                                                         #  check each parts mode predicate in results:
                if p not in self._URIpredsModelled: del d[p]                    #   if its not required for the model: delete it
        return d                                                                # return results dict
    def _splitURI(self,uri,errors=False):
        # usage:
        #    splits a uri into its base and fragment
        #    only if base is a valid url
        r = b = None                                                            # initialise result and base to None
        try:                                                                    # try:
            f = reuri.match(uri).group(5)                                           # parse the fragment from the uri
            if f is not None:                                                   #  if fragment found:
                a = reuri.match(uri).group(2)                                   #   parse the authority:
                if a:                                                           #   if authority exists: (try checking it)
                    try:                                                        #    try:
                        a = reaut.match(a).group(0)                             #     check authority is a valid domain
                        b = uri[:-len(f)-1]                                     #     check ok derive the base and base label
                        r = [b,f]                                               #     set the fragment
                    except: raise mterrors.URIauthorityError(a,uri)             #    except: raise a URIauthorityERror
            else: raise mterrors.URIparseError(uri)                             #  authority non-existant: raise a URIparseError
        except mterrors.URIerror, X:                                            # except uri errors:
            if errors: X._notify(c='A_TripleStore',m='_splitURI()')             #  if (notify) errors: notify it
        except AttributeError: pass                                             # except unparsable uri: this will be a subgraph so ignore
        return r                                                                # return r (either None or the validated [base,fragment] pair)

    def _expressURI(self,anyval):
        #
        # no longer used, but temporarilly retained for reference - ie. transformations needed for query
        #
        # usage:
        #
        #    for application: querying and delivering URI data
        #
        #    required for Query evaluation to ensure values can be matched across distributed stores.
        #    inputs a triple element value in full or native storage formats
        #    returns its fragment, base (implicit or explicit), native value and full value
        # Note:
        #    this method could be defined in mtstores - but defined here instead to keep together with other URI related methods
        # inputs:
        #    val  - stored element value (rem: fragment only is base is native)
        # returns:
        #    frag        - fragment value
        #    base        - base value
        #    native_val  - native storage value
        #    full_val    - full storage value (URI except for system predicates)
        native_val = val
        full_val = val
        try: thisbase = self._getURIbase()
        except: thisbase = ''
        try:
            base = rebse.match(val).group(1)
            frag = val[len(base)+1:]
            if base == thisbase: native_val = frag
        except:
            frag = val
            if thisbase:
                full_val = thisbase+'#'+frag
                base = thisbase
            else: base = ''
        return frag,base,native_val,full_val
    def _rt(self,t,order=None,toself=True):
        # usage:
        #    supports bi-directional re-ording of triple t:
        #     - from order to self (if toself is True)
        #     - to order from self (if toself is False)
        # inputs:
        #    t      - triple to be re-ordered
        #    order  - source or target order of t (if None default s,p,o ordering is assumed)
        #    toself - direction of re-ordering:
        #              - True:  from order to that of self
        #              - False: to order from that of self
        # returns:
        #    r     - reordered triple
        o = self._getTripleOrder()
        if not self._testTorder(order): order = ['s','p','o']
        if order == o: return t
        if toself: stoi = self._getStoi()
        else:
            stoi = {}
            for c,v in enumerate(order): stoi[v] = c
            order = o
        r = mtutils.slist()
        for c,i in enumerate(order): r[stoi[i]] = t[c]
        if isinstance(t,tuple): r = tuple(r)
        return r
    def _testTorder(self,order):
        # usage:
        #    tests if order is a valid triple order
        # inputs:
        #    order - triple ordering to test
        # returns:
        #    order valid [True|False]
        default = mtutils.slist(['s','p','o'])
        if (isinstance(order,list)
        and len(order) == 3
        and len(default._symmetric_distance(order)) == 0
            ): return True
        else: return False
    def _setTripleOrder(self,order=None):
        # usage:
        #    sets self._db['tripleOrder'] from the following in order of preference:
        #     1. order, if valid or
        #     2. self._default_tripleOrder (based on pref.dat setting), if valid or
        #     3. system default
        # inputs:
        #    order - triple order supplied
        # returns:
        #    o     - triple ordering finally set
        if self._testTorder(order): o = order
        else:
            if not self._testTorder(self._default_tripleOrder):
                self._default_tripleOrder = ['s','p','o']
            o = self._default_tripleOrder
        self._db['tripleOrder'] = o
        return o
    def _getTripleOrder(self):
        # usage:
        #    gets stored triple ordering for self
        #    if not set sets it from a valid default
        # returns:
        #    o - triple ordering of self
        if 'tripleOrder' not in self._db:
            o = self._setTripleOrder()
        else: o = self._db['tripleOrder']
        return o
    def _setIoTripleOrder(self,order=None):
        # usage:
        #    sets self._db['tripleOrder'] from the following in order of preference:
        #     1. order, if valid or
        #     2. self._default_tripleOrder (based on pref.dat setting), if valid or
        #     3. system default
        # inputs:
        #    order - triple order supplied
        # returns:
        #    o     - triple ordering finally set
        if self._testTorder(order): o = order
        else:
            o = self._default_ioTripleOrder
            if not self._testTorder(o): o = None
        self._db['ioTripleOrder'] = o
        return o
    def _getIoTripleOrder(self):
        # usage:
        #    gets stored triple ordering for self
        #    if not set sets it from a valid default
        # returns:
        #    o - triple ordering of self
        if 'ioTripleOrder' not in self._db:
            o = self._setIoTripleOrder()
        else: o = self._db['ioTripleOrder']
        return o
    def _getStoi(self):
        # usage:
        #    gets the stored triple ordering index of self
        #    from cache if available
        #    else derives it from self._getTripleOrder() caching result
        # returns:
        #    toi - dict of triple ordering by element id {elem0_id:order0,elem1_id:order1,elem2_id:order2}
        try: return self._stoi
        except AttributeError:
            stoi = mtutils.sdict()
            for c,i in enumerate(self._getTripleOrder()): stoi[i] = c
            self._stoi = stoi
            return stoi
class A_DistTripleStore(A_TripleStore): pass

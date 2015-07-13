'''
Copyright 2009, 2010 Anthony John Machin. All rights reserved.
Supplied subject to The GNU General Public License v3.0

Created on 12 Jul 2010

12/07/2010 spawned from dubug.py
    - to seperate Debug activation/de-activation from exploitation
    - thereby eliminate circular imports with utils and singleton

@author: Administrator
'''
from utils import Flatfile
import fileinput
import re
import os.path
from metabulate.singletons.singleton import Settings
mtconfig = Settings()._getItem('config')

class Debugger(object):
    def __init__(self
                ,sources=''                                          # file listing source files for debug output re-numbering
                 ):
        self._default_sources = Flatfile(path=mtconfig._interpretItem('debuglist_path','%configfilesbase%Config\\')
                                        ,name=mtconfig._interpretItem('debuglist_name','DebugList')
                                        ,type=mtconfig._interpretItem('debuglist_type','dat')
                                         )
        self._update(sources=sources)
    def _update(self, criteria=None, sources=None):
        if sources  is not None: self._setSources(sources)
    def _setSources(self,file):
        if not file: self._sources = self._default_sources
        elif isinstance(file,Flatfile): self._sources = file
        return self._sources
    def _getSources(self): return self._sources
    def _processSources(self,action=['activate','renumber'],sources=None,report=None):
        # usage:
        #    utility to automatically renumber _showDebug() line= parameters for
        #    all sources listed in a data file.
        #    source files affected are automatically loaded, relevant statements updated and resaved
        # inputs:
        #    action  = renumber|activate|deactivate
        #    sources = Flatfile of sources data file
        #    report  = yes to see reported actions taken
        def processSource(fn,action,regex):
            # usage:
            #    renumber _showDebug line= statements in a single file known to exist
            #    retreive file, check numbering, update if needed, and re-save altered files
            # input:
            #    fn    = full filename of existing file
            #    regex = compiled regex object for matching line numbers in _showDebug() statements
            # output:
            #    number of debug statements with changed line= parameter settings
            s = ''
            n = 0
            ren = act = dct = 0
            f = open(fn,"r")
            for line in f:
                n += 1
                try:
                    m = regex.findall(line)
                    if m:
                        if ('renumber' in action
                        and int(m[0][1]) != n):                         # if _showDebug() and wrong line= value:
                            line = m[0][0]+str(n)+m[0][2]+'\n'          #  update line with correct line= value
                            ren += 1
                        if (line.startswith('#')
                          and 'activate' in action):
                            line = line[1:]
                            act += 1
                        elif (not line.startswith('#')
                          and 'deactivate' in action):
                            line = '#'+line
                            dct += 1
                except: pass
                s += line                                               # add line to full file string
            f.close()
            if ren+act+dct:                                             # if updates made:
                f = open(fn,'w')                                        #  save these
                f.write(s)
                f.close()
            return [ren,act,dct]
        c = 0
        self._update(sources=sources)
        f = self._getSources()
        if action and isinstance(f,Flatfile):
            acts = []
            for act in action:
                if isinstance(act,basestring): acts += [act.lower()]
            fn = f._getFullname(existing='y')
            if fn:
                regex = re.compile('^(\#?\s*self\.\_showDebug\(.*?line\s*=\s*)(\d+)(.*\).*)$')
                n = 0
                for line in self._getSources()._getValues():
                    line = mtconfig._doSubs(line)
                    if os.path.exists(line):
                        n += 1
                        results = processSource(line,acts,regex)
                        resstr = ''
                        actstr = ['renumbered','activated','deactivated']
                        infix = ' debug lines'
                        for c1,result in enumerate(results):
                            if result:
                                resstr += str(result)+infix+' '+actstr[c1]+', '
                                if infix: infix = ''
                        if resstr:
                            c += 1
                            if report: print ('Processed: '+line+' ('+resstr[:-2]+')')
                if report: print (str(c)+' sources renumbered from '+fn)
        return c

if __name__ == "__main__":
    d = Debugger()
    d._processSources(action=['activate','renumber'],report='y')
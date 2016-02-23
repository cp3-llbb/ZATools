#!/nfs/soft/python/python-2.7.5-sl6_amd64_gcc44/bin/python
import os, sys

# Add default ingrid storm package
sys.path.append('/nfs/soft/python/python-2.7.5-sl6_amd64_gcc44/lib/python2.7/site-packages/storm-0.20-py2.7-linux-x86_64.egg')
sys.path.append('/nfs/soft/python/python-2.7.5-sl6_amd64_gcc44/lib/python2.7/site-packages/MySQL_python-1.2.3-py2.7-linux-x86_64.egg')

CMSSW_BASE = os.environ['CMSSW_BASE']
SCRAM_ARCH = os.environ['SCRAM_ARCH']
sys.path.append(os.path.join(CMSSW_BASE,'bin', SCRAM_ARCH))

from SAMADhi import Dataset, Sample, DbStore

class Process:
    def __init__(self, name):
        self.name = name
        self.type = 0
        self.file = ''
        self.xsection = 1.
        self.sumW = 1.
        self.channels = {}

    def __str__(self):
        result = "Process:\n"
        result += "\tname= %s\n" % self.name
        result += "\ttype= %i\n" % self.type
        result += "\tfile= %s\n" % self.file
        result += "\txsection= %.4g\n" % self.xsection
        result += "\tsumW= %.4g\n" % self.sumW
        result += "\tchannels (%i total):\n" % len(self.channels)
        for c in self.channels:
            result += "\t\t%s: %.4g\n" % (c, self.channels[c])
        return result

    def get_sample(self, name, tag):
        dbstore = DbStore()
        resultset = dbstore.find(Sample, Sample.name.like(unicode(name + "%_" + tag)))
        return resultset.one()

    def prepare_process(self, path, shortname, name, tag):
        #sample = self.get_sample(name, tag)
        self.name = shortname
        if 'ZZ' in name:
            self.type = -1
        elif 'TTTo2L2Nu' in name:
            self.type = 1
        elif 'DY' in name:
            self.type = 2
        if 'data_obs' in shortname:
            self.type = 0
        print name + "_" + tag + "_histos.root"
        
        self.file = os.path.join(path, name + "_" + tag + "_histos.root")
        print self.file
        os.path.isfile(self.file)
        print self.file
        self.xsection = 1 #sample.source_dataset.xsection
        self.sumW = 1 #sample.event_weight_sum
        self.channels = {}
        
        return self




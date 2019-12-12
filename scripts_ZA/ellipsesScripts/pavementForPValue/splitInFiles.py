import json
import numpy as np

with open("pavementForPValue_0p3_0p3.json") as f:
    parameters = json.load(f)

k=0
for i, line in enumerate(parameters):
    infile=[]
    if i%30==0:
        #print i
        imin = i-30
        imax = i
        if imin < 0:
            continue
        print k
        #print "imin: ", imin
        #print "imax: ", imax
        for j in np.arange(imin,imax):
            infile.append(parameters[j])
            print parameters[j]
        #print "--------"
        with open("pavementForPValue_MuMu_part{0}.json".format(k), "w") as fout:
            json.dump(infile, fout)
            fout.close()
        with open("pavementForPValue_ElEl_part{0}.json".format(k), "w") as fout:
            json.dump(infile, fout)
            fout.close()
        k = k+1
    if i==len(parameters)-1 and i-30!=imax:
        k = k+1
        print k
        imin=imax
        imax=len(parameters)
        #print "LAST CHUNCK"
        for j in np.arange(imin,imax):
            print parameters[j]
            infile.append(parameters[j])
        with open("pavementForPValue_MuMu_part{0}.json".format(k), "w") as fout:
            json.dump(infile, fout)
            fout.close()
        with open("pavementForPValue_ElEl_part{0}.json".format(k), "w") as fout:
            json.dump(infile, fout)
            fout.close()

#! /bin/env python

import sys, os, json
import getopt
import copy
import datetime
import subprocess
import numpy as np
import glob
import math
import scipy as sp
from scipy import ndimage
#import seaborn as sns
import pandas as pd
#import matplotlib
import matplotlib as ml
ml.use('Agg')
from matplotlib import rc
from matplotlib import text
from matplotlib import gridspec
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.font_manager as font_manager

#import pygame
#pygame.font.init()

sys.path.insert(0, '/home/ucl/cp3/asaggio/scratch/CMSSW_8_0_30/src/cp3_llbb/ZATools/scripts_ZA')

import argparse
from math import sqrt,atan,cos


def main():

    plt.rc('text', usetex=True)
    #plt.rc('font', family='serif')
    #ml.rcParams['text.usetex'] = True
    plt.rc('mathtext', default='regular')
    #ml.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}",r"\usepackage{sfmath}",r"\usepackage{slashed}"]

    categories = ['MuMu', 'ElEl']
    for cat in categories:
        print cat
        df = pd.read_csv('../ellipsesScripts/ellParam_{0}.csv'.format(cat), header=None)
        df.columns = ['MA', 'MH', 'a', 'b', 'theta']
        fig = plt.figure(figsize=(20,20))

        #ml.rcParams['image.cmap'] = 'gist_heat'
        gs = gridspec.GridSpec(2, 2, width_ratios=[4.5,1], height_ratios=[1,4.5])
        gs.update(wspace=0.0, hspace=0.0)
        ax0 = plt.subplot(gs[1,0])

        i=0
        plt.plot(df.loc[:,'MA'], df.loc[:,'MH'], "-o", linestyle='None')
        plt.xlim(0, 800)
        plt.ylim(150, 1100)
        for x, y in zip(df.loc[:,'MA'], df.loc[:,'MH']):
            string = "a="+str(round(df.loc[i,'a'],1)) + "\n b="+str(round(df.loc[i,'b'],1)) + "\n"+r"$\theta$="+str(round(df.loc[i,'theta'],1))+r"$^{\circ}$"
            plt.text(x, y, string, color="red", fontsize=15)
            i = i+1

            ax0.minorticks_on()
            start, end = ax0.get_xlim()
            ax0.xaxis.set_ticks(np.arange(start, end, 100))
            ax0.tick_params('both', direction='in', length=10, width=2, which='major')
            ax0.tick_params('both', direction='in', length=5, width=1, which='minor')
            
            plt.setp(ax0.get_xticklabels(), fontsize=33)
            plt.xlabel(r"$\mathrm{m_A}$ (GeV)", fontname="Arial", fontsize=30)
            plt.setp(ax0.get_yticklabels(), fontsize=33)
            plt.ylabel(r"$\mathrm{m_H}$ (GeV)", fontname="Arial", fontsize=30)
            plt.text(0.03, 0.95, r"$\textbf{CMS}$" + " Preliminary Simulation", fontsize=30, transform=ax0.transAxes)
            plt.text(0.72, 0.95, r"35.9 " + r"$\mathrm{fb^{-1}}$" + r" (13 TeV)", fontsize=30, transform=ax0.transAxes)
            plt.title("Ellipse parameters for {0} category".format(cat), fontsize=34)

        fig.savefig("ellParam_{0}.pdf".format(cat))
        fig.savefig("ellParam_{0}.png".format(cat))
    
if __name__ == "__main__":
    main()

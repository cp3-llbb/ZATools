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

    df = pd.read_csv('acceptance.csv', header=None)
    df.columns = ['MA', 'MH', 'acc']
    fig = plt.figure(figsize=(20,20))

    #ml.rcParams['image.cmap'] = 'gist_heat'
    gs = gridspec.GridSpec(2, 2, width_ratios=[4.5,1], height_ratios=[1,4.5])
    gs.update(wspace=0.0, hspace=0.0)
    ax0 = plt.subplot(gs[1,0])

    i=0
    plt.plot(df.loc[:,'MA'], df.loc[:,'MH'], "-o", linestyle='None')
    plt.xlim(0, 800)
    plt.ylim(100, 1200)
    for x, y in zip(df.loc[:,'MA'], df.loc[:,'MH']):
        plt.text(x, y, round(df.loc[i,'acc'],1), color="red", fontsize=24)
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
    plt.title("Acceptance (\%)", fontsize=34)

    '''
    axx = plt.subplot(gs[0,0], sharex=ax0)
    xedges = np.linspace(0, 1500, 150)
    yedges = np.linspace(0, 1500, 150)
    H, xedges, yedges = np.histogram2d(xedges, yedges, bins=(xedges, yedges))
    print (len(df.iloc[:,2]))
    H = df.iloc[:,2].reshape(150,150).T
    xcenters = np.linspace(5.0, 1495.0, 150) 
    ycenters = np.linspace(5.0, 1495.0, 150)
    hx, hy = H.sum(axis=0), H.sum(axis=1)
    projx = []
    for i, x_cent in enumerate(xcenters):
        if int(hx[i]) == 0:
            continue
        projx.extend(np.repeat(x_cent, int(hx[i])))
    projx = np.asarray(projx)
    print (len(projx))
    axx.hist(projx, bins=40, range=(50, 450), normed=True, histtype='bar', facecolor="#4CB391", rwidth=1, align='mid', alpha=0.75)
    plt.xlim(70,430)
    axx.axis('off')

    axy = plt.subplot(gs[1,1], sharey=ax0)
    projy = []
    for i, y_cent in enumerate(ycenters):
        if int(hy[i]) == 0:
            continue
        projy.extend(np.repeat(y_cent, int(hy[i])))
    projy = np.asarray(projy)
    #print (len(projy))
    axy.hist(projy, bins=40, range=(230,630), normed=True, orientation=u'horizontal', histtype='bar', facecolor="#4CB391", rwidth=1, align='mid', alpha=0.75)
    plt.ylim(250,630)
    axy.axis('off')
    
    jet= plt.get_cmap('jet')
    rhos = [0.5, 1., 1.5, 2, 2.5, 3.] 
    colors = iter(jet(np.linspace(0.64,1,6)))
    with open('ellipseParam_{0}.json'.format(args.category)) as f1:
        parameters = json.load(f1)
    ells = [] 
    for (mbb, mllbb, a_squared, b_squared, theta_rad, mA, mH) in parameters:
        if (mA == 300 and mH == 500):
            x = mbb
            y = mllbb
            print (mA, mH)
            for i, rho in enumerate(rhos):
                a = math.sqrt(a_squared)
                b = math.sqrt(b_squared)
                theta = theta_rad * 57.29   #conversion from radiants to degrees
                ells.append(Ellipse((x, y), rho*a, rho*b, theta, edgecolor=next(colors), linewidth=1, facecolor='none'))

    for ell in ells: 
        ax0.add_artist(ell)

    #params = {'legend.fontsize': 20,'legend.handlelength': 30} 
    #plt.rcParams.update(params)
    
    ax0.legend(ells, [r'$\rho$ = {}'.format(rho) for rho in rhos], loc='upper left', bbox_to_anchor=(0.1, 0.9), prop={'size': 20}, labelspacing=0.7)
    '''

    fig.savefig("acceptance.pdf")
    fig.savefig("acceptance.png")
    
if __name__ == "__main__":
    main()

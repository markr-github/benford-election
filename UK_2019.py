# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 15:51:20 2020
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl

# figure format
sns.set_style('whitegrid')
mpl.rcParams['axes.grid.axis'] = 'y'

# load data and define functions to extract Benford values
df = pd.read_csv('./data/UK_GE_constituency_results.csv')
first_digit = lambda X : np.array([ int(str(x)[0]) for x in X ])
digit_bars = lambda X : np.histogram(X,bins=np.arange(0.5,10))[0]
digits = np.arange(1,10)
benfords_norm = np.log10(1 + 1/digits)

# load top 4 national party counts: conservative, labour, lib dem, brexit,
# and save their names for axis titles.
party_keys = np.array([ 'con','lab','ld','brexit' ])
party_names = np.array([ 'Conservative','Labour','Lib Dem','Brexit'])
party_votes = { k : digit_bars(first_digit(df[k])) for k in party_keys }

# make figure.
kws = {
   'xticks' : digits,
   'ylim' : [0,0.5],
   }
fig,axs = plt.subplots(2,2,subplot_kw=kws,figsize=(6,6))

for a,k in enumerate(party_keys):
    ax = axs.flatten()[a]
    ax.set_title(party_names[a])
    ax.bar(digits,party_votes[k] / party_votes[k].sum(),label='First digit',
           color='None',edgecolor='blue')
    ax.plot(digits,benfords_norm,'r-',lw=4,label='Benford prediction')
    ax.legend()

for ax in axs[:,0]:
    ax.set_ylabel('Fraction of constituencies',fontsize=14)
for ax in axs[1]:
    ax.set_xlabel('Vote count first digit',fontsize=14)

fig.tight_layout()

# -*- coding: utf-8 -*-
"""
Created on Tue N
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
df = pd.read_csv('./data/pa_allegheny_county.csv',skiprows=2)
data = df[df.columns[[0,1, 4, 7, 10]]][:-1] # remove total count at bottom

data.columns = ['Precinct','Registered','Biden','Trump','Jorgensen']

trump_wins = data['Trump'] > data['Biden']
biden_wins = data['Biden'] > data['Trump']

first_digit = lambda X : np.array([ int(str(x)[0]) for x in X ])
digit_bars = lambda X : np.histogram(X,bins=np.arange(0.5,10))[0]
digits = np.arange(1,10)
benfords_norm = np.log10(1 + 1/digits)

plot_data = np.array([
    digit_bars(first_digit(data['Biden'][trump_wins])),
    digit_bars(first_digit(data['Trump'][trump_wins])),
    digit_bars(first_digit(data['Biden'][biden_wins])),
    digit_bars(first_digit(data['Trump'][biden_wins])),
    ])
plot_titles = np.array([
    "Biden votes, Trump precincts",
    "Trump votes, Trump precincts",
    "Biden votes, Biden precincts",
    "Trump votes, Biden precincts",
    ])

####
#### Plot Biden counts on left, Trump counts on right.
fig,axs = plt.subplots(2,2,figsize=(7,7))
sns.despine()

for a,ax in enumerate(axs.flatten()):
    ax.set_title(plot_titles[a])
    ax.bar(digits,plot_data[a],label='First digit')
    # scaled Benford
    scale = plot_data[a].sum()
    ax.plot(digits,benfords_norm*scale,'r-',lw=3,label='Benford prediction')
    
axs[0,0].legend()
for ax in axs[:,0]:
    ax.set_ylabel("Precincts",fontsize=14)
for ax in axs[1]:
    ax.set_xlabel("First digit of vote count",fontsize=14)

plt.tight_layout()
from scipy import stats, constants
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import math 
import seaborn as sns
import matplotlib.ticker
import os 
from argument import parser

sys.setrecursionlimit(10000)

def dropUnnecessary(df, args):
    df.drop(df.columns.difference(['Magnetic Field (Oe)','Channel 1 Resistance',
                                   'Channel 2 Resistance','Channel 3 Resistance']), 1, inplace=True)
    #df = df.drop(drop_columns,axis = 1)
    #df = df.rename(columns={'Magnetic Field (Oe)':'B', 'Channel '+ args.R +' Resistance':'R',
            #'Channel ' + args.H + ' Resistance':'H'})
    df = df.rename(columns={'Magnetic Field (Oe)':'B', 'Channel '+ args.R +' Resistance':'R',
            'Channel ' + args.H + ' Resistance':'H'})
    df.drop(df.columns.difference(['B','R','H']), 1, inplace=True)
    df = df.dropna()
    #df.drop(df.columns.difference(['B','R','H']), 1, inplace=True)
    return df
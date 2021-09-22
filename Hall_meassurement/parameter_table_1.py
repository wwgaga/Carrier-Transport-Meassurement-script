from scipy import stats, constants
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import math 
import seaborn as sns
import matplotlib.ticker
import os 

#read the data file
#input [filenames] and [temperature]

import glob

def parameter(T_columns):
    glob.glob("datafile-*.csv")
    filenames= []
    #T_columns = [2,5,10,25,75,100,125,175,200,250,275,300]
    for T in T_columns:
        file_name = 'Hall calculated parameter_'+str(T)+'K'
        filenames.append(file_name)
    list_of_dfs = [pd.read_csv(filename) for filename in filenames]
    for dataframe, filename in zip(list_of_dfs, filenames):
        dataframe['filename'] = filename
        combined_df = pd.concat(list_of_dfs, ignore_index=True)
    combined_df['Temperature(K)']= T_columns
    combined_df.drop(['Unnamed: 0'],axis=1, inplace=True)
    #combined_df.to_csv('all parameters',sep=',')
    return combined_df
'''
def plotfigure(df,column,ylabel):
    sns.set()
    fig = plt.figure(figsize=(6,5))
    ax = fig.add_subplot(111)
    ax.plot(df['Temperature(K)'],df[column],'b',marker=".", markersize=20)
    ax.set_title(column+'vs Temperature(K)',loc = 'center',fontsize=14,y = 1.1)
    ax.ticklabel_format(style='sci', axis='x', scilimits=(0,4))
    ax.set_xlabel(r'Temperature(K)',fontsize=20)
    ax.set_ylabel(ylabel,fontsize=20)
    ax.tick_params(axis='both', labelsize=18)
    ax.yaxis.get_offset_text().set_fontsize(18)
    my_file = column + '.png'
    fig.savefig(my_file , bbox_inches = "tight") 
    plt.close()

'''
def plot(combined_df):
    sns.set()
    fig = plt.figure(figsize=(6,5))
    ax1 = fig.add_subplot(111)
    ax1.plot(combined_df['Temperature(K)'],abs(combined_df['Carrier concentration[1/cm^3]:']),'r',marker=".", markersize=20)
    ax1.set_title('Carrier concentration vs Temperature(K)',loc = 'center',fontsize=14,y = 1.1)
    ax1.ticklabel_format(style='sci', axis='x', scilimits=(0,4))
    ax1.set_xlabel(r'Temperature(K)',fontsize=20)
    ax1.set_ylabel(r'Carrier concentration $(\frac{1}{cm^3})$',fontsize=20)
    ax1.tick_params(axis='both', labelsize=18)
    ax1.yaxis.get_offset_text().set_fontsize(18)
    my_file_1 = 'carrier concentration.png'
    fig.savefig(my_file_1,bbox_inches = "tight") 
    plt.close()

    fig = plt.figure(figsize=(6,5))
    ax2 = fig.add_subplot(111)
    ax2.plot(combined_df['Temperature(K)'],combined_df['Mobility by n :'],'b',marker=".", markersize=20)
    ax2.set_title('Mobility vs Temperature(K)',loc = 'center',fontsize=14,y = 1.1)
    ax2.ticklabel_format(style='sci', axis='y', scilimits=(0,2))
    ax2.set_xlabel(r'Temperature', fontsize=18)
    ax2.set_ylabel(r'Mobility_by_n $(\frac{cm^2}{v*s})$',fontsize=20)
    ax2.tick_params(axis='both', labelsize=18)
    ax2.yaxis.get_offset_text().set_fontsize(18)
    my_file_2 = 'mobility by n.png'
    fig.savefig(my_file_2,bbox_inches = "tight") 
    plt.close()

    fig = plt.figure(figsize=(6,5))
    ax3 = fig.add_subplot(111)
    ax3.plot(combined_df['Temperature(K)'],combined_df['Mobility by n :'],'b',marker=".", markersize=20)
    ax3.set_title('Mobility vs Temperature(K)',loc = 'center',fontsize=14,y = 1.1)
    ax3.ticklabel_format(style='sci', axis='y', scilimits=(0,2))
    ax3.set_xlabel(r'Temperature', fontsize=18)
    ax3.set_ylabel(r'Mobility_by_slope $(\frac{cm^2}{v*s})$',fontsize=20)
    ax3.tick_params(axis='both', labelsize=18)
    ax3.yaxis.get_offset_text().set_fontsize(18)
    my_file_3 = 'mobility by slope.png'
    fig.savefig(my_file_3,bbox_inches = "tight") 
    plt.close()
    
'''
    fig = plt.figure(figsize=(6,5))
    ax4 = fig.add_subplot(111)
    ax4.plot(combined_df['Temperature(K)'],combined_df['Resistivity at 0 Oe:'],'g',marker=".", markersize=20)
    ax4.set_title('Resistivity at 0 Oe vs Temperature(K)',loc = 'center',fontsize=14,y = 1.1)
    ax4.set_xlabel(r'Temperature(K)',fontsize=20)
    ax4.set_ylabel(r'Resistivity at 0 Oe $(Ohm*cm)$ at 0 Oe',fontsize=20)
    ax4.tick_params(axis='both', labelsize=18)
    ax4.yaxis.get_offset_text().set_fontsize(18) 
    ax4.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    my_file_4 = 'Resistivity at 0 Oe.png'
    fig.savefig(my_file_4,bbox_inches = "tight") 

    fig = plt.figure(figsize=(6,5))
    ax4 = fig.add_subplot(111)
    ax4.plot(combined_df['Temperature(K)'],1/combined_df['Resistivity at 0 Oe:'],'y',marker=".", markersize=20)
    ax4.set_title('Conductivity at 0 Oe vs Temperature(K)',loc = 'center',fontsize=14,y = 1.1)
    ax4.set_xlabel(r'Temperature(K)',fontsize=20)
    ax4.set_ylabel(r'Conductivity $(\frac{1}{Ohm*cm})$ at 0 Oe',fontsize=20)
    ax4.tick_params(axis='both', labelsize=18)
    ax4.yaxis.get_offset_text().set_fontsize(18)
    my_file_4 = 'Conductivity.png'
    fig.savefig(my_file_4,bbox_inches = "tight") 
    
    combined_df_1 = combined_df.style.format({col: '{:.3e}' for col in combined_df.columns[:4]})

    print(combined_df_1.data)

    #plot table with scietific notation 

    fig, ax = plt.subplots()

    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    columns = ['(Asymmetric) Slope:','Carrier concentration[1/cm^3]:','Resistivity at 0 Oe:','Mobility:','filename','Temperature(K)']

    ax.table(cellText=combined_df_1.data.values, colLabels=combined_df_1.data.columns, loc='center')
    fig.tight_layout()
    plt.savefig('parameter.png',dpi= 512)
    plt.show()
'''
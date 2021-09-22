import pandas as pd 
import os
import matplotlib.pyplot as plt
import numpy as np 
from scipy import optimize
import math
import seaborn as sns
# change the channel 
def dropUnnecessary(df):
    df.drop(df.columns.difference(['Temperature (K)','Bridge 1 Resistance (Ohms)',
                                   'Bridge 2 Resistance (Ohms)','Bridge 3 Resistance (Ohms)']), 1, inplace=True)
    df = df.rename(columns={'Bridge 1 Resistance (Ohms)':'R_xx_1',
                            'Bridge 2 Resistance (Ohms)':'R_xx_2'})
    return df

def findresistivity(resistance,L,W,t):#m
    resistivity = resistance*W*t/L
    return float(resistivity)

# plot resistivity  
# define a plot format 
def plot(df,column):
    sns.set()
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    fig.suptitle(column.split('$')[0] + ' VS temeprature',fontsize=18)
    ax1.plot(df['Temperature (K)'],df[column],'b-',marker='s',markevery=100,label = column.split('$')[0])#ohm*cm
    ax1.set_xlabel('Temperature (K)',fontsize=18)
    ax1.set_ylabel(column,fontsize=18)
    ax1.set_ylim([min(df[column]),max(df[column])])
    ax1.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax1.tick_params(axis='both', labelsize=18)
    ax1.yaxis.get_offset_text().set_fontsize(18)    
    ax1.legend(loc='upper left')
    #ax1.set_yscale('log') 
    plt.autoscale()
    plt.show()
    fig.savefig(column.split('$')[0]+'.png',bbox_inches = "tight")
    plt.close()

def fileResistivity_xx(path,L_1,W,t):
    (head, extension) = os.path.splitext(path)
    newpath =  head + '-cleaned' + extension
    df = pd.read_csv(path,skiprows=30)
    df = dropUnnecessary(df)
    #df = df[df['Temperature (K)']>120]
    df['Resistivity_xx_1 $(Ohm*cm)$'] = 0.00
    df['Resistivity_xx_2 $(Ohm*cm)$'] = 0.00
    df['Conductivity_xx_1 $(Siemens/cm)$'] = 0.00
    df['Conductivity_xx_2 $(Siemens/cm)$'] = 0.00

    for i in range(len(df.index)):
        df['Resistivity_xx_1 $(Ohm*cm)$'][i] = findresistivity(df['R_xx_1'][i],L_1,W,t)*1e2
        df['Resistivity_xx_2 $(Ohm*cm)$'][i] = findresistivity(df['R_xx_2'][i],L_1,W,t)*1e2
        df['Conductivity_xx_1 $(Siemens/cm)$'][i] = 1/(findresistivity(df['R_xx_1'][i],L_1,W,t)*1e2)
        df['Conductivity_xx_2 $(Siemens/cm)$'][i] = 1/(findresistivity(df['R_xx_2'][i],L_1,W,t)*1e2)
    df.to_csv(newpath+'.csv',index=False)#Ohm*cm
    
    #quick plot 
    df.set_index('Temperature (K)').plot(subplots=True,
                 kind='line', lw=3.5,linestyle='-',
                 grid=True, figsize=(20,10),layout=(3, 3), sharex=True)
    # edit the legends 
    #[ax.legend(loc=2,prop={'size': 20}) for ax in plt.gcf().axes] 

    plt.gcf().tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.gcf().suptitle("PPMS Cooldown RvsT meassurement",fontsize=20)
    plt.savefig('PPMS Cooldown RvsT meassurement.png')
    plt.show()
    
    # plot seperately 
    #resistivity_xx_2
    plot(df,'Resistivity_xx_2 $(Ohm*cm)$')
    plot(df,'Conductivity_xx_2 $(Siemens/cm)$')
    # resistivity_xx_1
    df_1 = df[df['Temperature (K)']>10]
    plot(df_1,'Resistivity_xx_1 $(Ohm*cm)$')
    plot(df_1,'Conductivity_xx_1 $(Siemens/cm)$')

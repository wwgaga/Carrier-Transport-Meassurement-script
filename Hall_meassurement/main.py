import argparse
import sys 
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# sys.path.insert()

from argument import parser
import rename_hall_geometry_1 as rename 
import ppms_mo_r_cooldowny as ppms 
import parameter_table_1 as parameter 

def rexx_cooldown(re_xx):
    #re_xx should be a dataframe contain temperature, r_xx_1, r_h_1,
    # r_h_2 and resistivity_xx_1
    T_columns = [2,5,10,25,50,75,100,125,150,175,200,225,250,275,300]
    #T_columns = [2]
    c = []
    d = [] 
    for T in T_columns: 
        #a = re_xx[re_xx['Temperature (K)'] < (T+0.1)]
        #b = a[re_xx['Temperature (K)'] > (T-0.1)]
        #### this way will lead UserWarning: Boolean Series key will be reindexed to match DataFrame index.
        b = re_xx[(re_xx['Temperature (K)'] < (T+0.1) ) & (re_xx['Temperature (K)'] > (T-0.1))]
        c.append(b.mean().Resistivity_xx_2)
        d.append(b.mean().Resistivity_xx_1)# previous xx_1
    return pd.DataFrame({'Temperature (K)':T_columns, 
                        'Resistivity_xx_2':c,
                        'Resistivity_xx_1':d}), T_columns#previous xx_1,Unit:Ohm*cm

def main(args):
    path = '/Users/wuriga/Documents/project/GB/'
    new_datapath = os.path.join(path,args.datapath)
    print(new_datapath)
    re_xx, Ts = rexx_cooldown(pd.read_csv(os.path.join(new_datapath, args.datafile)))
    print(re_xx,Ts)
    new_my_path = os.path.join(new_datapath,args.my_path)
    if not os.path.exists(new_my_path):
        os.makedirs(new_my_path)
    for T in Ts:
        #define as "MR_Ag_doped_PbTe_3_III_D_2k_1T"
        hallname = args.hallfilename + '_' + args.samplenumber+'_' + str(T) + 'K_1T.dat'
        #hallname = args.hallfilename + '_' + args.samplenumber+'_' + '9T_' + str(T) + 'K_Dyna.dat'
        print(hallname)
        data = pd.read_csv(os.path.join(new_datapath, hallname), skiprows=17)#30
        data_1 = rename.dropUnnecessary(data,args)
        #print('this is data_1, ', data_1)
        re_xx_T = float(re_xx[re_xx['Temperature (K)'] == T]['Resistivity_xx_2'])#previous xx_1
        #print(re_xx_T)
        p = ppms.PpmsData(data_1, re_xx_T, args.d, args.W, args.L, T, my_path=new_my_path)
        #break
        p.returnData(str(T)+'.png')
        p.normMR()
        

    ######################## data calculation ########################
    os.chdir(new_my_path)
    if args.inspect:
        temp_df = parameter.parameter(Ts)
        temp_df.to_csv('para.csv', index=False)
    parameter.plot(parameter.parameter(Ts))

    ######################## plot MR percentage ########################
    sns.set()
    for T in Ts:
        data_n= pd.read_csv('MR '+str(T)+'K')
        plt.plot(data_n['B'], data_n['MR%'], label = str(T) + 'K')
        plt.xlabel('Magnetic field(T)')
        plt.ylabel('MR%')
        plt.grid(True)
        plt.legend()
        plt.savefig('MR%.png')

if __name__ == '__main__':
    args = parser()
    main(args)


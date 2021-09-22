import numpy as np
import pandas as pd 
import os 
import matplotlib.pyplot as plt
import seaborn as sns 
import glob 
from args_conbine import parser_conbine
def conbine(args):
    #path = '/Users/wuriga/Documents/project/GB/*_2.9/'
    #dat_name = glob.glob(args.path + '/Pure*/*-cleaned.csv')
    par_name = glob.glob(os.path.join(args.path,args.my_image,'para.csv'))

    #print(dat_name)
    print(par_name)
    
    #par_df = pd.read_csv(par_name[-1])
    #par_df.head()

    #dat_df = pd.read_csv(dat_name[-1])
    #dat_df.head()

    materials = [s.split('/')[-3] for s in par_name]
    print(materials)
    #basepath = '/Users/wuriga/Documents/project/GB/Pure_PbTe_angle_2.9'
    for material in materials:
        print(material)
        name = os.path.join(args.path, material, args.my_image, 'para.csv')
        name_ = glob.glob(os.path.join(args.path, material, '*-cleaned.csv'))
        print(name_)
        print(name)
        assert len(name_) == 1
        name_ = name_[0]
        par_df = pd.read_csv(name)
        #print(par_df)
        dat_df = pd.read_csv(name_)

        Ts = []
        Mobs_n = []
        Mobs_slope = []
        Cons = []
        Res_1 = []
        Res_2 = []

        for T in par_df['Temperature(K)']:
            T = float(T)
            df = dat_df[(dat_df['Temperature (K)'] < (T+0.2) ) & (dat_df['Temperature (K)'] > (T-0.2))]
            df_ = par_df[par_df['Temperature(K)']==int(T)]

            if 'Resistivity_xx_2' in df.columns:
                if len(df)>1:
                    re_1 = np.mean(np.array(df['Resistivity_xx_1'].tolist()))
                    re_2 = np.mean(np.array(df['Resistivity_xx_2'].tolist()))
                else:
                    re_1 = df['Resistivity_xx_1'].astype(float)
                    re_2 = df['Resistivity_xx_2'].astype(float)
                Ts.append(int(T))
                Res_1.append(re_1)
                Res_2.append(re_2)
                Mobs_slope.append(float(df_['Mobility by slope :']))
                Mobs_n.append(float(df_['Mobility by n :']))
                Cons.append(float(df_['Carrier concentration[1/cm^3]:']))
            else: 
                if len(df)>1:
                    re_1 = np.mean(np.array(df['Resistivity_xx_1'].tolist()))
                else:
                    re_1 = float(df['Resistivity_xx_1'])  
                Ts.append(int(T))
                Mobs_slope.append(float(df_['Mobility by slope :']))
                Mobs_n.append(float(df_['Mobility by n :']))
                Res_1.append(re_1)
                Res_2.append(np.nan)
                Cons.append(float(df_['Carrier concentration[1/cm^3]:']))
    
        d = {'Temperture (K)': Ts, 'Mobility by slope'+r' $(\frac{cm^2}{v*s})$': Mobs_slope, 
            'Mobility by n'+r' $(\frac{cm^2}{v*s})$':Mobs_n,
            'Concentration'+r' $(\frac{1}{cm^3})$': Cons, 
            'Resistivity_xx_1'+r' $(Ohm*cm)$': Res_1,'Resistivity_xx_2'+r' $(Ohm*cm)$': Res_2}
        new_df = pd.DataFrame(data=d)
        new_df.head()
        new_df_filename = material +'.csv'
        print(new_df_filename)
        new_df.to_csv(os.path.join(args.path,new_df_filename), index=False)

if __name__ == '__main__':
    args = parser_conbine()
    conbine(args)

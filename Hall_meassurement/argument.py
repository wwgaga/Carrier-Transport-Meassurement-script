import argparse

def parser():
    parser = argparse.ArgumentParser(description='PPMS data processing')
    parser.add_argument('-datapath', default='PbTe_2_VD',
        help='PPMS data folder,input typle:PbTe_2_VD')
    parser.add_argument('-hallfilename',default = 'MR_Ag_doped_PbTe',
        help ='PPMS hall measurement datafile name' )
    parser.add_argument('-samplenumber',default='3_VD',
        help='the sample number')
    parser.add_argument('-datafile', default='MR_PbTe_2_VD_300K_2k_sweep_Dyna_1T-cleaned.dat', 
        help='PPMS r_xx cleaned data file')
    parser.add_argument('-my_path', default='image', 
        help='the directory to save the plot,input type:image')
    parser.add_argument('-d', type=float, default='1.513e-6', 
        help='sample thickness (meter)')
    parser.add_argument('-W', type=float, default='2.743e-6', help='sample width (meter)')
    parser.add_argument('-L', type=float, default='4e-6', help='sample length (meter)')
    parser.add_argument('-inspect', type=bool, default='False', 
        help='save data in to csv for inspection')
    parser.add_argument('-R',default='1',
        help='hall meassurement r_xx channel,input:Channel number , 1/2/3')
    parser.add_argument('-H',default='3',
        help='hall meassurement hall channel,input:Channel number,1/2/3')
    #parser.add_argument('-T_columns',default='[2,5,10,25,50,75,100,125,150,175,200,225,250,275,300]',
        #help='T_levels,input:T_levels')
    return parser.parse_args()
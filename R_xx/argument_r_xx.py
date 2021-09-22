import argparse

def parser_r_xx():
    parser_r_xx = argparse.ArgumentParser(description='PPMS cooldown resistivity_xx caculation')
    parser_r_xx.add_argument('-path',help='PPMS data folder')
    parser_r_xx.add_argument('-datafile',help='PPMS cooldown R_xx')
    parser_r_xx.add_argument('-W',type =float,help='sampel width(meter)')
    parser_r_xx.add_argument('-L',type =float,help='sample length(meter)')
    parser_r_xx.add_argument('-d',type =float,help='sample thickness(meter)')
    return parser_r_xx.parse_args()
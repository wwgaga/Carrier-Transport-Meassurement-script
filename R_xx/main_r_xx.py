import os 
import argparse
import R_xx_hall_geometry_1 as r_xx
from argument_r_xx import parser_r_xx 
import pandas as pd 

def main_r_xx(args):
    os.chdir(args.path)
    r_xx.fileResistivity_xx(args.datafile, 
                            args.L, args.W, args.d)

if __name__ == '__main__':
    args = parser_r_xx()
    main_r_xx(args)
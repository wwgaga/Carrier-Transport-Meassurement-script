import argparse

def parser_conbine():
    parser_conbine = argparse.ArgumentParser(description='PPMS data processing')
    parser_conbine.add_argument('-path', default='/Users/wuriga/Documents/project/GB/*_2.9/',
        help='GB orientation angle folder')
    parser_conbine.add_argument('-my_image',default = 'image',
        help ='stored plotted images of comparison GB vs no GB ' )
    parser_conbine.add_argument('-basepath', default='/Users/wuriga/Documents/project/GB/Pure_PbTe_angle_2.9',
        help='GB orientation angle folder')
    
    return parser_conbine.parse_args()
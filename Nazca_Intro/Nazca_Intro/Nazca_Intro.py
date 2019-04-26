# Import libraries
# You should try an import the bare minimum of modules
import sys # access system routines
import os
import glob
import re

# Introduction to the Mask Layout code Nazca
# Homepage: https://nazca-design.org/
# Manual: https://nazca-design.org/manual/
# Tutorials: https://nazca-design.org/tutorials/
# R. Sheehan 15 - 2 - 2019

# Have to tell Visual Studio where the Nazca package is located to ensure it works
sys.path.append('c:/program files (x86)/microsoft visual studio/shared/anaconda3_64/lib/site-packages/')
import nazca

import Nazca_Tutorials

def main():
    pass

if __name__ == '__main__':
    main()

    pwd = os.getcwd() # get current working directory

    print(pwd)

    Nazca_Tutorials.Example_16()
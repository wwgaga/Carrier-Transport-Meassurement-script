# Quantum Design Dynacool and PPMS Data Analysis

This script is used to analyze the data collected by Quantum Design Dynacool and PPMS for temperature-dependent conductivity and Hall measurement. The device employs hall bar geometry and connects through Bridge 1 for temperature-dependent conductivity measurement and Bridge 2 or 3 for Hall measurement, configured via the PPMS measurement software and a specific break-out box.

The measurement process is divided into two parts:

1. **Resistivity Cooldown Measurement**: This part involves measuring the longitudinal resistivities (xx-direction) as the temperature cools down from 300K to 2K.

2. **Hall Measurement**: Hall measurements are taken under magnetic fields ranging from -1 T to 1 T or -9 T to 9 T at different temperature levels (2K, 5K, 10K, 25K, 50K, 75K, 100K, 125K, ..., 300K). The magnetic resistance at each temperature level during the magnetic field scanning is recorded, and physical parameters such as carrier concentration and mobility are calculated. These calculated transport properties are visualized in the figure below.

## Usage

Due to the implement of the argument, only the data file path and saved path of the target calculated CSV file and plotted figures.
To analyze and plot the temperature  in Redshift, run 

To run the ETL pipeline and load data into Redshift, execute 


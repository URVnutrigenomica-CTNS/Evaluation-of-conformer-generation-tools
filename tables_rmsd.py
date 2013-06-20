#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2012-2013 María José Ojeda Montes <mjose.ojeda@urv.cat>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
#This script can be applied when RMSDs have been calculated between bioactive conformers and the set of conformers generated by each program or method. 
#Then, the lowest RMSD (for each bioactive conformer) is selected and it is  organised in a range of values. Finally, it generate a table for each number of rotatable bonds where x axis is 
#the number of bioactive conformer that are in a range of rmsd value and y axis is the different methods.   The ranks are 0, <0.5, <1,<1.5,<2,<2.5,>3 A. 

import os, csv
from glob import glob

#CHANGE YOUR PATHS IN THOSE VARIABLES
values_rmsd = glob('RMSD_conformacions/*_Rotatable')
output_tables =  'Tables_RMSD/'
if not os.path.isdir(output_tables):
    os.makedirs(output_tables)
 
#Programs that we have already calculate rmsd value 
programs = ['BALLOON', 'CLEAN3D',  'CONFAB', 'CONFGEN', 'CYNDI', 'OMEGA', 'ROTATE', 'VCONF', 'XEDEX' ]

#dictionary where the clue is the top of the rank of rmsd and the value is the number of bioactive poses that has obtain the minimum rmsd  in that rank
rangs_rmsd = {0:0, 0.5:0, 1:0, 1.5:0, 2:0, 2.5:0, 3:0, '>3':0}
keys = rangs_rmsd.keys()
keys.remove('>3')
keys.sort()

for file_rmsd in values_rmsd:
    enrot = dir_n_enll_rot.split('/')[-1].split('_Rotatable')[0]

    #To generate a table with the results in a csv file
    fitxercsv = open(output_tables + '/' + enrot + '_Rotatable_bonds.csv', 'wb')
    escriptor = csv.writer(fitxercsv)
    escriptor.writerow(['Program'] + keys + ['>3'])
   
    #To select the lowest RMSD of each set of conformers
    for program in programs:
        for struc_exp in glob(os.path.join(file_rmsd, program, '*.csv')):
            list_rmsd_conf = []
            fitxercsv = open(struc_exp,  'rb')
            print struc_exp
            for line in fitxercsv:
                linelist = line.split('","')
                if line.startswith('"Index"') or len(linelist) < 6:
                    continue
                #list of all rmsd value for this bioactive conformation
                rmsd = float(linelist[3])
                list_rmsd_conf.append(rmsd)
            #Selection of the minimum rmsd value for this bioactive conformation
            min_rmsd= min(list_rmsd_conf)
            
            #Dictionary that act as a meter of the number of bioactive conformer that has had a RMSD value in this range (i.e nº of bioactive conformer that has a conformation whose lowest RMSD between 0.5 and 1A)
            for key_dict in keys:
                if min_rmsd <=key_dict: 
                    rangs_rmsd[key_dict]+=1
                    break
            else:
                print 'RMSD higher than 3A'
                rangs_rmsd['>3'] +=1
            print 'The lowest RMSD is %s' % min(list_rmsd_conf) 
            for c in keys:
                print c, ':', rangs_rmsd[c]
            print '>3', ':', rangs_rmsd['>3']
         
        #Generate the ouput file
        escriptor.writerow([program] + [rangs_rmsd[key] for key in keys + ['>3']])
        for key in keys:
            rangs_rmsd[key] = 0
            rangs_rmsd['>3'] = 0
            
    fitxercsv.close()       
                

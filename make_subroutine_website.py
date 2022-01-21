#This function will grab all the subroutines in Ecosim and then dump them
#to html files
#
#Steps:
#1) read in and identify subroutine lines
#2) dump subroutines to txt file
#3) dump subroutines to html file
#
#

import numpy as np
import sys, subprocess, os, re
import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--dir', dest="ecomoddir", type=str, nargs=1, default=[""],
  help='the ecosim_mods directory')

args = parser.parse_args()
ecodir=args.ecomoddir[0]

print(ecodir)
ecofile_list = os.listdir(ecodir)
ecofile_list = [xx for xx in ecofile_list if xx.endswith('.f')]

htmlnew=open("./ecosim_subroutines.html","w")

#read in the js functions, ccs styles, and beginning of the table
#then write to the new file
with open("./preamble.html","r") as prehtml:
    lines = prehtml.readlines()
    for line in lines:
        htmlnew.write(line)
        
#start the html file
#htmlnew.write('<!DOCTYPE html>\n<html>\n<body>')

#write the top level dir for the modules
htmlnew.write('<tr class="parent">\n<td class="row-label">'+str(ecodir)+'</td>\n')
website_link = 'test.html'

#loop where we read over every module and print it subroutines
for ecosim_file in ecofile_list:
    with open(ecodir+ecosim_file,"r") as foldf:
        lines = foldf.readlines()
        for line in lines:
            if line.strip().startswith('module'):
                line_split = re.split(' ',line.strip())
                #htmlnew.write('<h>'+line.strip()+'</h>')
                htmlnew.write('<tr class="child_variable">\n<td class="row-label">&nbsp;&nbsp;&nbsp;&nbsp;'+line_split[1]+'</td>')
            elif line.lower().strip().startswith('subroutine'):
                htmlnew.write('\n')
                #htmlnew.write('<p>'+line.strip()+'</p>\n\n')
                line_split = re.split(' |[(|)]',line.strip())
                print(line_split)
                htmlnew.write('<tr class="child_dataset">\n<td class="row-label"><a href="'+website_link+'" target="_blank">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+line_split[1]+'</a></td>')
                #new_subroutine = True
            #elif line.lower().strip().startswith('call'):
            #    if new_subroutine == True:
            #        htmlnew.write('<p>Depends on:\n')
            #        new_subroutine = False
            #    htmlnew.write(line.strip()+'\n')

#Finish the html file
#htmlnew.write('</body>\n</html>')
htmlnew.write('</tbody>\n</table>\n</body>\n</html>')


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
import argparse, pathlib

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--dir', dest="ecomoddir", type=str, nargs=1, default=[""],
  help='the ecosim_mods directory')

args = parser.parse_args()
ecodir=args.ecomoddir[0]

print(ecodir)
ecofile_list = os.listdir(ecodir)
ecofile_list = [xx for xx in ecofile_list if xx.endswith('.f')]

#Make the directory for the files to go in
pathlib.Path("./ecosim_website/subroutine_htmls/").mkdir(parents=True,exist_ok=True)

htmlnew=open("./ecosim_website/ecosim_subroutines.html","w")

#read in the js functions, ccs styles, and beginning of the table
#then write to the new file
with open("./preamble.html","r") as prehtml:
    lines = prehtml.readlines()
    for line in lines:
        htmlnew.write(line)
        
#write the top level dir for the modules
htmlnew.write('<tr class="parent">\n<td class="row-label">'+str(ecodir)+'</td>\n')
#website_link = 'test.html'

#loop where we read over every module and print it subroutines
for ecosim_file in ecofile_list:
    with open(ecodir+ecosim_file,"r") as foldf:
        lines = foldf.readlines()
        for line in lines:
            if line.strip().startswith('module'):
                line_split = re.split(' ',line.strip())
                htmlnew.write('<tr class="child_variable">\n<td class="row-label">&nbsp;&nbsp;&nbsp;&nbsp;'+line_split[1]+'</td>')
            elif line.lower().strip().startswith('subroutine'):
                htmlnew.write('\n')
                line_split = re.split(' |[(|)]',line.strip())
                #genrate subroutine html file

                #print(line_split)
                website_link = './subroutine_htmls/'+line_split[1]+'.html'
                f_sub_html = open('./ecosim_website/'+website_link,'w')
                f_sub_html.write('<html>\n\t<body>')
                f_sub_html.write('\t\t<h2>'+line_split[1]+'</h2>')
                if len(line_split)>2:
                    f_sub_html.write('\t\t<p>Input Variables: '+line_split[2]+'</p>')
                else:
                    f_sub_html.write('\t\t<p>Input Variables: None</p>')
                #end subroutine file
                f_sub_html.write('\t</body>\n</html>')
                #print(line_split)
                htmlnew.write('<tr class="child_dataset">\n<td class="row-label"><a href="'+website_link+
                              '" target="_blank">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+
                              line_split[1]+'</a></td>')
                #new_subroutine = True
            #elif line.lower().strip().startswith('call'):
            #    if new_subroutine == True:
            #        htmlnew.write('<p>Depends on:\n')
            #        new_subroutine = False
            #    htmlnew.write(line.strip()+'\n')

#Finish the html file
#htmlnew.write('</body>\n</html>')
htmlnew.write('</tbody>\n</table>\n</body>\n</html>')


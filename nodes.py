from pyvis.network import Network
from pathlib import Path
import re
import sys

# This code creates a graph chart using all files in the directory, recursively.
# By default it uses [[name]] for reference, for any /subdir/name.md or .txt file.

if len(sys.argv) == 1:
    targetpath = '.' # default is the script location
else:
    targetpath = sys.argv[1] # location from command line

n = 1 # counter for node ID
net = Network(heading="Graph chart", height="900px", width="1700px") # init network
p = Path(targetpath).glob('**/*') # init path for files
full_list = [] # list of patlib objects
name_dict = {} # dictionary {name: id} for nodes
files = [x for x in p if x.is_file()] # get all files

# Create nodes:

for i in files:
    if not str(i).startswith('.') and not str(i).__contains__('/.'): # make sure there aren't any system or dot files
        full_list.append(i)
        net.add_node(n, label=str(i.name.replace('.md', ''))) # put file on chart
        name_dict[i.name.replace('.md', '').replace('.txt', '')] = n # save id and name for later
        n = n + 1 # increase ID

# Create edges:

for i in files:
    if not str(i).startswith('.') and not str(i).__contains__('/.'): # again, no dot files
        with open(i, 'r', encoding='utf-8') as f: # readonly!
            text = f.read()
            out_obj = re.findall(r'\[\[.*?]]', text)  # get all referenced files
            if len(out_obj) != 0: # if there are any references at all
                for res in out_obj:
                    try: # try-except in case there is no such file
                        # Ugly way to get names, but hey, it works for me
                        net.add_edge(name_dict[res[2:-2]], name_dict[i.name.replace('.md', '').replace('.txt', '')])
                        break
                    except KeyError:
                        print("ignoring key "+res)

net.show_buttons() # add settings to the page
net.show('vis_nodes.html') # open in browser


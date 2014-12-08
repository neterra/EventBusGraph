# Copyright (C) 2014 Federico Bollo, Neterra (http://neterra.com.ar/nueva/dev/)
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Created on 9/16/2014 by Federico Bollo
import os
import os.path
import sys

def write_header(f, count):
	f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" ' + 
			'"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n')
	f.write('<html xmlns="http://www.w3.org/1999/xhtml">\n')
	f.write('<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n')
	f.write('<title>EventBusGraph</title>\n')
	f.write('</head>\n')
	f.write('<body style="font-family:\'arial\'">\n')
	f.write('<script>\n')
	f.write('    var mGraphsCount = ' + str(count) + ';\n')
	f.write('</script>\n')

def write_footer(f, paths):
	f.write('<script src="viz.js"></script>\n')
	f.write('<script>\n')
	f.write('    function src(id) {\n')
	f.write('        return document.getElementById(id).innerHTML;\n')
	f.write('    }\n')
	f.write('    document.body.innerHTML += "<h1>EventBusGraph</h1>"\n')
	count = 0
	for path in paths:
		count = count + 1
		f.write('    document.body.innerHTML += ' +
				'"<font style=\\"font-size:16px;font-weight:bold;color:#3333AA;\\">' +
				str(count) + ') ' + path.replace('\\','\\\\')[:-1] + '</font><br>"\n')
	f.write('    document.body.innerHTML += "<br><hr>"\n')
	f.write('    for (i = 0; i < mGraphsCount; i++) {\n')
	f.write('      result = Viz(src(\'graph_\' + i), format="svg", engine="dot", options=null);\n')
	f.write('      if (i < (mGraphsCount - 1)) {\n')
	f.write('        document.body.innerHTML += result + "<br><br><hr><br>";\n')
	f.write('      } else {\n')
	f.write('        document.body.innerHTML += result + "<br><br><br>";\n')
	f.write('      }\n')
	f.write('}\n')
	f.write('</script>\n')
	f.write('</body>\n')
	f.write('</html>\n')

def write_graph_header(f, count):
	f.write('    <script type="text/vnd.graphviz" id="graph_' + str(count) + '">\n')
	f.write('        digraph g {\n')
	f.write('        graph [\n')
	f.write('        rankdir = "LR"\n')
	f.write('        ];\n')
	f.write('        node [\n')
	f.write('        fontsize = "10"\n')
	f.write('        shape = "ellipse"\n')
	f.write('        style = filled\n')
	f.write('        fillcolor = lightgrey\n')
	f.write('        fontname = arial\n')
	f.write('        ];\n')
	f.write('        edge [\n')
	f.write('        ];\n')

def write_graph_footer(f):
	f.write('            "node0":f0 -> "node1";\n')
	f.write('            "node1" -> "node2":f1;\n')
	f.write('            }\n')
	f.write('    </script>\n');

def write_graph_node_post(f, post_list):
	f.write('        "node0" [\n')
	f.write('        label = "<f3> Post | ')
	first_time = 1
	for item in post_list:
		if first_time != 1:
			f.write(' | ')
		f.write('<f0> ' + item)
		first_time = 0
	f.write('"\n')
	f.write('        shape = "record"\n')
	f.write('        style = filled\n')
	f.write('        color = white\n')
	f.write('        ];\n')

def write_graph_node_event(f, event):
	f.write('        "node1" [\n')
	f.write('        label = "' + event +'"\n')
	f.write('        shape = "ellipse"\n')
	f.write('        style = filled\n')
	f.write('        fillcolor = yellow\n')
	f.write('        fontsize = "12"\n')
	f.write('        ];\n')

def write_graph_node_on_event(f, on_event_list):
	f.write('        "node2" [\n')
	f.write('        label = "<f3> onEvent | ')
	first_time = 1
	for item in on_event_list:
		if first_time != 1:
			f.write(' | ')
		f.write('<f1> ' + item)
		first_time = 0
	f.write('"\n')
	f.write('        shape = "record"\n')
	f.write('        style = filled\n')
	f.write('        color = white\n')
	f.write('        ];\n')

def get_posted_event_class(line, count):
	if "new " not in line:
		print "line nro: " +  str(count)
		event_class = line.split('(')
		print event_class
		if "mEventBus" in line:
			dummy, dummy2, aux = line.split('(')
		else:
			dummy, dummy2, dummy3, aux = line.split('(')
		event_class, dummy, dummy2 = aux.split(')')
	else:
		index = line.find("new ")
		event_class = line[index+4:]
		index = event_class.find("(")
		event_class = event_class[:index]

	if "." in event_class:
		dummy, event_class = event_class.split(".")

	return event_class

def get_paths(fname):
	paths_aux = []
	f = open(fname, 'r')
	path_out_aux = './out.html'
	for line in f:
		if 'path_out' in line:
			dummy, path_out_aux = line.split('=')
		else:
			paths_aux.append(line.rstrip('\n'))
		
	f.close
	
	return paths_aux, path_out_aux.rstrip(' ').lstrip(' ')

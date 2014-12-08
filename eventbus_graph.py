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
from eventbus_graph_functions import *

# Main ------------------------------------------------------------------------
event_types_count = 1000
events_count = 0

dict = {'event': 0}

post_event_list = []
on_event_list = []
event_type_list = []
for i in range(0, event_types_count):
	post_event_list.append([])
	on_event_list.append([])
	event_type_list.append([])

if len(sys.argv) >= 2:
	config_file = sys.argv[1]
	print "config_file: " + config_file
else:
	print "You must enter a config file. Usage: python.exe eventbus_graph.py config_file"
	sys.exit(2)
	
paths, path_out = get_paths(config_file)
print paths

file_pattern = ".java"
path_count = 0
for path in paths:
	print path
	path_count = path_count + 1
	for dirpath, dirnames, filenames in os.walk(path):
		for filename in [f for f in filenames if f.endswith(file_pattern)]:
			fname = os.path.join(dirpath, filename)
			print fname
			f = open(fname, 'r')
			lines_count = 0
			for line in f:
				lines_count = lines_count + 1
				if ('mEventBus.post(' in line) or ('EventBus.getDefault().post(' in line):
					event_class = get_posted_event_class(line, lines_count)
					print event_class
					print fname[len(path):]
					post = str(path_count) + '\\\\' + \
						fname[len(path):len(fname)-len(file_pattern)].replace('\\', '\\\\') + \
						":" + str(lines_count)
					if event_class in dict:
						post_event_list[dict[event_class]].append(post)
					else:
						post_event_list[events_count].append(post)
						event_type_list[events_count].append(event_class)
						dict[event_class] = events_count
						events_count = events_count + 1
				if ('onEvent(' in line) or ('onEventMainThread(' in line) \
					or ('onEventBackgroundThread(' in line) or ('onEventAsync(' in line):
					print "line nro: " +  str(lines_count)
					dummy, event_class = line.split('(')
					event_class, dummy = event_class.split(')')
					dummy = event_class.split(' ')
					event_class = dummy[len(dummy)-2]
					if "." in event_class:
						dummy, event_class = event_class.split(".")
					print event_class
					print fname[len(path):]
					event = str(path_count) + '\\\\' + \
						fname[len(path):len(fname)-len(file_pattern)].replace('\\', '\\\\') + \
						":" + str(lines_count)
					if ('onEventMainThread(' in line):
						event = event + " (MainThread)"
					elif ('onEventBackgroundThread(' in line):
						event = event + " (BackgroundThread)"
					elif ('onEventAsync(' in line):
						event = event + " (Async)"
					if event_class in dict:
						on_event_list[dict[event_class]].append(event)
					else:
						on_event_list[events_count].append(event)
						event_type_list[events_count].append(event_class)
						dict[event_class] = events_count
						events_count = events_count + 1
			f.close()

aux = config_file.split('.')
if len(aux) > 1:
	out_file_name = aux[0] + '_ebg.html'
else:
	out_file_name = config_file + '_ebg.html'

f_out = open(path_out + out_file_name, 'w')

write_header(f_out, events_count)

for i in range(0, events_count):
	write_graph_header(f_out, i)
	write_graph_node_post(f_out, post_event_list[i])
	write_graph_node_event(f_out, event_type_list[i][0])
	write_graph_node_on_event(f_out, on_event_list[i])
	write_graph_footer(f_out)

write_footer(f_out, paths)

f_out.close()

print "events_count " + str(events_count)

for i in range(0, events_count):
	print str(on_event_list[i]) + " | " + str(event_type_list[i])
	print str(post_event_list[i]) + " | " + str(event_type_list[i])




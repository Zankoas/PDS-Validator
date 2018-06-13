from os import listdir
from os import walk
from os import path
import time
from openFile import open_file

def is_event_declaration(lines, line_number, show_warnings, output_file):
	result = list()
	title_found = False
	cond_title = False
	hidden_found = False
	immediate_found = False
	id_found = False
	triggered_only = False
	level = 0
	id_on_line = line_number
	
	if "_event " in lines[line_number].split("#")[0]:
	
		level = lines[line_number].split("_event ")[1].count('{')
		current_line = ' '.join(lines[line_number].split()).split("#")[0].split("_event ")[1].strip()
		
		if "id =" in current_line or "id=" in current_line:
			id_on_line = line_number
			id_found = True
		if "title" in current_line:
			title_found = True
		if "hidden =" in current_line or "hidden=" in current_line:
			hidden_found = True
		if "immediate =" in current_line or "immediate=" in current_line:
			immediate_found = True
		if "is_triggered_only" in current_line:
			triggered_only = True
		
		level = level - current_line.count('}')
		if level < 0:
			level = 0
		line_number = line_number + 1
		
		while level and not ( not level or (((title_found or hidden_found) and triggered_only) and immediate_found)) :#To exit cycle either level must be 0 or immediate is found along with title or hidden. 
			
			current_line = ' '.join(lines[line_number].split()).split("#")[0].strip()
			
			if ("id =" in current_line or "id=" in current_line) and id_found == False:
				id_on_line = line_number
				id_line = ' '.join(lines[id_on_line].split()).split('=')[1].split("#")[0].strip()
				id_found = True
			if "title" in current_line:
				if "title = {" in current_line:
					cond_title = True
				if title_found == True and cond_title == False and show_warnings == True:
					print("two title declarations in event: " + id_line + " in line " + (id_on_line+1).__str__())
					output_file.write("two title declarations in event: " + id_line + " in line " + (id_on_line+1).__str__() + "\n")
				title_found = True
			if "hidden =" in current_line or "hidden=" in current_line:
				if hidden_found == True and show_warnings == True:
					print("two hidden declarations in event: " + id_line + " in line " + (id_on_line+1).__str__())
					output_file.write("two hidden declarations in event: " + id_line + " in line " + (id_on_line+1).__str__() + "\n")
				hidden_found = True
			if "immediate =" in current_line or "immediate=" in current_line:
				#if immediate_found == True and show_warnings == True:
					#print("two immediate declarations in event: " + id_line + " in line " + (id_on_line+1).__str__())
					#output_file.write("two immediate declarations in event: " + id_line + " in line " + (id_on_line+1).__str__() + "\n")
				immediate_found = True
			if "is_triggered_only" in current_line:
				if triggered_only == True and show_warnings == True:
					print("two is_triggered_only declarations in event: " + id_line + " in line " + (id_on_line+1).__str__())
					output_file.write("two is_triggered_only declarations in event: " + id_line + " in line " + (id_on_line+1).__str__() + "\n")
				triggered_only = True
				
			level = level + current_line.count('{') - current_line.count('}')
			line_number = line_number + 1
			
			if len(lines)==line_number:
				if level !=0 and show_warnings == True:
					print("missing } in event: " + id_line)
					output_file.write("missing } in event: " + id_line + "\n")
				result.append(id_on_line)
				result.append(triggered_only)
				return result
				
		if title_found == True or hidden_found == True:
			if immediate_found == False and show_warnings == True:
				print("missing immediate in event: " + id_line + " in line " + (id_on_line+1).__str__())#reminder to write logs on event call
				output_file.write("missing immediate in event: " + id_line + " in line " + (id_on_line+1).__str__() + "\n")
			result.append(id_on_line)
			result.append(triggered_only)
			return result
		
		if immediate_found == True and show_warnings == True:
			print("strange event declaration - neither title nor hidden parameters are present: " + id_line + " in line " + (id_on_line+1).__str__())
			output_file.write("strange event declaration - neither title nor hidden parameters are present: " + id_line + " in line " + (id_on_line+1).__str__() + "\n")
			result.append(id_on_line)
			result.append(triggered_only)
			return result
		else:
			result.append(-1)
			result.append(triggered_only)
			return result
	else:
		result.append(-1)
		result.append(triggered_only)
		return result

def is_event_called(lines, line_number):
	current_line = ' '.join(lines[line_number].split()).split("#")[0].strip()
	if "country_event =" in current_line or "country_event=" in current_line or "news_event =" in current_line or "news_event=" in current_line:
		if "{" not in current_line.split("_event")[1]:
			if not lines[line_number+1].split("#")[0].strip().strip('	').startswith("{"):
				return line_number
		result = is_event_declaration(lines, line_number, False, None)
		if result[0] != -1:
			return -1
		while len(lines)!=line_number:
			current_line = ' '.join(lines[line_number].split()).split("#")[0].strip()
			if "id =" in current_line:
				return line_number
			line_number = line_number + 1
	return -1

def check_for_events(file_path, output_file):
	t0 = time.time()

	events_existed = list()
	events_existed_trigger = list()
	events_called = list()
	num = 0
	
	for root, directories, filenames in walk(file_path):
		for filename in filenames:
			if ".txt" in filename:
				file = open_file(path.join(root, filename))
				lines = file.readlines()
				line_number = 0
				for line in lines:
					result = is_event_declaration(lines, line_number, True, output_file)
					add_id = result[0]
					if add_id != -1:
						events_existed.append(lines[add_id].split('=')[1].split("#")[0].strip())
						events_existed_trigger.append(result[1])
					line_number = line_number + 1
				
	for root, directories, filenames in walk(file_path):
		for filename in filenames:
			if ".txt" in filename:
				file = open_file(path.join(root, filename))
				lines = file.readlines()
				line_number = 0
				for line in lines:
					add_id = is_event_called(lines, line_number)
					if add_id != -1:
						if "id " not in lines[add_id]:
							event_title = ' '.join(lines[add_id].split()).split("_event =")[1].strip().split(' ')[0]
						else:
							event_title = ' '.join(lines[add_id].split()).split("id =")[1].strip().split(' ')[0].strip().split('}')[0].strip()
						if event_title not in events_called:
							events_called.append(event_title)
						if event_title not in events_existed:
							print("nonexistent event " + event_title + " called in line " + (add_id+1).__str__() + " in file " + filename)
							output_file.write("nonexistent event " + event_title + " called in line " + (add_id+1).__str__() + " in file " + filename + "\n")
					line_number = line_number + 1
	
	for event_existed in events_existed:
		if event_existed not in events_called:
			if events_existed_trigger[num]==True:
				print("unused event: " + event_existed)
				output_file.write("unused event: " + event_existed + "\n")
		num = num + 1
	
	t0 = time.time() - t0
	print("Time taken for events script: " + (t0*1000).__str__() + " ms")
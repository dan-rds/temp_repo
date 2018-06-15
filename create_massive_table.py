import yaml
import csv
import os

#Some of the data was given in kBs so I converted
def human_readable_size(size, decimal_places):
    for unit in ['','KB','MB','GB','TB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f}{unit}"


'''Here's where it gets a little ugly, instead of rewriting the scripts that scrape the
info from the systems, I just decided to parse it after it was created. To do that, I made a 
parse function to prcess each type of data separatly.'''

def parse_device(dict_dev):
	table_entry = {}

	table_entry["System"] = dict_dev["hostname"]
	table_entry['Type'] = dict_dev["type"]
	table_entry["Make"] = ''
	table_entry["Model"] = ''
	table_entry['S/N'] = ''
	table_entry['Capacity/Speed'] = ''
	table_entry['Other'] = dict_dev["IP"] 
	print(table_entry)
	return table_entry
def parse_gpu(dict_gpu, host_computer):
	table_entry = {}
	if(len(dict_gpu) < 3):
		return
	table_entry["System"] = host_computer
	table_entry['Type'] = "GPU"
	table_entry["Make"] = dict_gpu["-type"].split(' ')[0]
	table_entry["Model"] = dict_gpu["-type"].split(' ')[1]
	table_entry['S/N'] = dict_gpu["serial"]
	table_entry['Capacity/Speed'] = dict_gpu["memory"]
	table_entry['Other'] = ' '
	
	return table_entry
def parse_disks(dict_disks, host_computer):
	matrix = []
	if(len(dict_disks) < 3):
			return
	for i in dict_disks:
		disk = dict_disks[i]
		#print(disk)
		table_entry = {}

		table_entry["System"] = host_computer
		table_entry['Type'] = "Disk"

		table_entry["Make"] = disk['-device'].split(' ')[0]
		table_entry["Model"] = disk["-device"].split(' ')[1]
		table_entry['S/N'] = disk["-serial"]
		table_entry['Capacity/Speed'] = disk["-capacity"].split('[')[1].split(']')[0]
		table_entry['Other'] = ' '
		
		matrix.append(table_entry)

	return matrix
def parse_memory(dict_mem, host_computer):
	table_entry = {}

	table_entry["System"] = host_computer
	table_entry['Type'] = "Memory"
	table_entry["Make"] =' '
	table_entry["Model"] = ' '
	table_entry['S/N'] = ' '

	memory_amount_kb = int(dict_mem['-total'].split(' ')[0])
	table_entry['Capacity/Speed'] = human_readable_size(memory_amount_kb, 1)
	table_entry['Other'] = ' '
	
	return table_entry

def make_table(path, filename, csv_rows):
	host_computer = filename.split("d")[0]
	parent_dir = path.split("/")[1]
	yaml_file = open(path+'/'+filename, 'r')
	yaml_dict = yaml.load(yaml_file)
	#if 'temp' in filename:
		#for i in yaml_dict["disks"]:
			#print(yaml_dict['disks'][i])
			

	csv_rows.append(parse_device(yaml_dict["device"]))
	if "gpu" in yaml_dict:
		csv_rows.append(parse_gpu(yaml_dict["gpu"], host_computer))
	if "disks" in yaml_dict:
		disk_rows = parse_disks(yaml_dict['disks'], host_computer)
		for dis in disk_rows:
			csv_rows.append(dis)
	if 'memory' in yaml_dict:
		csv_rows.append(parse_memory(yaml_dict['memory'], host_computer))

	for entry in csv_rows:
		if entry :
			if isinstance(entry, list):
				for i in entry:
					i["Network"] = parent_dir
			else:
				entry["Network"] = parent_dir


csv_contents = [] #An array of dictionaries with key->column value->cell contents
column_names = ['Network', 'System','Type','Make', 'Model', 'Capacity/Speed', 'S/N', "Other"]

for root, dirs, files in os.walk("yaml"):
	for fi in files:
		print(root,dirs,files)
		csv_contents.append(make_table(root, fi, csv_contents))

csv_contents = [i for i in csv_contents if i is not None] #remove empty rows

with open('csv-to-html-table/data/some.csv', 'w') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames=column_names)
	writer.writeheader()
	writer.writerows(csv_contents)


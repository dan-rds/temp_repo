import yaml
import csv
import os


def str_process(st):
	st = st.upper()
	newst = st.replace("-", "")
	return newst

def gen_dict_extract(key, var):
    if hasattr(var,'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result
def _find( var, key):
	#a = gen_dict_extract(key, var)
	c = gen_dict_extract(key, var)
	a = list(c)
	#print(a)
	# if len(a) > 0:
	# 	return (a[0])
	# else:

	return  ("  ".join(a))
fieldnames=['System','Type','Make', 'Model', 'S/N']

def make_files(template):
	
	fileSt = open(template + 'data.txt', 'r')
	y = yaml.load(fileSt)
	print(_finditem(y,'type'))
	table_catagory = (list(y.keys()))
	#print(table_catagory)
	for cat in table_catagory:
		cols = []
		cols.append("System")

		for item in y[cat]:
			#print(item)
			cols.append(item)
		y[cat]["System"] = template
		#print(y)
		with open(cat + "_tab.csv", 'w+') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=cols)
			writer.writeheader()
			writer.writerow(y[cat])

def append_csvs(template):
	print(template)
	fileSt = open("yaml/" + template + 'data.txt', 'r')
	y = yaml.load(fileSt)

	row = {}
	row["System"] = (_find(y,'hostname'))
	row["Type"] = (_find(y["device"],'type'))
	row["Observatory"] = (_find(y,'observatory'))
	row["Memory"] = 0
	row["Disk"] = 0
	row["Gpu"] = 0
	row["Ip"] = (_find(y,'ip'))
	print(row)
	with open("full_hw_table.csv", 'w+') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			#writer.writeheader()
			writer.writerow(row)


def find_between(s, start, end):
  return (s.split(start))[1].split(end)[0]

fields=["System","Type","Make", "Model", "S/N", "Capacity/Speed", "Other"]

def read_device():
	final_rows = []

	with open("csv/device_tab.csv", 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		next(csvreader)

		for row in csvreader:
			print(row)
			rows =['', '', '', '', '','', '']
			rows[fields.index('System')] = row[0]
			rows[fields.index('Type')] = "Computer: " + row[2]
			rows[fields.index('Make')] = ' '
			rows[fields.index('Model')] = ' '
			rows[fields.index('S/N')] = ' '

			final_rows.append(rows)
		return final_rows
def read_disk():
	final_rows = []

	with open("csv/disks_tab.csv", 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		next(csvreader)

		for row in csvreader:
			rows =['', '', '', '', '','', '']
			rows[fields.index('System')] = row[0]
			rows[fields.index('Type')] = "Disk"
			rows[fields.index('Make')] = row[2].partition(' ')[0]
			rows[fields.index('Model')] = row[2].partition(' ')[2]
			rows[fields.index('S/N')] = row[4]
			rows[fields.index('Capacity/Speed')] = find_between(row[3], "[","]")
			final_rows.append(rows)
		return final_rows

#bls0,23,Intel(R) Xeon(R) CPU E5-2620 v3 @ 2.40GHz,6,False
def read_cpu():
	final_rows = []

	with open("csv/cpu_tab.csv", 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		next(csvreader)
		
		for row in csvreader:
			rows =['', '', '', '', '','', ' ']
			rows[fields.index('System')] = row[0]
			rows[fields.index('Type')] = "CPU"
			rows[fields.index('Make')] = row[2].partition(' ')[0]
			rows[fields.index('Model')] = row[2].partition(' ')[2].split(' @')[0]
			rows[fields.index('S/N')] = ''
			rows[fields.index('Capacity/Speed')] = row[2].partition(' ')[2].split('@ ')[1]
			rows[fields.index('Other')] = "Cores: " + row[3]
			final_rows.append(rows)
		for i in final_rows:
			print (i)

		return final_rows

def read_mem():
	final_rows = []

	with open("csv/memory_tab.csv", 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		next(csvreader)
		
		for row in csvreader:
			rows =['', '', '', '', '','', ' ']
			rows[fields.index('System')] = row[0]
			rows[fields.index('Type')] = "Memory"
			rows[fields.index('Make')] = ' '
			rows[fields.index('Model')] = ' '
			rows[fields.index('S/N')] = ' '
			rows[fields.index('Capacity/Speed')] = row[1]
		
			final_rows.append(rows)
		

		return final_rows

def read_gpu():
	final_rows = []

	with open("csv/gpu_tab.csv", 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		next(csvreader)
		
		for row in csvreader:
			rows =['', '', '', '', '','', ' ']
			# print(row)
			if(len(row) < 3):
				#print(row)
				final_rows.append([row[0], ''])
			else:
				rows[fields.index('System')] = row[0]
				rows[fields.index('Type')] = "GPU"
				rows[fields.index('Make')] = row[1].partition(' ')[0]
				rows[fields.index('Model')] = row[1].partition(' ')[2]
				rows[fields.index('Capacity/Speed')] = row[3]
				rows[fields.index('S/N')] = row[2]
			
				final_rows.append(rows)

		# for i in final_rows:
		# 	print (i)
		return final_rows





#print (devices)
field_names = fields
dev_itter = iter(read_device())
disk_itter = iter(read_disk())
cpu_itter = iter(read_cpu())
gpu_itter = iter(read_gpu())
mem_itter = iter(read_mem())

with open('some_table.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(field_names)
    writer.writerows(dev_itter)
    writer.writerows(cpu_itter)
    writer.writerows(gpu_itter)
    writer.writerows(mem_itter)
    writer.writerows(disk_itter)
'''
lines = [line.rstrip('\s+\n') for line in open('local_group')]

for l in lines:
	append_csvs(l)
with myFile:
    writer = csv.writer(myFile)

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerows(y)
  
c = csv.DictWriter(y)

fileOut = open('ex.csv', 'w')
fileOut.write(c)
print (y)
'''
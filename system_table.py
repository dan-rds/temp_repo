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
	with open("mega_hw_table.csv", 'w+') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			#writer.writeheader()
			writer.writerow(row)

lines = [line.rstrip('\s+\n') for line in open('local_group')]

for l in lines:
	append_csvs(l)




'''
with myFile:
    writer = csv.writer(myFile)

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerows(y)
  
c = csv.DictWriter(y)

fileOut = open('ex.csv', 'w')
fileOut.write(c)
print (y)
'''
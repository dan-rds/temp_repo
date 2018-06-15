from tinydb import TinyDB, Query
import os
import yaml

# def process_str(s):
# 	s.remove('-')

def make_info_gpu( d ):

	out = d['-type'].title()
	out += "Serial: " + str(d['serial'])
	out += "Memory: " + d['memory'].title()
	#print(out)

	return out
def make_info_disk( d ):
	#print(d)
	out = d['-device'].title()
	out += "Serial: " + str(d['-serial'])
	out += "Memory: " + d['-capacity'].split('[')[1].split(']')[0]
	#print("out  [" ,type(out).__name__, "]   :", out)
	return out
def create_node(path, filename):
	fileSt = open(path + '/' + filename, 'r')
	y = yaml.load(fileSt)
	for catagory in y: 

		if 'gpu' == catagory and y[catagory]['-type']:# or 'gpu' == catagory:
			y[catagory]['name'] = catagory.title()
			y[catagory]['vis'] = '1'
			y[catagory]['children'] = [{'name':y[catagory]['-type'], 'info': make_info_gpu(y[catagory])}]


			make_info_gpu(y[catagory])
			#print(type(y[catagory]['-type']))
		elif 'gpu' == catagory:
			y[catagory] = ''
		elif 'disks' == catagory:
			print("catagory  [" ,type(catagory).__name__, "]   :", catagory)
			y[catagory]['name'] = catagory.title()
			y[catagory]['children'] =  []
			y[catagory]['vis'] = '1'
			for i in y[catagory]:
				#print("y[catagory][i]  [" ,type(y[catagory][i]).__name__, "]   :", y)
				
				if type(y[catagory][i]) != str and type(y[catagory][i]) != list:
					print("i  [" ,type(i).__name__, "]   :", i)
					y[catagory]['children'].append({'name':'Bay: ' + str(i), 'info': make_info_disk(y[catagory][i])})
	for key in list(y.keys()):
		if type(y[key]) == str:
			del y[key]
	for catagory in y:
		print(type(y[catagory]))
		
		''''if 'disks' == catagory or catagory == 'gpu':
			
			child = []
			child_gpu = []
			info = []
			for item in y[catagory]:
				

				if '-type' == item and y[catagory][item]:#in y[catagory][item]:
					#name = y[catagory][] 
					#print(y[catagory][item])
					#for i in y[catagory][item]:
					#if y[catagory]['-type'] != None:
					#child =({'name':y[catagory]['-type'] })
					#print(y[catagory][item])
					#make_info(y[catagory])
					#make_info()
					
					child.append({'name':y[catagory][item]} )
					y[catagory]["name"] = "GPU"

					
				elif  catagory != 'gpu' and '-device' in y[catagory][item]:
					#for term in y[catagory][item]:
					name = y[catagory][item]['-device'] 
					#for i in y[catagory][item]:
					cap = "  " + y[catagory][item]['-capacity'].split('[')[1].split(']')[0]
					child.append({'name':y[catagory][item]['-device'] + cap } )
					info.append({'info': cap})
					#print(y[catagory][item])
					y[catagory]["name"] = 'Disk'

					
			if len(child) > 0:
				y[catagory]['children'] = child
			elif catagory == 'gpu':
				y[catagory] = ''
			if len(info) > 0:
				y[catagory]['info'] = info
			
	'''
	top_dev = y.pop('device')



	temp = []
	top_dev['children'] = []
	top_dev['vis'] = 1
	for i in y:
		temp_i = {}
		temp_i["name"] = i.title()
		temp_i.update(y[i])
		#print("y[i]  [" ,type(y[i]).__name__, "]   :", y[i])

		top_dev['children'].append(temp_i)

	top_dev['name'] = filename.split('d')[0]
	return top_dev
 


root = {}
root['name'] = " "
root['children'] = []
root['vis'] = 0

for path, subdirs, files in os.walk('yaml'):
	parent_dir = path.split('/')[-1]
	temp_node = {}
	if parent_dir != "yaml":
		temp_node["name"] = parent_dir.title()
		temp_node['vis'] = 1
		temp_node["children"] = []
		
		for name in files:
			temp_node["children"].append(create_node(path, name))
		root['children'].append(temp_node)
# for rootdir, dirs, files in os.walk("yaml"):
# 	print(dirs)
# 	for fi in files:
# 		root['children'].append(create_node('yaml/))


#root['children'].append(create_node('blc01data.txt'))

#print("root['children']  [" ,type(root['children']).__name__, "]   :", root['children'])
#root['children'].append(create_node('bls0data.txt'))


#print(top_dev)
# for a in y: 
# 	db.insert(y[a])



import json
with open('test.json', 'w') as outfile:
    json.dump(root, outfile)












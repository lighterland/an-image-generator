import os, random, shutil, json

def get_index():
	return len(os.listdir('result/images/'))

def create_folder():
	if os.path.exists('reshuffle'):
		shutil.rmtree('reshuffle')
	os.makedirs(f'reshuffle')
	folder = ['images', 'json']
	for name in folder:
		os.makedirs(f'reshuffle/{name}')

def update_json(index):
	json_file = open(f'reshuffle/json/{index}.json', 'r')
	f = json.load(json_file)
	json_file.close()
	f["name"] = f'#{index}'
	f["image"] = f'{index}.png'
	json_file = open(f'reshuffle/json/{index}.json', 'w')
	json.dump(f, json_file, indent=4)
	json_file.close()

def reshuffle():
	create_folder()
	index_list = list(range(1,get_index()+1))
	for i in range(1,get_index()+1):
		index = random.choice(index_list)
		shutil.copy(f'result/images/{i}.png', f'reshuffle/images/{index}.png')
		shutil.copy(f'result/json/{i}.json', f'reshuffle/json/{index}.json')
		update_json(index)
		index_list.remove(index)
		print(i)

if __name__ == '__main__':
	reshuffle()
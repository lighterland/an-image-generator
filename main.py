import os, random, json, shutil, os.path
from PIL import Image
import pandas as pd
import setting


def dna_existCount(add):
	if add:
		try:
			count = int(open(f'temp/dnaExCount.txt').read())
		except:
			count = 0
			with open('temp/dnaExCount.txt','w') as f:
				f.write(str(count))
		count += 1
		print(count)
		if count > 100 and setting.useRarity_adj: #100 attempts
			for rarity_adj in open('rarity_adj.txt').read().splitlines():
				if not os.path.exists('temp/layers/'+rarity_adj.partition(' : ')[0]+'.txt'):
					with open('temp/layers/'+rarity_adj.partition(' : ')[0]+'.txt','w') as f:
						f.write(rarity_adj.partition(' : ')[2])
					f.close()
			with open('temp/rarity_adj_stat.txt','w') as stat:
				stat.write('used')
			count = 0

	with open('temp/dnaExCount.txt','w') as f:
		f.write(str(count))

	return f.close()


def dir_check():
	if os.path.exists('result'):
		shutil.rmtree('result')
	os.makedirs(f'result')	
	folder = ['images', 'json']
	for name in folder:
		os.makedirs(f'result/{name}')
	if os.path.exists('temp'):
		shutil.rmtree('temp')
	os.makedirs(f'temp/dna')
	for layer in os.listdir('layers'):
		os.makedirs(f'temp/layers/{layer}')
		for file in os.listdir(f'layers/{layer}'):
			with open(f'temp/layers/{layer}/{file}.txt','w') as f:
				for quantity in open('rarity.txt').read().splitlines():
					if f'{layer}/'+file == quantity.partition(' : ')[0]:
						q = quantity.partition(' : ')[2]
				f.write(q)
			f.close()
	return print('folder created!')

def get_combination():
	layers = open('layerorder.txt').read().splitlines()
	combination = []
	for part in layers:
		item = random.choice(os.listdir(f'temp/layers/{part}')).partition('.txt')[0]
		combination.append(f'{part}/{item}')
	return combination

def check_combination():
	confirm = True
	temp_dna = open('temp/dna/temp_dna.txt').read()
	
	if setting.useCondition:
		confirm = setting.valid_condition(temp_dna)

	for dna in os.listdir('temp/dna'):
		if dna != 'temp_dna.txt':
			with open('temp/dna/'+dna) as f:
				if temp_dna == f.read():
					confirm = False
					f.close()
					print('dna exists!')
					dna_existCount(True)

	return confirm

def create_image(combination, index):
	res = setting.imageSize
	imgres = (res, res)
	final = Image.new('RGBA', imgres)
	for part in combination:
		if setting.imageSmooth:
			imglayer = Image.open('layers/'+part).convert('RGBA').resize((imgres), Image.BICUBIC)
		else:
			imglayer = Image.open('layers/'+part).convert('RGBA').resize((imgres), Image.NEAREST)
		final = Image.alpha_composite(final,imglayer)
	final.save(f'result/images/{index}.png')
	return print(f'{index}.png created!')

def defaultdict(index):
	return {
		"name": f'#{index}',
		"description": "",
		"image": f"{index}.png",
	}

def get_attribute(key,value):
	return {
		"trait_type": key,
		"value": value
	}

def export_metadata(combination, index, all_json, all_csv):
	meta_json = defaultdict(index)
	meta_csv = defaultdict(index)
	meta_json["attributes"] = []

	for key in combination:
		key = key.partition('.png')[0]
		meta_json["attributes"].append(get_attribute(key.partition('/')[0], key.partition('/')[2]))
		meta_csv[key.partition('/')[0]] = key.partition('/')[2]

	with open(f'result/json/{index}.json', 'w') as outfile:
		json.dump(meta_json, outfile, indent=4)

	all_json[index] = meta_json
	all_csv[index] = meta_csv

	return all_json, all_csv

def export_all_metadata(all_json, all_csv):
	with open('result/all.json', 'w') as outfile:
		json.dump(all_json, outfile, indent=4)
	dataFrame = pd.read_json(json.dumps(all_csv),orient='index')
	dataFrame.to_csv('result/all.csv', index=False)

def check_rarity(combination):
	for layer in os.listdir('temp/layers'):
		for item in os.listdir(f'temp/layers/{layer}'):
			q = int(open(f'temp/layers/{layer}/{item}').read())
			for path in combination:
				if f'{layer}/'+item.partition('.txt')[0] == path:
					q -= 1
			with open(f'temp/layers/{layer}/{item}', 'w') as f:
				f.write(str(q))
			f.close()
			if q < 1:
				os.remove(f'temp/layers/{layer}/{item}')
				print(item,'is removed from the availability traits!')

def generate():
	index = 1
	all_json = {}
	all_csv = {}
	dir_check()
	while True:
		while True:
			combination = get_combination()
			with open('temp/dna/temp_dna.txt', 'w') as dna:
				for part in combination:
					dna.write(part+'\n')
			if check_combination():
				os.rename('temp/dna/temp_dna.txt', f'temp/dna/{index}.txt')
				check_rarity(combination)
				break
			dna.close()
			dna_existCount(True) # edit
			
		create_image(combination, index)
		all_json, all_csv = export_metadata(combination, index, all_json, all_csv)
		index += 1
		if len(os.listdir('temp/layers/background')) < 1:
			break

	export_all_metadata(all_json, all_csv)

if __name__ == '__main__':
	generate()

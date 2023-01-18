import os, shutil
from PIL import Image

def create_folder():
	if os.path.exists('resize'):
		shutil.rmtree('resize')
	os.makedirs(f'resize')
	return print("folder created!")

def goResize():
	create_folder()
	for img in os.listdir('reshuffle/images/'):
		f = Image.open(f'reshuffle/images/{img}')
		f = f.resize((256,256),Image.ANTIALIAS)
		f.save(f'resize/{img}',optimize=True,quality=10)
		print(img)

if __name__ == '__main__':
	goResize()
import os

for path in os.listdir('layers'):
	for file in os.listdir(f'layers/{path}'):
		print(f"{path}/{file} : ")
	print()
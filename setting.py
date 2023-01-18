

imageSize = 512
imageSmooth = True
useCondition = True
useRarity_adj = True


def condition(exList,temp_dna):

	ex_trait_list = exList
	count = 0

	for trait in temp_dna.split('\n'):
		if trait in ex_trait_list:
			count += 1

	return True if count<2 else False

def valid_condition(temp_dna):
	condition_1 = condition([
		'background/Amethyst.png',
		'eyes/Angry.png'
	], temp_dna)

	condition_2 = condition([
		'hand/BlackGlove.png',
		'mouth/Angry.png'
	], temp_dna)

	if not (condition_1 and condition_2): # edit
		print('invalid combination')

	return True if condition_1 and condition_2 else False # edit


from nltk.corpus import stopwords

from nltk.stem import PorterStemmer
import numpy as np
import json
import re
stemmer=PorterStemmer()
stop = set(stopwords.words('english'))


#import Levenshtein

project_name = "TasteTest"
net_ids = "Robert Li: rl597, Seraphina Lee: el542, Frank Li: fl338, Steven Ye: xy93"


#######populating flavor values
from annotated import annotatedDict
import units
import ml_model




with open('aggreg.json') as json_data:
	raw = json.load(json_data)[:3000]
with open('all_ingrs.json') as json_data:
	all_ingrs = json.load(json_data)

ingr_inv_index = {}
all_ingrs_lst = []
i=0
for ingr in all_ingrs:
	all_ingrs_lst.append(ingr)
	ingr_inv_index[ingr] = i
	i += 1


flav_mat = np.zeros((len(raw), 5))
flav_norms = np.zeros(len(raw))
ingr_mat = np.zeros((len(raw), len(all_ingrs)))

#ml -- getting flavor profiles for each of the topics we get by topic-modelling the ingredients
topic_profs = np.load('topic_profs.npy')
#topic_profs = [ml_model.flavors_to_topics(i, ml_model.model, ml_model.feature_names) for i in range(ml_model.n_topic)]
model_components = np.load('model_components.npy')
cv_vocabulary = np.load('cv_vocabulary.npy').item()


def ingr_to_topic_prof(ingr, model_components, topic_profs):
	return topic_profs[np.argmax(model_components[:, cv_vocabulary[ingr]])]

#######
#####################################################################################################################
#Helpers for labels that are pre built in

def isLactoOvoVegatarian(dish):
	return 'lacto ovo vegetarian' in dish['diets']
def isGlutenFree(dish):
	return dish['glutenFree']

def isVegetarian(dish):
	return dish['vegetarian']

def isKetogenic(dish):
	return dish['ketogenic']

def isDairyFree(dish):
	return dish['dairyFree']

def isVegan(dish):
	return dish['vegan']

def isPescatarian(dish):
	return 'pescatarian' in dish['diets']

#Major Food Groups
# NOTE: that these labels should only be included for excluding recipes. Obviously, you won't find a recipe that uses all dairy products.

dairy = set(['milk', 'butter', 'cheese', 'cream', 'curds', 'custard', 'half-and-half', 'pudding', 'sour cream',
             'condensed milk', 'yogurt', 'milk chocolate', 'margarine', 'nougat'])

shellfish = set(['crawfish', 'clams', 'cuttlefish', 'mussels', 'octopus', 'oysters', 'sea urchin', 'scallops',
                 'snails', 'escargot', 'squid', 'calamari', 'krill', 'shrimp', 'scampi', 'prawns','lobster',
                 'abalone', 'geoduck', 'crayfish', 'crab'])

fish = set(['anchovies', 'anchovy', 'bass', 'catfish', 'cod', 'flounder', 'grouper', 'haddock', 'hake', 'halibut', 'herring', 'mahi mahi',
            'perch', 'pike', 'pollock', 'salmon', 'lox', 'scrod', 'sole', 'snapper', 'swordfish', 'red snapper',
            'tilapia', 'trout', 'tuna', 'fish oil', 'caesar dressing', 'imitation crab', 'worcestershire sauce', 'barbecue sauce'])

treeNuts = set(['almond', 'almond', 'almond butter', 'beechnut', 'brazil nut', 'butternut', 'cashew', 'chestnut', 'chinquapin nut',
                'coconut', 'hazelnut', 'filbert', 'gianduja', 'nutella', 'ginkgo nut', 'hickory nut', 'litchi', 'lichee', 'lychee',
                'macadamia nut', 'marzipan', 'almond paste', 'nangai nut', 'nut meal', 'nut meat', 'almond milk', 'cashew milk',
                'walnut oil', 'almond oil', 'pecan', 'pesto', 'pine nut', 'praline', 'pistachio', 'walnut','argan oil'])

egg = set(['abumin', 'albumen', 'egg', 'egg white', 'egg yolk', 'eggnog', 'mayonnaise', 'meringue', 'surimi', 'ovalbumin'])

peanuts = set(['peanut', 'peanut butter', 'peanut oil', 'goobers','lupin', 'monkey nuts', 'peanut flour', 'lupine'])

wheat = set(['bread crumbs', 'bulgur', 'cereal extract', 'club wheat', 'couscous', 'cracker meal', 'cracker meal',
             'durum', 'einkorn', 'emmer', 'farina', 'flour', 'matzoh', 'matzo', 'matzah', 'matza', 'wheat germ oil',
             'wheat grass', 'ale', 'beer'])

soy = set(['soy oil', 'edamame', 'miso', 'shoyu', 'soya', 'soy sauce', 'tamari', 'tempeh', 'tofu', 'soybean'])

sesame = set(['benne', 'benne seed', 'benniseed', 'gingelly', 'gingelly oil', 'sesame salt', 'gomasio', 'halvah', 'sesame flour', 'sesame oil', 'sesame paste',
              'sesame seed', 'sesamol', 'sesamum indicum', 'sim sim', 'tahini', 'tahina', 'tehina', 'til'])

pork = set(['bacon', 'chorizo', 'ground pork', 'pork belly', 'panchetta', 'prosciutto', 'ham',
            'serrano', 'spam', 'liverwurst', 'mortadella', 'blood sausage', 'spare ribs', 'pork tenderloin',
           'pork shoulder'])

wild_meat = set(['rabbit','boar','elk','buffalo','bison','frog'])

beef = set(['beef tartar', 'beef', 'steak', 'ribeye', 'corned beef', 'pastrami', 'roast beef',
            'sirloin', 'tenderloin', 'filet mignon', 'round', 'brisket', 'prime rib', 'short rib'
            ,'chuck roast', 'chuck steak', 'beef shank', 'skirt', 'skirt steak', 'strip steak'])

alcohol = set(['wine', 'brandy', 'gin', 'beer', 'lager', 'cognac', 'rum', 'vodka', 'wiskey', 'scotch',
               'tequila', 'moon shine', 'red wine', 'white wine', 'rose', 'absinthe', 'sake'
               , 'soju', 'rice wine', 'liquer','spirit', 'bourbon'])

kosher = wild_meat.intersection(pork.intersection(shellfish))



restriction_dict = {"alcohol" : alcohol,
					"beef" : beef,
					"dairy" : dairy,
					"egg" : egg,
					"fish" : fish,
					#"gluten" : ,
					"halal" : pork | alcohol,
					#"ketogenic" :,
					#"kosher" :,
					#"lactoovo": ,
					"pork" : pork,
					"peanut" : peanuts,
					#"pescatarian": ,
					"sesame" : sesame,
					"shellfish" : shellfish,
					"soy" : soy,
					"treenuts" : treeNuts,
					#"vegan" :,
					#"vegetarian" :,
					"wheat" : wheat}

def tokenize_ingredients (ingredients, stop_words):
	List = []
	for i in ingredients:
		tokens = re.findall("[^\s]+", i)
		#print (tokens)
		for j in tokens:
			if j not in stop_words:
				List.append (j)
	return set(List)

""" get_stems takes in a list of ingredients and stems them
	using PorterStemmer
"""
def get_stems(ingredients):
	ingredientsSet = set ()
	for w in ingredients:
		#w = w.replace (" ", "")
		ingredientsSet.add (stemmer.stem (w.lower()))
	#print (ingredientsSet)
	return ingredientsSet


def is_free_of(dish, restriction_set):
	recipe_ingredients = [ingr['name'] for ingr in dish['extendedIngredients']]
	tokened_ingredients = tokenize_ingredients (recipe_ingredients, stop)
	ingr = get_stems(tokened_ingredients)
	for elt in ingr:
		if elt in restriction_set:
			return False
	return True


def is_kosher(dish):
	recipe_ingredients = [ingr['name'] for ingr in dish['extendedIngredients']]
	tokened_ingredients = tokenize_ingredients (recipe_ingredients, stop)
	ingr = get_stems(tokened_ingredients)
	beef_check = False
	for elt in ingr:
		if elt in beef:
			beef_check = True
		if elt in kosher:
			 return False
	return (not beef_check or is_free_of(dish, dairy))
	#if beef_check == true and is_free_of(dish, dairy) == false:
	#	return false
	#return true

def exclude_recipe_restriction (restriction_strings):
	filter_vec = np.zeros((len(raw), 1))
	rest_free = ['gluten', 'dairy']
	other_rec_flag = ['vegetarian', 'ketogenic', 'vegan']
	for i in range(len(raw)):
		dish = raw[i]
		include_flag = True
		for restriction in restriction_strings:
			if restriction in rest_free:
				include_flag = include_flag and dish[restriction+'Free']
			elif restriction in other_rec_flag:
				include_flag = include_flag and dish[restriction]
			elif restriction == 'lactoovo':
				include_flag = include_flag and ('lacto ovo vegetarian' in dish['diets'])
			elif restriction == 'pescatarian':
				include_flag = include_flag and ('pescatarian' in dish['diets'])
			elif restriction == 'kosher':
				include_flag = include_flag and is_kosher(dish)
			else:
				include_flag = include_flag and is_free_of(dish, restriction_dict[restriction])
		filter_vec[i] = int(include_flag)
	return filter_vec







########################################################################################
#precomputation script:







#makes the matrices flav_mat (recipe x flavor matrix that has the flavor profiles for each recipe)
# flav_norms (vector with the norms of each row of the flav_mat)
# ingr_mat (recipe x ingredient matrix that has 1 if the recipe contains that ingredient)
for i in range(len(raw)):
	flav_prof = np.array([0,0,0,0,0])
	for j in range(len(raw[i]['extendedIngredients'])):
		ingr = raw[i]['extendedIngredients'][j]
		amount = ingr['amount']
		unit = ingr['unit'] #need to map them to proportional weights later (e.g. 1 lb = 16 oz)
		name = ingr['name']
		if name in annotatedDict:
			flav_lst = [annotatedDict[name]['sweet'], annotatedDict[name]['salty'],annotatedDict[name]['sour'], annotatedDict[name]['bitter'], annotatedDict[name]['umami']]
			flav_prof = np.add(flav_prof, (amount*units.unit_weights(unit))*np.array(flav_lst))
		else:
			###call ml_model and get topic-estimated flavor prof
			flav_prof = np.add(flav_prof, ingr_to_topic_prof(name, model_components, topic_profs))
		ingr_mat[i,ingr_inv_index[name]] = 1
	if np.max(flav_prof) == 0:
		flav_prof = np.array([1,1,1,1,1])
	flav_mat[i,:] = 10*((1.0*flav_prof)/np.max(flav_prof))
	flav_norms[i] = np.linalg.norm(flav_mat[i])




restriction_strs = ["alcohol",
					"beef",
					"dairy",
					"egg",
					"fish",
					"gluten",
					"halal",
					"ketogenic",
					"kosher",
					"lactoovo",
					"pork",
					"peanut",
					"pescatarian",
					"sesame",
					"shellfish",
					"soy",
					"treenuts",
					"vegan",
					"vegetarian",
					"wheat"]

np.save('flav_mat', flav_mat)
np.save('flav_norms', flav_norms)
for res in restriction_strs:
	np.save(res, exclude_recipe_restriction([res]))

















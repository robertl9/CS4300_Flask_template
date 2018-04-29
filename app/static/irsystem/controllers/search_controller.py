from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from scraper import *

from nltk.corpus import stopwords

from nltk.stem import PorterStemmer
import re
stemmer=PorterStemmer()
stop = set(stopwords.words('english'))


import json

#import Levenshtein

project_name = "TasteTest"
net_ids = "Robert Li: rl597, Seraphina Lee: el542, Frank Li: fl338, Steven Ye: xy93"


#######populating flavor values
import re
from annotated import annotatedDict
import units
#import ml_model

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


#######

@irsystem.route('/', methods=['GET'])
def search():
	try:
		print(request.args)
		query = request.args.get('search')
		sweet = int(request.args.get('sweet'))
		salty = int(request.args.get('salty'))
		sour = int(request.args.get('sour'))
		bitter = int(request.args.get('bitter'))
		umami = int(request.args.get('umami'))
		flavors = np.array([sweet, salty, sour, bitter, umami])
		if np.max(flavors) == 0:
			flav_prof = np.array([1,1,1,1,1])
		query = [(pair.split('|')[0], bool(int(pair.split('|')[1]))) for pair in query.split(',')[:-1]]
		data = [raw[i] for i in cos_sim_flavor(flavors, filter_clude_ingr(query))]
		output_message = "Your search returned " + str(len(data)) + " results:"
	except TypeError:
		data = []
		query = []
		output_message = ''
		sweet = salty = sour = bitter = umami = 0
	return render_template('search.html', name=project_name,
		                                  netid=net_ids,
		                                  ingrs=all_ingrs_lst,
		                                  data=data,
		                                  query=query,
		                                  sweet=sweet,
		                                  salty=salty,
		                                  sour=sour,
		                                  bitter=bitter,
		                                  umami=umami,
		                                  output_message=output_message)


#precompute flavor matrix (recipe x flavor) + docnorms (recipe x norm)
#takes in np array of np array containing flavor profile, and returns a ranked list of indices
def cos_sim_flavor(flavors, mat):
	lst = np.dot(mat,flavors)
	scores = np.divide(lst, 1.0*flav_norms)
	first_zero_elt = np.count_nonzero(scores)
	return np.ndarray.tolist(np.argsort(-scores))[:first_zero_elt]

#def edit_distance (ingredient, database_res):
#	return Levenshtein.distance(ingredient.lower(), database_res.lower())

#def edit_distance_search (query, ingredients):
#	List = []
#	for i in ingredients:
#		tupl = (edit_distance(query, i["text"]),i)
#		List.append(tupl)
#	sortedList = sorted(List, key=lambda tup: tup[0])
#	return sortedList

#returns list of strings which contain substring. Unoptimized
def substr_match (query, list_of_words):
	length = len(query)
	List = []
	for i in list_of_words:
		if i[:length] == query:
			List.append(i)
	return List

""" tokenize_ingredients takes in a list of ingredients and tokenizes them
	by the spaces and returns a set of the tokenized ingredients, excluding
	stop words.
	Example: ["zest of lemon", "zest of lime"] would return
	["zest", "lemon", "lime"]
"""
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

""" exclude_recipe takes in a list tuples (ingredients, bool) (where bool = true if include, false if exclude)
 and the recipe_ingredients and returns a boolean vector representing
 whether the excluded / included ingredients are found in the recipe.
"""
def exclude_recipe (ingredients_tuples):
	filter_vec = np.zeros((len(raw), 1))
	for i in range(len(raw)):
		recipe_ingredients = [ingr['name'] for ingr in raw[i]['extendedIngredients']]
		excluded_ingredients = [ingr for (ingr, incl) in ingredients_tuples if not incl]
		included_ingredients = [ingr for (ingr, incl) in ingredients_tuples if incl]
		new_exclu = tokenize_ingredients (excluded_ingredients, stop)
		#new_inclu = tokenize_ingredients(included_ingredients, stop)
		new_recipe = tokenize_ingredients (recipe_ingredients, stop)
		excluded_ingredients_set = get_stems (new_exclu)
		included_ingredients_set = get_stems(included_ingredients)
		recipe_ingredients_set = get_stems (new_recipe)
		inter_exclu = excluded_ingredients_set.intersection (recipe_ingredients_set)
		inter_inclu = included_ingredients_set.intersection (recipe_ingredients_set)

		### we want inter_exclu to be empty and inter_inclu to be nonempty
		if len(included_ingredients)==0:
			filter_vec[i] = (len(inter_exclu) == 0)
		else:
			filter_vec[i] = (len(inter_exclu) == 0 and len(inter_inclu) > 0)
	return filter_vec


#return flavor matrix that has 0's for recipes that include (if incl) or exclude (if not incl) the query ingredient
def filter_clude_ingr(query):
	filtered_flav_mat = np.copy(flav_mat)
	filter_vec = exclude_recipe(query)
	filtered_flav_mat = filter_vec*filtered_flav_mat
	return filtered_flav_mat


#return dish with new field rating containing social feedback scrapped from source url
def add_rating(dish):
	dish["rating"] = parser(dish["sourceUrl"])
	return dish


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

dairy = Set(['milk', 'butter', 'cheese', 'cream', 'curds', 'custard', 'half-and-half', 'pudding', 'sour cream',
             'condensed milk', 'yogurt', 'milk chocolate', 'margarine', 'nougat'])

shellfish = Set(['crawfish', 'clams', 'cuttlefish', 'mussels', 'octopus', 'oysters', 'sea urchin', 'scallops',
                 'snails', 'escargot', 'squid', 'calamari', 'krill', 'shrimp', 'scampi', 'prawns','lobster',
                 'abalone', 'geoduck', 'crayfish', 'crab'])

fish = Set(['anchovies', 'anchovy', 'bass', 'catfish', 'cod', 'flounder', 'grouper', 'haddock', 'hake', 'halibut', 'herring', 'mahi mahi',
            'perch', 'pike', 'pollock', 'salmon', 'lox', 'scrod', 'sole', 'snapper', 'swordfish', 'red snapper',
            'tilapia', 'trout', 'tuna', 'fish oil', 'caesar dressing', 'imitation crab', 'worcestershire sauce', 'barbecue sauce'])

treeNuts = Set(['almond', 'almond', 'almond butter', 'beechnut', 'brazil nut', 'butternut', 'cashew', 'chestnut', 'chinquapin nut',
                'coconut', 'hazelnut', 'filbert', 'gianduja', 'nutella', 'ginkgo nut', 'hickory nut', 'litchi', 'lichee', 'lychee',
                'macadamia nut', 'marzipan', 'almond paste', 'nangai nut', 'nut meal', 'nut meat', 'almond milk', 'cashew milk',
                'walnut oil', 'almond oil', 'pecan', 'pesto', 'pine nut', 'praline', 'pistachio', 'walnut','argan oil'])

egg = Set(['abumin', 'albumen', 'egg', 'egg white', 'egg yolk', 'eggnog', 'mayonnaise', 'meringue', 'surimi', 'ovalbumin'])

peanuts = Set(['peanut', 'peanut butter', 'peanut oil', 'goobers','lupin', 'monkey nuts', 'peanut flour', 'lupine'])

wheat = Set(['bread crumbs', 'bulgur', 'cereal extract', 'club wheat', 'couscous', 'cracker meal', 'cracker meal',
             'durum', 'einkorn', 'emmer', 'farina', 'flour', 'matzoh', 'matzo', 'matzah', 'matza', 'wheat germ oil',
             'wheat grass', 'ale', 'beer'])

soy = Set(['soy oil', 'edamame', 'miso', 'shoyu', 'soya', 'soy sauce', 'tamari', 'tempeh', 'tofu', 'soybean'])

sesame = Set(['benne', 'benne seed', 'benniseed', 'gingelly', 'gingelly oil', 'sesame salt', 'gomasio', 'halvah', 'sesame flour', 'sesame oil', 'sesame paste',
              'sesame seed', 'sesamol', 'sesamum indicum', 'sim sim', 'tahini', 'tahina', 'tehina', 'til'])

pork = Set(['bacon', 'chorizo', 'ground pork', 'pork belly', 'panchetta', 'prosciutto', 'ham',
            'serrano', 'spam', 'liverwurst', 'mortadella', 'blood sausage', 'spare ribs', 'pork tenderloin',
           'pork shoulder'])

wild_meat = Set(['rabbit','boar','elk','buffalo','bison','frog'])

beef = Set(['beef tartar', 'beef', 'steak', 'ribeye', 'corned beef', 'pastrami', 'roast beef',
            'sirloin', 'tenderloin', 'filet mignon', 'round', 'brisket', 'prime rib', 'short rib'
            ,'chuck roast', 'chuck steak', 'beef shank', 'skirt', 'skirt steak', 'strip steak'])

alcohol = Set(['wine', 'brandy', 'gin', 'beer', 'lager', 'cognac', 'rum', 'vodka', 'wiskey', 'scotch',
               'tequila', 'moon shine', 'red wine', 'white wine', 'rose', 'absinthe', 'sake'
               , 'soju', 'rice wine', 'liquer','spirit'])

def is_halal(dish):
	recipe_ingredients = [ingr['name'] for ingr in dish['extendedIngredients']]
	ingr = get_stems(recipe_ingredients)
	for elt in ingr:
		if elt in pork:
			return false
		if elt in alcohol:
			return false
	return true

def isTreeNutFree(dish):
	recipe_ingredients = [ingr['name'] for ingr in dish['extendedIngredients']]
	ingr = get_stems(recipe_ingredients)
	for elt in ingr:
		if elt in treeNuts:
			return false
	return true

def is_kosher(dish):
	recipe_ingredients = [ingr['name'] for ingr in dish['extendedIngredients']]
	ingr = get_stems(recipe_ingredients)
	beef_check = false
	for elt in ingr:
		if elt in beef:
			beef_check = true
		if elt in kosher:
			 return false
	if beef_check == true and isDairyFree(dish) == false:
		return false
	return true

def isShellFishFree(dish):
	recipe_ingredients = [ingr['name'] for ingr in dish['extendedIngredients']]
	ingr = get_stems(recipe_ingredients)
	for elt in ingr:
		if elt in shellfish:
			return false
	return true

def isFishFree(dish):
	recipe_ingredients = [ingr['name'] for ingr in dish['extendedIngredients']]
	ingr = get_stems(recipe_ingredients)
	for elt in ingr:
		if elt in fish:
			return false
	return true

def isEggFree(dish):
	recipe_ingredients = [ingr['name'] for ingr in dish['extendedIngredients']]
	ingr = get_stems(recipe_ingredients)
	for elt in ingr:
		if elt in egg:
			return false
	return true

def isPeanutFree(dish):
	recipe_ingredients = [ingr['name'] for ingr in dish['extendedIngredients']]
	ingr = get_stems(recipe_ingredients)
	for elt in ingr:
		if elt in peanuts:
			return false
	return true

def isWheatFree(dish):
	recipe_ingredients = [ingr['name'] for ingr in dish['extendedIngredients']]
	ingr = get_stems(recipe_ingredients)
	for elt in ingr:
		if elt in wheat:
			return false
	return true

def isSoyFree(dish):
	recipe_ingredients = [ingr['name'] for ingr in dish['extendedIngredients']]
	ingr = get_stems(recipe_ingredients)
	for elt in ingr:
		if elt in soy:
			return false
	return true

def isSesameFree(dish):
	recipe_ingredients = [ingr['name'] for ingr in dish['extendedIngredients']]
	ingr = get_stems(recipe_ingredients)
	for elt in ingr:
		if elt in sesame:
			return false
	return true

def isPorkFree(dish):
	recipe_ingredients = [ingr['name'] for ingr in dish['extendedIngredients']]
	ingr = get_stems(recipe_ingredients)
	for elt in ingr:
		if elt in pork:
			return false
	return true

def isBeefFree(dish):
	recipe_ingredients = [ingr['name'] for ingr in dish['extendedIngredients']]
	ingr = get_stems(recipe_ingredients)
	for elt in ingr:
		if elt in beef:
			return false
	return true

def isAlcoholFree(dish):
	recipe_ingredients = [ingr['name'] for ingr in dish['extendedIngredients']]
	ingr = get_stems(recipe_ingredients)
	for elt in ingr:
		if elt in alcohol:
			return false
	return true

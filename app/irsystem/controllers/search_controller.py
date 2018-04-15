from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import json
import Levenshtein

project_name = "TasteTest"
net_ids = "Robert Li: rl597, Seraphina Lee: el542, Frank Li: fl338, Steven Ye: xy93"


#######populating flavor values
import re
from annotated import annotated

with open('aggreg.json') as json_data:
	raw = json.load(json_data)
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

for i in range(len(raw)):
	flav_prof = np.array([0,0,0,0,0])
	for j in range(len(raw[i]['extendedIngredients'])):
		ingr = raw[i]['extendedIngredients'][j]
		amount = ingr['amount']
		unit = ingr['unit'] #need to map them to proportional weights later (e.g. 1 lb = 16 oz)
		name = ingr['name']
		if name in annotated:
			flav_lst = [annotated[name]['sweet'], annotated[name]['salty'],annotated[name]['sour'], annotated[name]['bitter'], annotated[name]['umami']]
			flav_prof = np.add(flav_prof, amount*np.array(flav_lst))
		ingr_mat[i,ingr_inv_index[name]] = 1
	if np.max(flav_prof) == 0:
		flav_prof = np.array([1,1,1,1,1])
	flav_mat[i,:] = 10*(flav_prof/np.max(flav_prof))
	flav_norms[i] = np.linalg.norm(flav_mat[i])


		

#######

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	sweet = request.args.get('sweet')
	salty = request.args.get('salty')
	sour = request.args.get('sour')
	bitter = request.args.get('bitter')
	umami = request.args.get('umami')
	if not query:
		data = []
		output_message = ''
	else:
		flavors = np.array([int(sweet), int(salty), int(sour), int(bitter), int(umami)])
		data = [raw[i] for i in cos_sim_flavor(flavors, filter_include_ingr(query))]
		output_message = "Your search for \"" + query + "\" returned " + str(len(data)) + " results:"
	return render_template('search.html', name=project_name, netid=net_ids, output_message=output_message, data=data, ingrs=all_ingrs_lst)


#precompute flavor matrix (recipe x flavor) + docnorms (recipe x norm)
#takes in np array of np array containing flavor profile, and returns a ranked list of indices
def cos_sim_flavor(flavors, mat):
	lst = np.dot(mat,flavors)
	scores = np.divide(lst, flav_norms)
	return np.ndarray.tolist(np.argsort(-scores))

def edit_distance (ingredient, database_res):
	return Levenshtein.distance(ingredient.lower(), database_res.lower())

def edit_distance_search (query, ingredients):
	List = []
	for i in ingredients:
		tupl = (edit_distance(query, i["text"]),i)
		List.append(tupl)
	sortedList = sorted(List, key=lambda tup: tup[0])
	return sortedList

#returns list of strings which contain substring. Unoptimized
def substr_match (query, list_of_words):
	length = len(query)
	List = []
	for i in list_of_words:
		if i[:length] == query:
			List.append(i)
	return List 

#return flavor matrix that has 0's for recipes that don't include the query ingredient
def filter_include_ingr(query):
	if query in all_ingrs_lst:
		filtered_flav_mat = np.array(flav_mat.shape)
		filtered_flav_mat = ingr_mat[:, ingr_inv_index[query]].reshape(len(raw), 1)*flav_mat
		return filtered_flav_mat
	else:
		return flav_mat










from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import json
import Levenshtein

project_name = "TasteTest"
net_ids = "Robert Li: rl597, Seraphina Lee: el542, Frank Li: fl338, Steven Ye: xy93"


#######delete later, just populating test flavor values
import re

with open('aggreg.json') as json_data:
	raw = json.load(json_data)
flav_mat = np.zeros((len(raw), 5))
flav_norms = np.zeros(len(raw))
for i in range(len(raw)):
	flav_mat[i] = [i%10]*5
	flav_norms[i] = np.linalg.norm(flav_mat[i])
#######

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	sweet = request.args.get('sweet')
	salty = request.args.get('salty')
	sour = request.args.get('sour')
	bitter = request.args.get('bitter')
	savory = request.args.get('savory')
	if not query:
		data = []
		output_message = ''
	else:
		##query should be of form '2,5,7,2,9' (5 integers separated out by commas) for now
		output_message = "Your search: " + query
		# flav = re.findall('[0-9]+', query)
		# if len(flav) != 5:
		# 	data = ["query should be of form e.g. '2,5,7,2,9'"]
		flavors = np.array([int(sweet), int(salty), int(sour), int(bitter), int(savory)])
		data = [raw[i]['title'] for i in cos_sim_flavor(flavors)]
	return render_template('search.html', name=project_name, netid=net_ids, output_message=output_message, data=data)


#precompute flavor matrix (recipe x flavor) + docnorms (recipe x norm)
#takes in np array of np array containing flavor profile, and returns a ranked list of indices
def cos_sim_flavor(flavors):
	lst = np.dot(flav_mat,flavors)
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
		if i[:length] = query:
			List.append(i)
	return List 

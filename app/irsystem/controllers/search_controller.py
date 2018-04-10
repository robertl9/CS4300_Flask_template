from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import json

project_name = "TasteTest"
net_ids = "Robert Li: rl597, Seraphina Lee: el542, Frank Li: fl338, Stephen Ye: xy93"


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
	if not query:
		data = []
		output_message = ''
	else:
		##query should be of form '2,5,7,2,9' (5 integers separated out by commas) for now
		output_message = "Your search: " + query
		flav = re.findall('[0-9]+', query)
		if len(flav) != 5:
			data = ["query should be of form e.g. '2,5,7,2,9'"]
		else:
			flavors = np.array([int(x) for x in flav])
			data = [raw[i]['title'] for i in cos_sim_flavor(flavors)]
	return render_template('search.html', name=project_name, netid=net_ids, output_message=output_message, data=data)


#precompute flavor matrix (recipe x flavor) + docnorms (recipe x norm)
#takes in np array of np array containing flavor profile, and returns a ranked list of indices
def cos_sim_flavor(flavors):
	lst = np.dot(flav_mat,flavors)
	scores = np.divide(lst, flav_norms)
	return np.ndarray.tolist(np.argsort(-scores))
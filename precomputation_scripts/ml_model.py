from __future__ import print_function
import numpy as np
import json
import warnings
warnings.filterwarnings("ignore")
import re

from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.feature_extraction.text import CountVectorizer
from annotated import annotatedDict

with open('aggreg.json') as json_data:
	raw = json.load(json_data)
	lst = []
	for rec in raw:
		lst.append(''.join([ing['name']+' ' for ing in rec['extendedIngredients']]))

with open('all_ingrs.json') as json_data:
	all_ingrs = json.load(json_data)

cv = CountVectorizer(stop_words = 'english', vocabulary = all_ingrs, max_df=0.9, min_df=3,
                     max_features=6000)
counts = cv.fit_transform(lst)

n_topic = 15
model = LDA(n_topics=n_topic)
res = model.fit_transform(counts)
feature_names = cv.get_feature_names()

def flavors_to_topics(topic_ind, model, feature_names):
	indices_ranked = np.argsort(-model.components_[topic_ind, :]) ## col = ingredient, row = topic
	flav_prof = np.array([0,0,0,0,0])
	tagged = 0
	for ind in indices_ranked:
		if tagged < 20:
			name = feature_names[ind]
			if name in annotatedDict:
				tagged += 1
				flav_lst = [annotatedDict[name]['sweet'], annotatedDict[name]['salty'],annotatedDict[name]['sour'], annotatedDict[name]['bitter'], annotatedDict[name]['umami']]
				flav_prof = np.add(flav_prof, np.array(flav_lst))
	return 10*((1.0*flav_prof)/np.max(flav_prof))


def ingr_to_topic_prof(ingr, model, topic_profs):
	return topic_profs[np.argmax(model.components_[:, cv.vocabulary_[ingr]])]


topic_profs = [flavors_to_topics(i, model, feature_names) for i in range(n_topic)]

np.save('topic_profs.npy', topic_profs)
np.save('model_components.npy', model.components_)
np.save('cv_vocabulary.npy', cv.vocabulary_)






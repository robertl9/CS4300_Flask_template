from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import requests
import json
from bs4 import BeautifulSoup

from nltk.corpus import stopwords

from nltk.stem import PorterStemmer
import re
stemmer=PorterStemmer()
stop = set(stopwords.words('english'))


#import Levenshtein

project_name = "TasteTest"
net_ids = "Robert Li: rl597, Seraphina Lee: el542, Frank Li: fl338, Steven Ye: xy93"


#######populating flavor values
#from annotated import annotatedDict
#import units
#import ml_model

smallest = ["pinch", "pinches", "gram",  "mL", "grams", "g", "ml",  "gr", "gm", "dash", "Dash", "dashes",  "Gram"]
spoon = ["teaspoons", "tablespoon", "teaspoon", "tablespoons", "tsp", "Tb", "tbsp", "Tablespoon",
	"Teaspoon", "T", "t", "Tbsp", "Tbs", "Tablespoons", "tsps", "Tsp","Teaspoons", "tbsps", "TB", "Tbsps"]
cup = ["cup", "cups", "c", "C", "Cup", "Cups"]
pint = ["pint", "pints", "pt"]
small = ["ounces", "oz", "ounce", "fl. oz.", "ozs", "fluid ounces", "Oz"]
bigger = ["pounds", "lb", "pound", "lbs", "kg", "Pound", "Pounds", "quarts", "quart", "l", "liters", "L", "liter"]
length = ["9-inch", "7-inch", "3-inch", "6-inch", "2-inch", "4-inch", "10-inch", "8 inch", "inches", "8-inch","inch"]
biggest = ["gallon"]

units_lst = [(smallest, 0.1), (spoon, 1), (cup, 1), (pint, 4), (small, 0.2), (bigger, 8), (length, 0.5), (biggest, 16)]

def unit_weights(unit):
	for (lst, weight) in units_lst:
		if unit in lst:
			return weight
	return 1

annotatedDict = {"button mushrooms" : { "umami" : 8, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "poppy seeds" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 2, "sweet" : 3 },
			 "low sodium chicken stock" : { "umami" : 6, "bitter" : 1, "sour" : 1, "salty": 4, "sweet" : 2 },
			 "oreo cookies" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 8 },
			 "rice syrup" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 8 },
			 "skim milk" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 3 },
			 "caraway seeds" : { "umami" : 1, "bitter" : 3, "sour" : 1, "salty": 3, "sweet" : 2 },
			 "brandy" : { "umami" : 1, "bitter" : 5, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "pear" : { "umami" : 1, "bitter" : 1, "sour" : 3, "salty": 1, "sweet" : 5 },
			 "ground turkey" : { "umami" : 6, "bitter" : 1, "sour" : 1, "salty": 4, "sweet" : 1 },
			 "golden brown sugar" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 10 },
			 "fennel bulb" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "dry bread crumbs" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "coarse sea salt" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 10, "sweet" : 1 },
			 "coconut cream" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 3 },
			 "dried parsley" : { "umami" : 1, "bitter" : 3, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "cheese" : { "umami" : 3, "bitter" : 3, "sour" : 2, "salty": 4, "sweet" : 2 },
			 "pepperoni" : { "umami" : 7, "bitter" : 1, "sour" : 1, "salty": 6, "sweet" : 1 },
			 "sriracha sauce" : { "umami" : 4, "bitter" : 1, "sour" : 1, "salty": 4, "sweet" : 2 },
			 "baguette" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 2 },
			 "skinless boneless chicken thighs" : { "umami" : 6, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "baby arugula" : { "umami" : 2, "bitter" : 6, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "dry mustard" : { "umami" : 3, "bitter" : 2, "sour" : 2, "salty": 3, "sweet" : 2 },
			 "low fat sour cream" : { "umami" : 1, "bitter" : 1, "sour" : 6, "salty": 3, "sweet" : 1 },
			 "blue cheese" : { "umami" : 3, "bitter" : 2, "sour" : 3, "salty": 5, "sweet" : 1 },
			 "shredded mozzarella" : { "umami" : 3, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 2 },
			 "yellow onions" : { "umami" : 3, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "cumin powder" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 2, "sweet" : 2 },
			 "cashews" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 2 },
			 "red curry paste" : { "umami" : 4, "bitter" : 2, "sour" : 1, "salty": 6, "sweet" : 2 },
			 "cajun seasoning" : { "umami" : 4, "bitter" : 1, "sour" : 1, "salty": 6, "sweet" : 3 },
			 "jalapeno peppers" : { "umami" : 2, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "raspberry jam" : { "umami" : 1, "bitter" : 1, "sour" : 4, "salty": 1, "sweet" : 4 },
			 "wine" : { "umami" : 1, "bitter" : 4, "sour" : 2, "salty": 1, "sweet" : 3 },
			 "ground cardamom" : { "umami" : 1, "bitter" : 3, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "whipping cream" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 6 },
			 "whole cranberry sauce" : { "umami" : 1, "bitter" : 3, "sour" : 3, "salty": 1, "sweet" : 5 },
			 "shiitake mushrooms" : { "umami" : 6, "bitter" : 2, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "parmigiano reggiano" : { "umami" : 4, "bitter" : 3, "sour" : 1, "salty": 4, "sweet" : 1 },
			 "pomegranate juice" : { "umami" : 1, "bitter" : 1, "sour" : 3, "salty": 1, "sweet" : 3 },
			 "mascarpone cheese" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 3 },
			 "spinach leaves" : { "umami" :1, "bitter" : 4, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "puff pastry" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 3 },
			 "corn kernels" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 3 },
			 "light cream cheese" : { "umami" : 1, "bitter" : 1, "sour" : 2, "salty": 3, "sweet" : 3 },
			 "instant yeast" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "granny smith apples" : { "umami" : 1, "bitter" : 2, "sour" : 4, "salty": 1, "sweet" : 4 },
			 "parsley leaves" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "ground chicken" : { "umami" : 6, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "unsweetened applesauce" : { "umami" : 1, "bitter" : 1, "sour" : 3, "salty": 1, "sweet" : 3 },
			 "tapioca flour" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "dill" : { "umami" : 1, "bitter" : 2, "sour" : 2, "salty": 1, "sweet" : 1},
			 "oatmeal" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "gruyere cheese" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 2, "sweet" : 3 },
			 "cheddar" : { "umami" : 3, "bitter" : 3, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "almond butter" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "semi-sweet chocolate" : { "umami" : 1, "bitter" : 3, "sour" : 1, "salty": 1, "sweet" : 4 },
			 "cooked brown rice" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "unsweetened chocolate" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "nonfat greek yogurt" : { "umami" : 1, "bitter" : 4, "sour" : 2, "salty": 1, "sweet" : 3 },
			 "nonfat cool whip" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 6 },
			 "sundried tomatoes" : { "umami" : 6, "bitter" : 2, "sour" : 1, "salty": 5, "sweet" : 2 },
			 "sweetened shredded coconut" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 4 },
			 "cornmeal" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "hamburger buns" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "tart apples" : { "umami" : 1, "bitter" : 1, "sour" : 4, "salty": 1, "sweet" : 3 },
			 "hoisin sauce" : { "umami" : 4, "bitter" : 1, "sour" : 1, "salty": 5, "sweet" : 3 },
			 "sharp cheddar" : { "umami" : 2, "bitter" : 5, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "sherry vinegar" : { "umami" : 1, "bitter" : 2, "sour" : 3, "salty": 3, "sweet" : 2 },
			 "canned pumpkin puree" : { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 3 },
			 "pumpkin" : { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 3 },
			 "maraschino cherries" : { "umami" : 1, "bitter" : 1, "sour" : 2, "salty": 1, "sweet" : 5 },
			 "roma tomatoes" : { "umami" : 3, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "turbinado sugar" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 10 },
			 "seasoning" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "limes" : { "umami" : 1, "bitter" : 1, "sour" : 10, "salty": 1, "sweet" : 1 },
			 "self-raising flour" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "radishes" : { "umami" : 1, "bitter" : 3, "sour" : 1, "salty": 1, "sweet" : 2},
			 "sunflower seeds" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 4, "sweet" : 1 },
			 "whiskey" : { "umami" : 1, "bitter" : 4, "sour" : 2, "salty": 1, "sweet" : 2 },
			 "roasted peanuts" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 2 },
			 "raw cashews" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "cinnamon sticks" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "mayo" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "juice of orange" : { "umami" : 1, "bitter" : 1, "sour" : 3, "salty": 1, "sweet" : 4 },
			 "greens" : { "umami" : 1, "bitter" : 3, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "milk chocolate" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 7 },
			 "extra firm tofu" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "rice wine vinegar" : { "umami" : 1, "bitter" : 2, "sour" : 4, "salty": 3, "sweet" : 1 },
			 "pancetta" : { "umami" : 7, "bitter" : 1, "sour" : 1, "salty": 7, "sweet" : 1 },
			 "ground turmeric" : { "umami" : 1, "bitter" : 3, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "simple syrup" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 8 },
			 "margarine" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 2 },
			 "fresh mint leaves" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "iceberg lettuce" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "vegetable shortening" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 2 },
			 "dried rosemary" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "vinegar" : { "umami" : 1, "bitter" : 2, "sour" : 4, "salty": 2, "sweet" : 1 },
			 "lemon extract" : { "umami" : 1, "bitter" : 1, "sour" : 10, "salty": 1, "sweet" : 1 },
			 "rice flour" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "rum" : { "umami" : 1, "bitter" : 3, "sour" : 2, "salty": 10, "sweet" : 3 },
			 "ground pork" : { "umami" : 7, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "frozen spinach" : { "umami" : 1, "bitter" : 3, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "old fashioned rolled oats" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "ears corn" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "bell pepper" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "lemongrass" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "dried apricots" : { "umami" : 1, "bitter" : 1, "sour" : 3, "salty": 1, "sweet" : 4 },
			 "bacon strips" : { "umami" : 7, "bitter" : 1, "sour" : 1, "salty": 5, "sweet" : 1 },
			 "bell peppers" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "confectioners sugar" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 10 },
			 "grapeseed oil" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "white cake mix" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 4 },
			 "tahini" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 3, "sweet" : 2 },
			 "old-fashioned oats" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "crushed red pepper" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "food coloring" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "raw honey" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 10 },
			 "garam masala" : { "umami" : 3, "bitter" : 2, "sour" : 1, "salty": 3, "sweet" : 2 },
			 "allspice" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "nuts" : { "umami" : 2, "bitter" : 2, "sour" : 1, "salty": 2, "sweet" : 2 },
			 "seasoned salt" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 10, "sweet" : 1 },
			 "quick cooking oats" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "broccoli" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "white pepper" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "blackberries" : { "umami" : 1, "bitter" : 1, "sour" : 2, "salty": 1, "sweet" : 3 },
			 "beef stock" : { "umami" : 6, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "lime wedges" : { "umami" : 1, "bitter" : 1, "sour" : 10, "salty": 1, "sweet" : 1 },
			 "cooked quinoa" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "medjool dates" : { "umami" : 1, "bitter" : 1, "sour" : 3, "salty": 1, "sweet" : 5 },
			 "provolone cheese" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 3, "sweet" : 2 },
			 "nutella" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 8 },
			 "cumin seeds" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "ricotta cheese" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 3, "sweet" : 2 },
			 "lemons" : { "umami" : 1, "bitter" : 1, "sour" : 10, "salty": 1, "sweet" : 1 },
			 "prosciutto" : { "umami" : 7, "bitter" : 2, "sour" : 1, "salty": 5, "sweet" : 1 },
			 "vanilla bean" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 3 },
			 "low fat milk" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "fresh flat-leaf parsley" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "coconut sugar" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 8 },
			 "golden raisins" : { "umami" : 1, "bitter" : 1, "sour" : 2, "salty": 1, "sweet" : 4 },
			 "double cream" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 3 },
			 "canned tomato sauce" : { "umami" : 3, "bitter" : 1, "sour" : 2, "salty": 2, "sweet" : 2 },
			 "sub rolls" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "agave nectar" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 10 },
			 "fresh cilantro leaves" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "canned chickpeas" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "red bell peppers" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "black peppercorns" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "barbecue sauce" : { "umami" : 4, "bitter" : 1, "sour" : 2, "salty": 5, "sweet" : 3 },
			 "tequila" : { "umami" : 1, "bitter" : 3, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "pomegranate seeds" : { "umami" : 1, "bitter" : 1, "sour" : 3, "salty": 1, "sweet" : 4 },
			 "whole eggs" : { "umami" : 4, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "pepper sauce" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "hazelnuts" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "bourbon" : { "umami" : 1, "bitter" : 4, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "cocoa" : { "umami" : 1, "bitter" : 3, "sour" : 1, "salty": 1, "sweet" : 6 },
			 "half & half" : { "umami" :1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "spaghetti" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "mozzarella cheese" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "leeks" : { "umami" : 1, "bitter" : 3, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "enchilada sauce" : { "umami" : 3, "bitter" : 2, "sour" : 1, "salty": 5, "sweet" : 2 },
			 "sriracha" : { "umami" : 3, "bitter" : 1, "sour" : 1, "salty": 4, "sweet" : 2 },
			 "red wine" : { "umami" : 1, "bitter" : 3, "sour" : 3, "salty": 1, "sweet" : 3 },
			 "olives" : { "umami" : 1, "bitter" :3, "sour" : 1, "salty": 6, "sweet" : 1 },
			 "panko bread crumbs" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "vegetable stock" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 5, "sweet" : 1 },
			 "part-skim mozzarella cheese" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "chicken breast" : { "umami" : 6, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "lemon peel" : { "umami" : 1, "bitter" : 3, "sour" : 4, "salty": 1, "sweet" : 1 },
			 "panko breadcrumbs" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "beer" : { "umami" : 1, "bitter" : 4, "sour" : 2, "salty": 1, "sweet" : 2 },
			 "mint leaves" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "rice" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "milk chocolate chips" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 7 },
			 "swiss cheese" : { "umami" : 1, "bitter" : 5, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "stevia" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 10 },
			 "light coconut milk" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 3 },
			 "romaine lettuce" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "whipped topping" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 5 },
			 "almond flour" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "frozen corn" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 2, "sweet" : 3 },
			 "slivered almonds" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 2, "sweet" : 2 },
			 "white chocolate" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 8 },
			 "orange" : { "umami" : 1, "bitter" : 1, "sour" : 4, "salty": 1, "sweet" : 5 },
			 "plain yogurt" : { "umami" : 1, "bitter" : 1, "sour" : 2, "salty": 1, "sweet" : 3 },
			 "feta" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 4, "sweet" : 2 },
			 "chili sauce" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 3, "sweet" : 2 },
			 "marinara sauce" : { "umami" : 3, "bitter" : 1, "sour" : 2, "salty": 4, "sweet" : 2 },
			 "russet potatoes" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "vanilla ice cream" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 7 },
			 "peanut butter cups" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 7 },
			 "dates" : { "umami" : 1, "bitter" : 1, "sour" : 3, "salty": 1, "sweet" : 4 },
			 "yogurt" : { "umami" : 1, "bitter" : 2, "sour" : 2, "salty": 1, "sweet" : 4 },
			 "jalapenos" : { "umami" : 2, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "coffee" : { "umami" : 1, "bitter" : 5, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "ranch dressing" : { "umami" : 3, "bitter" : 1, "sour" : 2, "salty": 5, "sweet" : 2 },
			 "arugula" : { "umami" : 2, "bitter" : 4, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "bread crumbs" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "semisweet chocolate" : { "umami" : 1, "bitter" : 3, "sour" : 1, "salty": 1, "sweet" : 6 },
			 "ice cubes" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "tomato sauce" : { "umami" : 3, "bitter" : 2, "sour" : 2, "salty": 4, "sweet" : 2 },
			 "black olives" : { "umami" : 2, "bitter" : 3, "sour" : 1, "salty": 7, "sweet" : 1 },
			 "whole wheat flour" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "icing sugar" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 10 },
			 "brownie mix" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 6 },
			 "whole wheat pastry flour" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "fresh chives" : { "umami" : 1, "bitter" : 2, "sour" : 3, "salty": 1, "sweet" : 2 },
			 "yellow bell pepper" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "sweet potato" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 5 },
			 "shredded cheese" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "cayenne" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "mango" : { "umami" : 1, "bitter" :1 , "sour" : 4, "salty": 1, "sweet" : 5 },
			 "sweet onion" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 2, "sweet" : 2 },
			 "white onion" : { "umami" : 1, "bitter" : 3, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "roasted red peppers" : { "umami" : 3, "bitter" : 2, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "pineapple juice" : { "umami" : 1, "bitter" : 1, "sour" : 4, "salty": 1, "sweet" : 7 },
			 "capers" : { "umami" : 1, "bitter" : 2, "sour" : 4, "salty": 6, "sweet" : 1 },
			 "graham cracker crumbs" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 3 },
			 "lean ground beef" : { "umami" : 7, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "cabbage" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "brussels sprouts" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "fresh mushrooms" : { "umami" : 6, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "shredded mozzarella cheese" : { "umami" : 1, "bitter" : 1, "sour" : 2, "salty": 2, "sweet" : 2 },
			 "salmon" : { "umami" : 6, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "fresh thyme leaves" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "plain flour" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "peanuts" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "half and half" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "evaporated milk" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 4 },
			 "grape tomatoes" : { "umami" : 2, "bitter" : 2, "sour" : 2, "salty": 1, "sweet" : 3 },
			 "basmati rice" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "tortilla chips" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "cider vinegar" : { "umami" : 1, "bitter" : 3, "sour" : 4, "salty": 1, "sweet" : 3 },
			 "yeast" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "skinless boneless chicken breast" : { "umami" : 6, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "yukon gold potatoes" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "basil" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "mint" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "white whole wheat flour" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "fresh parsley leaves" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "vodka" : { "umami" : 1, "bitter" : 3, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "brown rice" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "graham crackers" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 3 },
			 "egg white" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "cinnamon stick" : { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "red potatoes" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "white vinegar" : { "umami" : 1, "bitter" : 2, "sour" : 4, "salty": 3, "sweet" : 1 },
			 "fresh mint" : { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "turkey" : { "umami" : 7, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },

			 "salt": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 10, "sweet" : 1 },
			 "olive oil": { "umami" : 5, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "butter": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 4, "sweet" : 1 },
			 "flour": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "sugar": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 10 },
			 "garlic": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 5, "sweet" : 2 },
			 "eggs": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "vanilla extract": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 8 },
			 "water": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "unsalted butter": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "kosher salt": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 10, "sweet" : 1 },
			 "onion": { "umami" : 2, "bitter" : 3, "sour" : 2, "salty": 3, "sweet" : 4 },
			 "milk": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1},
			 "baking powder": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "egg": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "granulated sugar": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 10},
			 "baking soda": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "salt and pepper": { "umami" : 2, "bitter" : 3, "sour" : 1, "salty": 10, "sweet" : 1},
			 "lemon juice": { "umami" : 7, "bitter" : 1, "sour" : 10, "salty": 1, "sweet" : 4 },
			 "brown sugar": { "umami" : 7, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 10 },
			 "pepper": { "umami" : 2, "bitter" : 3, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "black pepper": { "umami" : 2, "bitter" : 3, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "cinnamon": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 4 },
			 "garlic cloves": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 5, "sweet" : 2 },
			 "cream cheese": { "umami" : 1, "bitter" : 1, "sour" : 2, "salty": 3, "sweet" : 3 },
			 "honey": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 9 },
			 "heavy cream": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 3 },
			 "vanilla": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 6 },
			 "ground cinnamon": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 4 },
			 "powdered sugar": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 10 },
			 "vegetable oil": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "parmesan cheese": { "umami" : 7, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "garlic powder": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 5, "sweet" : 1 },
			 "oregano": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "lemon zest": { "umami" : 1, "bitter" : 3, "sour" : 10, "salty": 1, "sweet" : 2},
			 "canola oil": { "umami" : 3, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "sea salt": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 10, "sweet" : 1 },
			 "sour cream": { "umami" : 1, "bitter" : 1, "sour" : 6, "salty": 1, "sweet" : 2 },
			 "carrots": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 4 },
			 "bacon": { "umami" : 9, "bitter" : 1, "sour" : 1, "salty": 7, "sweet" : 1 },
			 "lime juice": { "umami" : 1, "bitter" : 2, "sour" : 10, "salty": 10, "sweet" : 4 },
			 "cilantro": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "light brown sugar": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 10 },
			 "cornstarch": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 10 },
			 "ground cumin": { "umami" : 3, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "red onion": { "umami" : 2, "bitter" : 3, "sour" : 2, "salty": 3, "sweet" : 4 },
			 "extra virgin olive oil": { "umami" : 3, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "ground pepper": { "umami" : 2, "bitter" : 3, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "fresh parsley": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "celery": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 3 },
			 "chili powder": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "avocado": { "umami" : 1, "bitter" : 1, "sour" : 2, "salty": 1, "sweet" : 4 },
			 "maple syrup": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 9 },
			 "green onions": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 3 },
			 "cayenne pepper": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "buttermilk": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "dijon mustard": { "umami" : 1, "bitter" : 4, "sour" : 3, "salty": 1, "sweet" : 4 },
			 "nutmeg": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 3 },
			 "whole milk": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "egg whites": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "paprika": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "juice of lemon": { "umami" : 1, "bitter" : 1, "sour" : 10, "salty": 1, "sweet" : 4 },
			 "pecans": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 2 },
			 "yellow onion": { "umami" : 2, "bitter" : 3, "sour" : 2, "salty": 3, "sweet" : 4 },
			 "oil": { "umami" : 3, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "walnuts": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 2 },
			 "canned tomatoes": { "umami" : 5, "bitter" : 1, "sour" : 5, "salty": 1, "sweet" : 5 },
			 "all purpose flour": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "soy sauce": { "umami" : 6, "bitter" : 1, "sour" : 1, "salty": 8, "sweet" : 1 },
			 "red pepper flakes": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "coconut oil": { "umami" : 3, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "worcestershire sauce": { "umami" : 2, "bitter" : 1, "sour" : 3, "salty": 1, "sweet" : 5 },
			 "blueberries": { "umami" : 3, "bitter" : 1, "sour" : 5, "salty": 1, "sweet" : 6 },
			 "mayonnaise": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "egg yolks": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "skinless boneless chicken breasts": { "umami" : 6, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "almonds": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 2 },
			 "fresh ginger": { "umami" : 1, "bitter" : 3, "sour" : 2, "salty": 1, "sweet" : 4 },
			 "red bell pepper": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 4 },
			 "chocolate chips": { "umami" : 1, "bitter" : 3, "sour" : 1, "salty": 1, "sweet" : 8 },
			 "balsamic vinegar": { "umami" : 2, "bitter" : 1, "sour" : 9, "salty": 2, "sweet" : 1 },
			 "chicken broth": { "umami" : 5, "bitter" : 1, "sour" : 1, "salty": 4, "sweet" : 1 },
			 "ginger": { "umami" : 1, "bitter" : 3, "sour" : 2, "salty": 1, "sweet" : 4 },
			 "fresh cilantro": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "almond milk": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "scallions": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 3 },
			 "cocoa powder": { "umami" : 1, "bitter" : 4, "sour" : 1, "salty": 1, "sweet" : 6 },
			 "strawberries": { "umami" : 3, "bitter" : 1, "sour" : 6, "salty": 1, "sweet" : 6 },
			 "ground ginger": { "umami" : 1, "bitter" : 3, "sour" : 2, "salty": 1, "sweet" : 4 },
			 "zucchini": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "carrot": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 3 },
			 "peanut butter": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 4, "sweet" : 1 },
			 "garlic clove": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 5, "sweet" : 1 },
			 "onion powder": { "umami" : 2, "bitter" : 3, "sour" : 2, "salty": 3, "sweet" : 4 },
			 "unsweetened cocoa powder": { "umami" : 1, "bitter" : 5, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "tomato paste": { "umami" : 5, "bitter" : 1, "sour" : 5, "salty": 1, "sweet" : 5 },
			 "spinach": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "juice of lime": { "umami" : 1, "bitter" : 1, "sour" : 10, "salty": 1, "sweet" : 4 },
			 "fresh basil": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "tomatoes": { "umami" : 5, "bitter" : 1, "sour" : 5, "salty": 1, "sweet" : 5 },
			 "ground nutmeg": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "cherry tomatoes": { "umami" : 5, "bitter" : 1, "sour" : 5, "salty": 1, "sweet" : 5 },
			 "parsley": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "banana": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 5 },
			 "apple cider vinegar": { "umami" : 1, "bitter" : 1, "sour" : 4, "salty": 1, "sweet" : 3 },
			 "bananas": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 5 },
			 "mushrooms": { "umami" : 6, "bitter" : 2, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "hot sauce": { "umami" : 3, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 3 },
			 "cumin": { "umami" : 3, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "tomato": { "umami" : 5, "bitter" : 1, "sour" : 5, "salty": 1, "sweet" : 5},
			 "potatoes": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "parmesan": { "umami" : 7, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "confectioners' sugar": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 10 },
			 "jalapeno": { "umami" : 2, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "orange zest": { "umami" : 1, "bitter" : 3, "sour" : 6, "salty": 1, "sweet" : 4 },
			 "white sugar": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 10 },
			 "sesame oil": { "umami" : 6, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "onions": { "umami" : 2, "bitter" : 3, "sour" : 2, "salty": 3, "sweet" : 4 },
			 "bread": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "vegetable broth": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "chicken stock": { "umami" : 5, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "semisweet chocolate chips": { "umami" : 1, "bitter" : 3, "sour" : 1, "salty": 2, "sweet" : 6 },
			 "sea-salt": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 10, "sweet" : 1 },
			 "shredded cheddar cheese": { "umami" : 3, "bitter" : 2, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "feta cheese": { "umami" : 3, "bitter" : 1, "sour" : 2, "salty": 4, "sweet" : 1 },
			 "dried thyme": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "fresh thyme": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "Salt & Pepper": { "umami" : 2, "bitter" : 3, "sour" : 1, "salty": 10, "sweet" : 1 },
			 "sharp cheddar cheese": { "umami" : 3, "bitter" : 2, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "smoked paprika": { "umami" : 3, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "shrimp": { "umami" : 5, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "sweetened condensed milk": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 4 },
			 "thyme": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "shallots": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 3 },
			 "coconut": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 3 },
			 "ground cloves": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 5, "sweet" : 1 },
			 "bay leaf": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "dry white wine": { "umami" : 1, "bitter" : 3, "sour" : 3, "salty": 1, "sweet" : 2 },
			 "fresh rosemary": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "apples": { "umami" : 1, "bitter" : 1, "sour" : 3, "salty": 1, "sweet" : 5 },
			 "sesame seeds": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 2 },
			 "molasses": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 8 },
			 "heavy whipping cream": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 6 },
			 "bay leaves": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "ground beef": { "umami" : 6, "bitter" : 1, "sour" : 1, "salty": 4, "sweet" : 1 },
			 "goat cheese": { "umami" : 1, "bitter" : 1, "sour" : 2, "salty": 3, "sweet" : 2 },
			 "red wine vinegar": { "umami" : 1, "bitter" : 2, "sour" : 7, "salty": 1, "sweet" : 3 },
			 "low sodium chicken broth": { "umami" : 4, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "green bell pepper": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 3 },
			 "marshmallows": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 10 },
			 "orange juice": { "umami" : 1, "bitter" : 1, "sour" : 4, "salty": 1, "sweet" : 7 },
			 "rice vinegar": { "umami" : 2, "bitter" : 1, "sour" : 5, "salty": 1, "sweet" : 1 },
			 "lemon": { "umami" : 1, "bitter" : 1, "sour" : 10, "salty": 1, "sweet" : 4 },
			 "semi sweet chocolate chips": { "umami" : 1, "bitter" : 3, "sour" : 1, "salty": 2, "sweet" : 6 },
			 "shallot": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 3 },
			 "canned black beans": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "chocolate": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 8 },
			 "curry powder": { "umami" : 3, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "almond extract": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "dark brown sugar": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 10 },
			 "plain greek yogurt": { "umami" : 1, "bitter" : 1, "sour" : 3, "salty": 1, "sweet" : 6 },
			 "corn syrup": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 10 },
			 "cheddar cheese": { "umami" : 3, "bitter" : 2, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "raspberries": { "umami" : 1, "bitter" : 1, "sour" : 5, "salty": 1, "sweet" : 5 },
			 "monterey jack cheese": { "umami" : 3, "bitter" : 2, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "whipped cream": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 9 },
			 "bbq sauce": { "umami" : 2, "bitter" : 1, "sour" : 3, "salty": 1, "sweet" : 5 },
			 "cucumber": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "fish sauce": { "umami" : 5, "bitter" : 1, "sour" : 2, "salty": 1, "sweet" : 3 },
			 "lime zest": { "umami" : 1, "bitter" : 3, "sour" : 10, "salty": 1, "sweet" : 4 },
			 "dark chocolate chips": { "umami" : 1, "bitter" : 3, "sour" : 1, "salty": 2, "sweet" : 6 },
			 "egg yolk": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "cake flour": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "kale": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "peas": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "low sodium soy sauce": { "umami" : 5, "bitter" : 1, "sour" : 1, "salty": 6, "sweet" : 1 },
			 "raisins": { "umami" : 1, "bitter" : 1, "sour" : 2, "salty": 1, "sweet" : 5 },
			 "rosemary": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "cream of tartar": { "umami" : 1, "bitter" : 1, "sour" : 2, "salty": 1, "sweet" : 1 },
			 "cherries": { "umami" : 1, "bitter" : 1, "sour" : 3, "salty": 1, "sweet" : 4 },
			 "butternut squash": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "ketchup": { "umami" : 1, "bitter" : 1, "sour" : 3, "salty": 1, "sweet" : 5 },
			 "creamy peanut butter": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 4, "sweet" : 1 },
			 "salted butter": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 4, "sweet" : 1 },
			 "mustard": { "umami" : 3, "bitter" : 2, "sour" : 2, "salty": 3, "sweet" : 2 },
			 "sprinkles": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 7 },
			 "chicken": { "umami" : 7, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "dark chocolate": { "umami" : 1, "bitter" : 3, "sour" : 1, "salty": 2, "sweet" : 6 },
			 "lettuce": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "canned coconut milk": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "peaches": { "umami" : 1, "bitter" : 1, "sour" : 2, "salty": 1, "sweet" : 6 },
			 "baby spinach": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "apple": { "umami" : 1, "bitter" : 1, "sour" : 4, "salty": 1, "sweet" : 4 },
			 "cauliflower": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "greek yogurt": { "umami" : 1, "bitter" : 1, "sour" : 3, "salty": 1, "sweet" : 6 },
			 "active yeast": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "cream": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 8 },
			 "bittersweet chocolate": { "umami" : 1, "bitter" : 3, "sour" : 1, "salty": 1, "sweet" : 6 },
			 "sweet potatoes": { "umami" : 2, "bitter" : 1, "sour" : 3, "salty": 1, "sweet" : 1 },
			 "asparagus": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "lime": { "umami" : 1, "bitter" : 1, "sour" : 10, "salty": 1, "sweet" : 3 },
			 "pumpkin puree": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 3 },
			 "fresh dill": { "umami" : 1, "bitter" : 1, "sour" : 6, "salty": 1, "sweet" : 3 },
			 "beef broth": { "umami" : 6, "bitter" : 1, "sour" : 1, "salty": 4, "sweet" : 1 },
			 "salsa": { "umami" : 2, "bitter" : 1, "sour" : 3, "salty": 2, "sweet" : 5 },
			 "artichoke hearts": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "pineapple": { "umami" : 1, "bitter" : 1, "sour" : 4, "salty": 1, "sweet" : 6 },
			 "ice": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "garlic salt": { "umami" : 3, "bitter" : 1, "sour" : 1, "salty": 10, "sweet" : 1 },
			 "pine nuts": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "jalapeno pepper": { "umami" : 2, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "flour tortillas": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 1 },
			 "quinoa": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "dried cranberries": { "umami" : 1, "bitter" : 2, "sour" : 4, "salty": 1, "sweet" : 4 },
			 "applesauce": { "umami" : 1, "bitter" : 1, "sour" : 4, "salty": 1, "sweet" : 5 },
			 "coconut flour": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "green beans": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "chives": { "umami" : 3, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "ham": { "umami" : 5, "bitter" : 1, "sour" : 1, "salty": 4, "sweet" : 1 },
			 "white chocolate chips": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 2, "sweet" : 10 },
			 "pumpkin pie spice": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 4 },
			 "italian seasoning": { "umami" : 2, "bitter" : 1, "sour" : 2, "salty": 3, "sweet" : 2 },
			 "shredded chicken": { "umami" : 6, "bitter" : 1, "sour" : 1, "salty": 4, "sweet" : 1 },
			 "dried basil": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "corn tortillas": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "coconut milk": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 2 },
			 "chicken breasts": { "umami" : 6, "bitter" : 1, "sour" : 1, "salty": 4, "sweet" : 1 },
			 "basil leaves": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "pasta": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "kalamata olives": { "umami" : 5, "bitter" : 1, "sour" : 4, "salty": 3, "sweet" : 2 },
			 "ground allspice": { "umami" : 1, "bitter" : 2, "sour" : 2, "salty": 2, "sweet" : 2 },
			 "black beans": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "white wine": { "umami" : 1, "bitter" : 1, "sour" : 3, "salty": 1, "sweet" : 3 },
			 "coarse salt": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 10, "sweet" : 1 },
			 "rolled oats": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "cranberries": { "umami" : 1, "bitter" : 1, "sour" : 5, "salty": 1, "sweet" : 4 },
			 "avocados": { "umami" : 1, "bitter" : 1, "sour" : 2, "salty": 1, "sweet" : 4 },
			 "shortening": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 3 },
			 "broccoli florets": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "ground coriander": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "pie crust": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 3, "sweet" : 2 },
			 "white wine vinegar": { "umami" : 1, "bitter" : 1, "sour" : 8, "salty": 1, "sweet" : 1 },
			 "green onion": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 3 },
			 "chia seeds": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "fresh basil leaves": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "bread flour": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "peanut oil": { "umami" : 2, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "oats": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 1, "sweet" : 1 },
			 "breadcrumbs": { "umami" : 1, "bitter" : 1, "sour" : 1, "salty": 2, "sweet" : 1 },
			 "flat-leaf parsley": { "umami" : 1, "bitter" : 2, "sour" : 1, "salty": 1, "sweet" : 1 },
			 }

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


#### the ml components are no longer called, but have been used to precompute matrices:
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

#for i in range(len(raw)):
#	flav_prof = np.array([0,0,0,0,0])
#	for j in range(len(raw[i]['extendedIngredients'])):
#		ingr = raw[i]['extendedIngredients'][j]
#		amount = ingr['amount']
#		unit = ingr['unit'] #need to map them to proportional weights later (e.g. 1 lb = 16 oz)
#		name = ingr['name']
#		if name in annotatedDict:
#			flav_lst = [annotatedDict[name]['sweet'], annotatedDict[name]['salty'],annotatedDict[name]['sour'], annotatedDict[name]['bitter'], annotatedDict[name]['umami']]
#			flav_prof = np.add(flav_prof, (amount*unit_weights(unit))*np.array(flav_lst))
#		else:
#			###call ml_model and get topic-estimated flavor prof
#			flav_prof = np.add(flav_prof, ingr_to_topic_prof(name, model_components, topic_profs))
#		ingr_mat[i,ingr_inv_index[name]] = 1
#	if np.max(flav_prof) == 0:
#		flav_prof = np.array([1,1,1,1,1])
#	flav_mat[i,:] = 10*((1.0*flav_prof)/np.max(flav_prof))
#	flav_norms[i] = np.linalg.norm(flav_mat[i])

flav_mat = np.load('flav_mat.npy')
flav_norms = np.load('flav_norms.npy')
restriction_strs = {"alcohol" : np.load('alcohol.npy'),
					"beef" : np.load('beef.npy'),
					"dairy" : np.load('dairy.npy'),
					"egg" : np.load('egg.npy'),
					"fish" : np.load('fish.npy'),
					"gluten" : np.load('gluten.npy'),
					"halal" : np.load('halal.npy'),
					"ketogenic": np.load('ketogenic.npy'),
					"kosher": np.load('kosher.npy'),
					"lactoovo": np.load('lactoovo.npy'),
					"pork": np.load('pork.npy'),
					"peanut": np.load('peanut.npy'),
					"pescatarian": np.load('pescatarian.npy'),
					"sesame": np.load('sesame.npy'),
					"shellfish": np.load('shellfish.npy'),
					"soy": np.load('soy.npy'),
					"treenuts": np.load('treenuts.npy'),
					"vegan": np.load('vegan.npy'),
					"vegetarian": np.load('vegetarian.npy'),
					"wheat": np.load('wheat.npy')}
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
		restrictions = request.args.getlist('restrictions')
		print(restrictions)
		flavors = np.array([sweet, salty, sour, bitter, umami])
		if np.max(flavors) == 0:
			flav_prof = np.array([1,1,1,1,1])
		query = [(pair.split('|')[0], bool(int(pair.split('|')[1]))) for pair in query.split(',')[:-1]]
		data = [raw[i] for i in cos_sim_flavor(flavors, filter_clude_ingr(query, restrictions))]
		output_message = "Your search returned " + str(len(data)) + " results."
	except TypeError:
		data = []
		query = []
		restrictions = []
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
		                                  restrictions=restrictions,
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
	excluded_ingredients = [ingr for (ingr, incl) in ingredients_tuples if not incl]
	included_ingredients = [ingr for (ingr, incl) in ingredients_tuples if incl]
	print(included_ingredients)
	new_exclu = tokenize_ingredients (excluded_ingredients, stop)
	new_inclu = tokenize_ingredients(included_ingredients, stop)
	excluded_ingredients_set = get_stems (new_exclu)
	#included_ingredients_set = get_stems(new_inclu)
	included_ingredients_set = get_stems(included_ingredients)
	for i in range(len(raw)):
		recipe_ingredients = [ingr['name'] for ingr in raw[i]['extendedIngredients']]
		new_recipe = tokenize_ingredients (recipe_ingredients, stop)
		recipe_ingredients_set = get_stems (new_recipe)
		inter_exclu = excluded_ingredients_set.intersection (recipe_ingredients_set)
		inter_inclu = included_ingredients_set.intersection (recipe_ingredients_set)

		### we want inter_exclu to be empty and inter_inclu to be nonempty
		if len(included_ingredients)==0:
			filter_vec[i] = (len(inter_exclu) == 0)
		else:
			filter_vec[i] = (len(inter_exclu) == 0 and len(inter_inclu) == len(included_ingredients))
	return filter_vec


#return flavor matrix that has 0's for recipes that exclude or 1's if include the query ingredient
def filter_clude_ingr(query, restrictions):
	filtered_flav_mat = np.copy(flav_mat)
	filter_vec = np.multiply(exclude_recipe(query), exclude_recipe_restriction_prec(restrictions))
	filtered_flav_mat = filter_vec*filtered_flav_mat
	return filtered_flav_mat


#return dish with new field rating containing social feedback scrapped from source url
def add_rating(dish):
	dish["rating"] = parser(dish["sourceUrl"])
	return dish


def exclude_recipe_restriction_prec(restrictions):
	filter_vec = np.ones((len(raw), 1))
	for res_str in restrictions:
		filter_vec = np.multiply(filter_vec, restriction_strs[res_str])
	return filter_vec


##all the functions and sets below are no longer called, since we saved them as precomputed matrices
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

##############################################



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

def parser(web_page):
    first_index = web_page.find('.')
    second_index = web_page.find('.',first_index+1)
    web = web_page[first_index+1:second_index]
    if web == "allrecipes":
        return review_parser_allrecipes(web_page)
    elif web =="foodnetwork":
        return review_parser_foodnetwork(web_page)
    else:
        return -1 #probably just return the spoontacular score


def review_parser_allrecipes(web_page): #returns the star_rating out of five as a float for the site all recipes
    page = requests.get(web_page)
    formatted = BeautifulSoup(page.content, 'html.parser')
    rating_box = formatted.find('div', attrs={'class':'rating-stars'})
    rating = rating_box.get('data-ratingstars')
    try:
        return float(rating)
    except ValueError:
        return -1


def review_parser_foodnetwork(web_page): #returns star_rating for foodnetwork
    page = requests.get(web_page)
    formatted = BeautifulSoup(page.content, 'html.parser')
    rating_box = formatted.find('script',attrs={'type':'application/ld+json'})
    rating = json.loads(rating_box.text)
    try:
        return rating["aggregateRating"]["ratingValue"]
    except ValueError:
        return -10

def find_missing (lst, annotated):
	for i in lst:
		if i[0] not in annotated.keys():
			print (i)

def get_annotated():
	return annotatedDict

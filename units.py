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
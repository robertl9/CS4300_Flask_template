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

kosher = shellfish.union(pork.union(wild_meat))



def restriction_category(cat_lst): #this function takes in a list of broad categories such a kosher and wheat
                                   #and return a set of ingredients to be excluded
                                    #cat_lst is the list of restrictions and ingr_lst is recipe ingredient list
                                    #cat_lst has to be one of the above categories
    result = Set()
    for elt in cat_lst:
        result = result.union(elt)
    return result
        
def is_kosher(ingr_lst):
    beef_check = false
    dairy_check = false
    for elt in ingr_lst:
        if elt in beef:
            beef_check = true
        if elt in dairy:
            dairy_check = true
        if elt in kosher:
            return false
    return not (beef_check && dairy_check)


def is_halal(ingr_lst):
    for elt in ingr_lst:
        if elt in pork:
            return false
        if elt in alcohol:
            return false
    return true
    
    
    
    
    
    
    
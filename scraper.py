
import urllib2
from bs4 import BeautifulSoup

#Given the recipe website, denote this of type query
#For example... 
query = 'https://www.allrecipes.com/recipe/21014/good-old-fashioned-pancakes/?internalSource=previously%20viewed&referringContentType=home%20page&clickId=cardslot%202'

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
    page = urllib2.urlopen(web_page)
    formatted = BeautifulSoup(page, 'html.parser')
    rating_box = formatted.find('div', attrs={'class':'rating-stars'})
    rating = rating_box.get('data-ratingstars')
    try:
        return float(rating)
    except ValueError:
        return -1


def review_parser_foodnetwork(web_page): #returns star_rating for foodnetwork
    page = urllib2.urlopen(web_page)
    formatted = BeautifulSoup(page, 'html.parser')
    rating_box = formatted.find('span',attrs={'class':'gig-rating-stars'})
    rating = rating_box.get('title')
    try:
        return float(rating.split()[0])
    except ValueError:
        return -1
    
    
    
    

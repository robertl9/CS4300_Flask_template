import requests
import json
from bs4 import BeautifulSoup

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

    
    
    

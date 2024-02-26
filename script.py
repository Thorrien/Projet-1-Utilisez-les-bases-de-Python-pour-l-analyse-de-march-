import requests
from bs4 import BeautifulSoup
from livre import Livre


def recuperationLivre(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    livre = Livre(soup.find('h1').string)
    livre.prix = soup.find("p", class_="price_color").string
    livre.description = soup.find(id="product_description").next_sibling.next_sibling.string
    table = soup.table
    livre.upc = table.td.string
    livre.type = livre.upc.find_next("td").string
    livre.prixHT = livre.type.find_next("td").string 
    livre.prix = livre.prixHT.find_next("td").string 
    livre.taxe = livre.prix.find_next("td").string
    stock = livre.taxe.find_next("td").string
    livre.revues = stock.find_next("td").string
    
    for parse in stock.split('('):
        for element in parse.split():
            if element.isdigit():
                livre.nombreStock = int(element)
                
    if stock.startswith('In stock'):
        livre.stock = True
    else :
        livre.stock = False
    
    blocNote = soup.find(class_="col-sm-6 product_main")
    if blocNote.find(class_="star-rating Five"):
        livre.note = 5
    elif blocNote.find(class_="star-rating Four"):
        livre.note = 4
    elif blocNote.find(class_="star-rating Three"):
        livre.note = 3
    elif blocNote.find(class_="star-rating Two"):
        livre.note = 2
    elif blocNote.find(class_="star-rating One"):
        livre.note = 1
    elif blocNote.find(class_="star-rating Zero"):
        livre.note = 0

    categorie = soup.ul
    livre.categorie = categorie.find_next("a").find_next("a").find_next("a").string

    return livre





url = 'http://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html'


recuperationLivre(url)
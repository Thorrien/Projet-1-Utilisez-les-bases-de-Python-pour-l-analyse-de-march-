import requests
from bs4 import BeautifulSoup
from livre import Livre
import csv

def recuperationLivre(url):
    intitules = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    livre = Livre(soup.find('h1').string)
    intitules.append("titre du livre")
    #livre.prix = soup.find("p", class_="price_color").string
    livre.description = soup.find(id="product_description").next_sibling.next_sibling.string
    intitules.append("product_description")
    table = soup.table
    livre.upc = table.td.string
    intitules.append(table.th.string)
    livre.type = livre.upc.find_next("td").string
    intitules.append(livre.upc.find_next("th").string)
    livre.prixHT = livre.type.find_next("td").string 
    intitules.append(livre.type.find_next("th").string)
    livre.prix = livre.prixHT.find_next("td").string 
    intitules.append(livre.prixHT.find_next("th").string)
    livre.taxe = livre.prix.find_next("td").string
    intitules.append(livre.prix.find_next("th").string)
    stock = livre.taxe.find_next("td").string
    livre.revues = stock.find_next("td").string
    intitules.append(stock.find_next("th").string)

    for parse in stock.split('('):
        for element in parse.split():
            if element.isdigit():
                livre.nombreStock = int(element)
    if stock.startswith('In stock'):
        livre.stock = True
    else:
        livre.stock = False

    intitules.append("En stock")
    intitules.append("Nombre en stock") 

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

    intitules.append("Nombre d'étoiles")

    categorie = soup.ul
    livre.categorie = categorie.find_next("a").find_next("a").find_next("a").string

    intitules.append("Catégorie")

    return livre, intitules

def creationDuCsv(intitules, livre):
    with open(f'{livre.titre}.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(intitules)
        csv_file.close()
    
def incrementationDuLivre(livre):
    ligne = [livre.titre, livre.description, livre.upc, livre.type, livre.prixHT, livre.prix, livre.taxe, livre.revues, livre.stock, livre.nombreStock, livre.note, livre.categorie]
    with open(f'{livre.titre}.csv', "a", newline="") as f_object:
        writer = csv.writer(f_object)
        writer.writerow(ligne)
        f_object.close()

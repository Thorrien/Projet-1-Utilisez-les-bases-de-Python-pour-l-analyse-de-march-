import requests
from bs4 import BeautifulSoup
from livre import Livre
import csv
import os


def recuperationLivre(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    livre = Livre(soup.find('h1').string)
    livre.prix = soup.find("p", class_="price_color").string
    if soup.find(id="product_description") :
        livre.description = soup.find(id="product_description").next_sibling.next_sibling.string
    table = soup.table
    livre.upc = table.td.string
    livre.type = livre.upc.find_next("td").string
    livre.prixHT = livre.type.find_next("td").string
    livre.prix = livre.prixHT.find_next("td").string
    livre.taxe = livre.prix.find_next("td").string
    stock = livre.taxe.find_next("td").string

    for partie in stock.split('('):
        for element in partie.split():
            if element.isdigit():
                livre.nombreStock = int(element)

    if stock.startswith('In stock'):
        livre.stock = True
    else:
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
    print(f"récupération du livre {livre.titre} terminée")
    return livre


def creationDuCsv(name):
    intitules = []
    intitules.append("titre du livre")
    intitules.append("UPC")
    intitules.append("Type")
    intitules.append("Prix HT")
    intitules.append("Prix TTC")
    intitules.append("Taxes")
    intitules.append("Revues")
    intitules.append("En stock")
    intitules.append("Nombre en stock")
    intitules.append("Nombre d'étoiles")
    intitules.append("Catégorie")
    intitules.append("product_description")
    os.makedirs(os.path.join('Données', name), exist_ok=True)
    chemin_fichier_csv = os.path.join('Données', name, f'{name}.csv')
    with open(chemin_fichier_csv, 'w', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(intitules)
        csv_file.close()


def incrementationDuLivre(livre, categorie):
    ligne = [livre.titre, livre.upc, livre.type, livre.prixHT, livre.prix, livre.taxe, livre.revues, livre.stock, livre.nombreStock, livre.note, livre.categorie, livre.description]
    chemin_fichier_csv = os.path.join('Données', categorie, f'{categorie}.csv')
    with open(chemin_fichier_csv, "a", newline="", encoding="utf-8") as f_object:
        writer = csv.writer(f_object)
        writer.writerow(ligne)
        f_object.close()


def recuperationDesLivresDUneCategorie(url, name):
    listeUrlLivres = []
    listeUrlLivrespropre = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    listeBlocPrduits = soup.find_all(class_="image_container")
    for element in listeBlocPrduits:
        lien = element.find('a')
        listeUrlLivres.append(lien.get('href'))

    for element in listeUrlLivres:
        listeUrlLivrespropre.append(element.replace("../../..", "http://books.toscrape.com/catalogue"))

    for element2 in listeUrlLivrespropre:
        livreTemporaire = recuperationLivre(element2)
        incrementationDuLivre(livreTemporaire, name)

    if soup.find(class_="next"):
        pageSuivante = soup.find(class_="next")
        lienPageSuivante = pageSuivante.find_next('a')
        split = lienPageSuivante.get('href').split('.')
        lienpropre = url.replace("index", split[0])
        lienpropre = f"{lienpropre[:-6]}{split[0].split('-')[1]}.html"
        recuperationDesLivresDUneCategorie(lienpropre, name)


def recuperationDesCategoriesEtLivres(url):
    listeUrlsCategories = []
    listeNoms = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    navList = soup.find(class_="nav nav-list")
    listeDesBalisea = navList.find_all("a")
    del(listeDesBalisea[0])
    for element in listeDesBalisea:
        listeUrlsCategories.append(f"https://books.toscrape.com/{element.get('href')}")
        listeNoms.append(element.text.strip())

    for lien, nomcategorie in zip(listeUrlsCategories, listeNoms):
        creationDuCsv(nomcategorie)
        recuperationDesLivresDUneCategorie(lien, nomcategorie)
        print(f'-------------------------------')
        print(f'Document {nomcategorie}.csv est complet')
        print(f'-------------------------------')
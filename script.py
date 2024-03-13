import requests
from bs4 import BeautifulSoup
from livre import Livre
import csv
import os
import time

session = requests.Session()


def recuperationLivre(url):
    page = session.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    livre = Livre(soup.find('h1').string, url)

# Récupération de la description

    if soup.find(id="product_description"):
        livre.description = soup.find(
            id="product_description").next_sibling.next_sibling.string

# Récupération des éléments de la table

    table = soup.table
    livre.upc = table.td.string
    livre.type = livre.upc.find_next("td").string
    livre.prixHT = livre.type.find_next("td").string
    livre.prix = livre.prixHT.find_next("td").string
    livre.taxe = livre.prix.find_next("td").string
    stock = livre.taxe.find_next("td").string

# Double split pour récupérer le nombre dans la chaine de carracatère.
    for partie in stock.split('('):
        for element in partie.split():
            if element.isdigit():
                livre.nombreStock = int(element)

    if stock.startswith('In stock'):
        livre.stock = True
    else:
        livre.stock = False

# Récupération de la note

    blocNote = soup.find(class_="col-sm-6 product_main")
    notation = blocNote.find_next("p").find_next("p").find_next("p")["class"][1]

    match notation:
        case "Five":
            livre.note = 5
        case "Four":
            livre.note = 4
        case "Three":
            livre.note = 3
        case "Two":
            livre.note = 2
        case "One":
            livre.note = 1
        case "Zero":
            livre.note = 0
        case _:
            pass

# récupération de la catégorie

    categorie = soup.ul
    livre.categorie = categorie.find_next(
        "a").find_next("a").find_next("a").string

# Récupération de l'image et intégration de l'image dans le dossier correspondant

    elementImage = soup.find('img')
    urlImage = elementImage['src']
    livre.urlImage = urlImage.replace("../../",
                                "http://books.toscrape.com/")
    imageTéléchargée = session.get(livre.urlImage)
    livre.lienImage = f'{livre.upc}.jpg'
    cheminEnregistrement = os.path.join('Données',
                                        livre.categorie,
                                        livre.lienImage)

    with open(cheminEnregistrement, 'wb') as fichier_image:
        fichier_image.write(imageTéléchargée.content)

    return livre


def creationDuCsv(name):
    intitules = ["product_page_url", "universal_ product_code",
                 "title", "price_including_tax",
                 "price_excluding_tax", "number_available",
                 "product_description", "category",
                 "review_rating", "image_url", "Revues",
                 "Nom fichier image"]

    os.makedirs(os.path.join('Données', name), exist_ok=True)
    chemin_fichier_csv = os.path.join('Données', name, f'{name}.csv')
    with open(chemin_fichier_csv, 'w', encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=intitules)
        writer.writeheader()


def incrementationDuLivre(livre, categorie):
    ligne = [livre.pageUrl, livre.upc, livre.titre, livre.prix,
             livre.prixHT, livre.nombreStock, livre.description,
             livre.categorie, livre.note, livre.urlImage,
             livre.revues, livre.lienImage]
    
    chemin_fichier_csv = os.path.join('Données', categorie, f'{categorie}.csv')
    with open(chemin_fichier_csv, "a", newline="",
              encoding="utf-8") as f_object:
        writer = csv.writer(f_object)
        writer.writerow(ligne)


def recuperationDesLivresDUneCategorie(url, name):
    listeUrlLivres = []
    listeUrlLivrespropre = []
    page = session.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    listeBlocPrduits = soup.find_all(class_="image_container")
    for element in listeBlocPrduits:
        lien = element.find('a')
        listeUrlLivres.append(lien.get('href'))

    for element in listeUrlLivres:
        listeUrlLivrespropre.append(
            element.replace("../../..",
                            "http://books.toscrape.com/catalogue")
            )

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
    tps3 = time.time()
    listeUrlsCategories = []
    listeNoms = []
    page = session.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    navList = soup.find(class_="nav nav-list")
    listeDesBalisea = navList.find_all("a")
    del (listeDesBalisea[0])

    for element in listeDesBalisea:
        listeUrlsCategories.append(
            f"https://books.toscrape.com/{element.get('href')}"
            )
        listeNoms.append(element.text.strip())

    for lien, nomcategorie in zip(listeUrlsCategories, listeNoms):
        creationDuCsv(nomcategorie)
        recuperationDesLivresDUneCategorie(lien, nomcategorie)
        print(f'-------------------------------')
        print(f'Document {nomcategorie}.csv est complet')
        print(f'-------------------------------')
    tps4 = time.time()    
    print(f'-------------------------------')
    print(f'Tous les documents sont créés en {(tps4 - tps3)/60} minutes ')
    print(f'-------------------------------')

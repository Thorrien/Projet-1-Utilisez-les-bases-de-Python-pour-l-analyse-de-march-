from script import recuperationLivre, creationDuCsv, incrementationDuLivre, recuperationDesLivresDUneCategorie, recuperationDesCategoriesEtLivres
from livre import Livre

url = 'https://books.toscrape.com/index.html'

recuperationDesCategoriesEtLivres(url)
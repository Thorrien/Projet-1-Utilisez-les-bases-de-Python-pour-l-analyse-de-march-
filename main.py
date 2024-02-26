from script import recuperationLivre, creationDuCsv, incrementationDuLivre
from livre import Livre

url = 'http://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html'


livre, intitules = recuperationLivre(url)
creationDuCsv(intitules, livre)
incrementationDuLivre(livre)
#livre.__str__()

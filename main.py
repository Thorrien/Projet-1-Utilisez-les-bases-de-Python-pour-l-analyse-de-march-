from script import recuperationLivre
from livre import Livre

url = 'http://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html'


livre = recuperationLivre(url)

livre.__str__()

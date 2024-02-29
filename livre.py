

class Livre:
    def __init__(self, titre, pageUrl):
        self.titre = titre
        self.pageUrl = pageUrl
        self.prix = ""
        self.prixHT = ""
        self.stock = True
        self.nombreStock = 0
        self.note = 0
        self.description = ""
        self.type = ""
        self.taxe = ""
        self.revues = 0
        self.upc = ""
        self.categorie = ""
        self.lienImage = ""
        self.urlImage = ""

    def __str__(self):
        print(f"Titre : {self.titre}")
        print(f"UPC : {self.upc}")
        print("------------------------------------------------")
        print(f"Prix TTC : {self.prix}")
        print(f"Prix HC: {self.prixHT}")
        print(f"taxe : {self.taxe}")
        print(f"En stock : {self.stock}")
        print(f"Nombre en Stock : {self.nombreStock}")
        print(f"Note : {self.note}")
        print(f"Revues : {self.revues}")
        print(f"type : {self.type}")
        print(f"taxe : {self.taxe}")
        print(f"categorie : {self.categorie}")
        print("------------------------------------------------")
        print(f"Description : {self.description}")

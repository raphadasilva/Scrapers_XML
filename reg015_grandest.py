from lxml import etree
import json

departements = ["08", "10","51","52","54", "55", "57", "67", "68", "88"] # là on met nos différents codes départementaux
liste_objets = [] # on va remplir cette liste de dictionnaires au fur et à mesure, avant de la convertir en tableau d'objets JS

for departement in departements:
	arbre = etree.parse("http://www.interieur.gouv.fr/avotreservice/elections/telechargements/RG2015/resultatsT2/44/44"+departement+"/44"+departement+"000.xml") # la structure des dossiers où sont rangés les xml nous permet d'automatiserleur interrogation
	print ("Department numero "+departement)
	for noeud in arbre.xpath("//Election/Region/SectionElectorale/Communes/Commune"): # on se place sur le noeud principal, et on déroule
		objet = {} 
		for insee in noeud.xpath("CodSubCom"):
			objet["code insee"] = departement+insee.text # on implémente notre dictionnaire au fur et à mesure
		for commune in noeud.xpath("LibSubCom"):
			objet["ville"] = commune.text
		for resultats in noeud.xpath("Tours/Tour[NumTour=2]"):
			for inscrits in resultats.xpath("Mentions/Inscrits/Nombre"):
				objet["inscrits"] = int(inscrits.text) # text renvoie par défaut une chaîne de cara', du coup on convertit en chiffre certaines valeurs
			for abstentions in resultats.xpath("Mentions/Abstentions/Nombre"):
				objet["abstentions"] = int(abstentions.text)
			for exprimes in resultats.xpath("Mentions/Exprimes/Nombre"):
				objet["exprimes"] = int(exprimes.text)
			for liste in resultats.xpath("Listes/Liste"):
				for nuance in liste.xpath("CodNuaListe"):
					nu = nuance.text
				for voix in liste.xpath("NbVoix"):
					vox = int(voix.text)
				objet[nu] = vox # et vlà le travail !
			print(objet)
			liste_objets.append(objet) # on met à jour la liste chaque fois qu'une boucle dans le noeud principal est achevé

ficjson = open('reg015_grandest.json','w+') # on crée notre json
ficjson.write(json.dumps(liste_objets)) # et on convertit notre liste. Terminé !

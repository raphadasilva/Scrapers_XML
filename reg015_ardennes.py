from lxml import etree
import json

arbre = etree.parse("http://www.interieur.gouv.fr/avotreservice/elections/telechargements/RG2015/resultatsT2/44/4408/4408000.xml")
ardennes = "08"
liste_objets = [] # cette liste contiendra plein de dictionnaire, on la convertira en tableau d'objets JS à la fin

# on interroge chaque noeud principal de notre arbre pour pouvoir faire ensuite des sélections sur des sous-noeuds précis
for noeud in arbre.xpath("//Election/Region/SectionElectorale/Communes/Commune"):
	objet = {} # ce dictionnaire va rassembler toutes les informations qui nous intéressent
	for insee in noeud.xpath("CodSubCom"):
		objet["code insee"] = ardennes+insee.text # là on reconstitue le code INSEE complet
	for commune in noeud.xpath("LibSubCom"):
		objet["ville"] = commune.text
	for resultats in noeud.xpath("Tours/Tour[NumTour=2]"):
		for inscrits in resultats.xpath("Mentions/Inscrits/Nombre"):
			objet["inscrits"] = int(inscrits.text) # par défaut, text renvoie une chaîne de cara', donc on convertit
		for abstentions in resultats.xpath("Mentions/Abstentions/Nombre"):
			objet["abstentions"] = int(abstentions.text)
		for exprimes in resultats.xpath("Mentions/Exprimes/Nombre"):
			objet["exprimes"] = int(exprimes.text)
		for liste in resultats.xpath("Listes/Liste"):
			for nuance in liste.xpath("CodNuaListe"):
				nu = nuance.text
			for voix in liste.xpath("NbVoix"):
				vox = int(voix.text)
			objet[nu] = vox # et voilà le travail
	print(objet)
	liste_objets.append(objet) # on incrémente notre liste à chaque fois

ficjson = open('reg015_ardennes.json','w+')
ficjson.write(json.dumps(liste_objets)) # plus qu'à convertir la liste en json et le tour est joué !

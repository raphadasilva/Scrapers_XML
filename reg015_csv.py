from lxml import etree
import csv

departements = ["08", "10","51","52","54", "55", "57", "67", "68", "88"]
ficsv = open('reg015_grandest.csv', 'w')

try:
	majcsv = csv.DictWriter(ficsv, ['code insee', 'ville', 'inscrits', 'abstentions', 'exprimes', 'LDVG', 'LFN', 'LUD'])
	majcsv.writeheader()
	for departement in departements:
		arbre = etree.parse("http://www.interieur.gouv.fr/avotreservice/elections/telechargements/RG2015/resultatsT2/44/44"+departement+"/44"+departement+"000.xml")
		print ("Departement numero "+departement)
		for noeud in arbre.xpath("//Election/Region/SectionElectorale/Communes/Commune"):
			objet = {}
			for insee in noeud.xpath("CodSubCom"):
				objet["code insee"] = departement+insee.text
			for commune in noeud.xpath("LibSubCom"):
				objet["ville"] = commune.text
			for resultats in noeud.xpath("Tours/Tour[NumTour=2]"):
				for inscrits in resultats.xpath("Mentions/Inscrits/Nombre"):
					objet["inscrits"] = int(inscrits.text)
				for abstentions in resultats.xpath("Mentions/Abstentions/Nombre"):
					objet["abstentions"] = int(abstentions.text)
				for exprimes in resultats.xpath("Mentions/Exprimes/Nombre"):
					objet["exprimes"] = int(exprimes.text)
				for liste in resultats.xpath("Listes/Liste"):
					nu = ""
					vox = 0
					for nuance in liste.xpath("CodNuaListe"):
						nu = nuance.text
					for voix in liste.xpath("NbVoix"):
						vox = int(voix.text)
					objet[nu] = vox
				print(objet)
				majcsv.writerow(objet)
finally:
	ficsv.close()
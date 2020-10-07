import csv
from rdflib import Graph, Literal, Namespace, URIRef

nomDuFichier = input("Saisir le nom du fichier (doit être en .csv): ")

#Variables à modifier pour sélectionner le fichier de données-----------------------------------------------------------
input_file = list(csv.reader(open(nomDuFichier)))
#When left blank all entities will be of type owl:thing or add type relations when a csv header is "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" the subjects will then be assigned the values in this column as object
subjectsClassName = "Montagne"
#------------------------------------------------------------------------------------------------------------------

# #_______________On demande si il y a des titres <----- Fonction non prise en charge
# title=int(input("Les colonnes ont-elles des titres ? 1 pour oui, 0 pour non\nRéponse : "))
# if title==1:
#     #Demander le numéro de la ligne des titres (on applique un -1 sur la valeur entrée car lignes vont de 0 à n)
#     titleRow=int(input("Saisir le numéro de la ligne contenant les titres du fichier csv :\nRéponse :  "))-1


#________________Demander la premiere ligne de valeurs (on applique un -1 sur la valeur entrée car lignes vont de 0 à n)
ligneDuTitre = int(input("Saisir le numéro de la première ligne de valeur : "))-1


#________________On demande si on veut saisir la dernière ligne
derniereLigne=int(input("Voulez-vous saisir la dernière ligne ? 1 pour oui, 0 pour non\nRéponse : "))

if derniereLigne==1:
    #Demander le numéro de la dernière ligne (on applique un -1 sur la valeur entrée car lignes vont de 0 à n)
    ligneFinale=int(input("Saisir le numéro de la dernière ligne :\nRéponse :  "))
else:
	ligneFinale=len(input_file)



#définit le préfixe en début de fichier

prefix = ("http∶//ex.org/pred/")
g = Graph()
ex = Namespace(prefix)
g.bind("pred", ex)
rowIndex = 0

#Première ligne



#ligneDuTitre = 0
ligneDuDebut = ligneDuTitre

print("ligneDuDebut = "+str(ligneDuDebut))
print("ligneDuTitre = "+str(ligneDuTitre))
print("ligneFinale = "+str(ligneFinale))



#for row in input_file:

for i in range(ligneDuDebut, ligneFinale):
	
	colIndex = 0
	#premier element de chaque ligne = sujet
	subj = URIRef(input_file[i][1])
	
	#  Définit les prédicats
	if subjectsClassName != "":
		g.add(  (subj, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef(prefix+subjectsClassName))  )



	if rowIndex > 0:
		for colVal in input_file[i]:
			#print("colVal = "+colVal)
			if colIndex > 0:
				name = prefix + input_file[ligneDuTitre][colIndex]
				pred = URIRef(name)
				if colVal != "":
					if not colVal.__contains__(" ") and colVal.__contains__("dbpedia"):
						obj = URIRef(colVal)
					else:
						obj = Literal(colVal)
					g.add((subj, pred, obj))
			#colonne suivante
			colIndex+=1
	#ligne suivante
	rowIndex+=1

g.serialize(destination='turtle.ttl', format='turtle')
print("Le fichier a bien été généré.")
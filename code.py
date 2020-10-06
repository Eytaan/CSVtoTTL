import csv
from rdflib import Graph, Literal, Namespace, URIRef

#Only modify these variables when using as a normal user-----------------------------------------------------------
input_file = list(csv.reader(open("data.csv")))

#When left blank all entities will be of type owl:thing or add type relations when a csv header is "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" the subjects will then be assigned the values in this column as object
subjectsClassName = "Montagne"
#------------------------------------------------------------------------------------------------------------------

#a=input("Saisir le numéro de la ligne contenant les titres du fichier csv: ")

prefix = ("http∶//ex.org/pred/")
# make a graph
g = Graph()
ex = Namespace(prefix)
g.bind("pred", ex)

rowIndex = 0
for row in input_file:
	colIndex = 0
	subj = URIRef(row[0])
	 #add class to all if wanted
	if subjectsClassName != "":
		g.add(  (subj, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef(prefix+subjectsClassName))  )
	
	#First row
	if rowIndex==0:
		colIndex2 = 0
		for colVal in row:
			if colIndex2 > 0:
				cellBelow = input_file[rowIndex+1][colIndex2]
				isObject = not cellBelow.__contains__(" ") and cellBelow.__contains__("dbpedia")
				name =prefix + colVal
				colIndex2+=1

	if rowIndex > 0:
		for colVal in row:
			if colIndex > 0:
				name = prefix + input_file[0][colIndex]
				pred = URIRef(name)
				if colVal != "":
					if not colVal.__contains__(" ") and colVal.__contains__("dbpedia"):
						obj = URIRef(colVal)
					else:
						obj = Literal(colVal)
					g.add((subj, pred, obj))
			colIndex+=1
	rowIndex+=1

g.serialize(destination='turtle.ttl', format='turtle')

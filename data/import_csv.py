import csv
with open ("/Users/gwenaellepatat/Desktop/Appli_Lettres/import_csv.py", newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader :
    	print(row)
    	print(', '.join(row))
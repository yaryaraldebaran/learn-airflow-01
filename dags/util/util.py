import csv

with open("../data/a.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
    print(row)
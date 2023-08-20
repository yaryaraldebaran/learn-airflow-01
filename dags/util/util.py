import csv
data_list = []

def input_sql_from_csv():
    with open("../data/data_city.csv", 'r') as file:
        csvreader = csv.DictReader(file)
        for row in csvreader:
            data_list.append(row)
    return data_list

# for data_dict in data_list:
#   print(data_dict)
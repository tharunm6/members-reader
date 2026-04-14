import csv

with open("members.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['first_name']} {row['last_name']}")

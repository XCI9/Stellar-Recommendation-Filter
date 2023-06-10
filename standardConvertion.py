import csv

year = 110

with open('standard/input.txt',encoding='utf8') as input, open(f'{year}_standard.csv','w',encoding='utf8', newline='') as csvFile:
    output = csv.writer(csvFile)


    lines = input.readlines()

    for line in lines:
        subject, highest, higher, mid, lower, lowest = line.strip('\n').split(' ')

        output.writerow([year, subject, highest, higher, mid, lower, lowest])
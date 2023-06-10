import csv
from collections import deque

department = {}
index = 1
with open("main.csv", "w", encoding = 'utf8', newline='') as csvOut:
    output = csv.writer(csvOut)
    for year in range(104,111):
        with open(f"{year}.csv", newline='', encoding = 'utf8') as csvFile:
            input = csv.reader(csvFile)

            for line in input:
                line = deque(line)
                schoolId = line[0]
                departmentId = line[1]
                name = line[2].split('【外加】')

                if len(name) == 1:
                    addition = 0
                elif len(name) == 2:
                    addition = 1
                else:
                    raise Exception("Should not reach here.")

                name = name[0]

                if not department.get(schoolId):
                    department[schoolId] = {}
                if not department[schoolId].get(name):
                    department[schoolId][name] = index
                    index += 1

                line.popleft()
                line.popleft()
                line.popleft()

                line.appendleft(addition)
                line.appendleft(department[schoolId][name])
                #line.appendleft(name)
                #line.appendleft(schoolId)
                line.appendleft(year)

                output.writerow(line)

with open("department.csv", "w", encoding = 'utf8', newline='') as csvOut:
    output = csv.writer(csvOut)

    for school,departments in department.items():
        for department, id in departments.items():
            output.writerow([id,school,department])




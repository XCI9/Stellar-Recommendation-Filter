import tabula
import csv
import os

def theshold2int(theshold):
    if theshold == '頂標': return 5
    if theshold == '前標': return 4
    if theshold == '均標' or theshold == 'A級': return 3
    if theshold == '後標' or theshold == 'B級': return 2
    if theshold == '底標' or theshold == 'C級': return 1
    raise Exception("should not reach here.")

def outputFormat(data):
    schoolID, id, name, finalCount, wantCount, theshold, compareRule, firstStageCount, firstCompare,secondStageCount,secondCompare = data
    
    subjects = ['國文','英文','數學','社會','自然','總級分','英聽']
    subjectStandard = []
    for subject in subjects:
        if theshold.get(subject):
            subjectStandard.append(theshold2int(theshold[subject]))
        else:
            subjectStandard.append(0)

    if len(firstCompare) != len(compareRule) or len(secondCompare) != len(compareRule):
        raise Exception("compare not match!")

    while len(compareRule) < 7:
        compareRule.append('')
        secondCompare.append('')
        firstCompare.append('')

    #firstCompareOutput = []
    #for compare in firstCompare:
    #    firstCompareOutput.append(compare[0])
    #    firstCompareOutput.append(compare[1])
#
    #while len(secondCompare) < 7:
    #    secondCompare.append(('',''))
#
    #secondCompareOutput = []
    #for compare in secondCompare:
    #    secondCompareOutput.append(compare[0])
    #    secondCompareOutput.append(compare[1])


    return schoolID, id, name, finalCount, wantCount, *subjectStandard,  *compareRule, \
           firstStageCount, *firstCompare, secondStageCount,*secondCompare 

    



#year = 107

for year in range(110,109,-1):
    files = []
    for dirPath, dirNames, fileNames in os.walk(f"./pdf/{year}/"):
        for f in fileNames:
            files.append(os.path.join(dirPath, f))


    with open(f'{year}.csv','w',encoding='utf8', newline='') as csvFile, open('except.csv','w',encoding='utf8') as exceptFile:
        writer = csv.writer(csvFile)
        exceptCSV = csv.writer(exceptFile)

        for file in files:
            print(f'\nopen {file}.')
            schoolID = file.split('_')[-1].split('.')[0]
            pages = tabula.read_pdf(file, pages="all", format="csv", silent=True)

            #print(page)
            for page in pages:
                    page.to_csv("test.csv")

                    with open("test.csv", encoding="utf8") as csvfile:
                        rows = csv.reader(csvfile)

                        for row in rows:
                            if len(row) == 14:
                                shift = 0
                            elif len(row) == 13:
                                shift = -1
                            else:
                                raise Exception("should not reach here!")
                            break

                        i = 0
                        header = True
                        exception = False
                        for row in rows:
                            try:
                                if header and row[6+shift] != '國文':
                                    continue
                                else:
                                    header = False

                                if i == 0:
                                    theshold = {}
                                    firstCompare = []
                                    secondCompare = []
                                    compareRule = []


                                if row[7+shift] != '' and row[7+shift] != '--' and row[7+shift] != '-- --':
                                    theshold[row[6+shift]] = row[7+shift].split(' ')[0]

                                if row[9+shift] != '' and row[9+shift] != '--' and row[9+shift] != '-- --':
                                    theshold[row[8+shift]] = row[9+shift].split(' ')[0]
    

                                if row[10+shift] != '':
                                    compareRule.append(row[10+shift])

                                    firstCompareResult = row[11+shift].split(" ")[-1]
                                    if firstCompareResult != '' and firstCompareResult != '--':
                                        firstCompare.append(firstCompareResult)
                                    else:
                                        firstCompare.append('')

                                    if row[13+shift] != '' and row[13+shift] != '--':
                                        secondCompare.append(row[13+shift])
                                    else:
                                        secondCompare.append('')


                                if i == 3:
                                    id = row[1]
                                    if not exception:
                                        name = row[2]
                                    wantCount = int(row[4+shift])
                                    finalCount = int(row[5+shift])
                                    firstStageCount = int(row[11+shift].split(' ')[0])
                                    if row[12+shift] != '--':
                                        secondStageCount = int(row[12+shift])
                                    else:
                                        secondStageCount = 0

                                if exception and i == 4:
                                    exception = False
                                    name += row[2]

                                if i == 6:
                                    output = outputFormat([schoolID, id, name, finalCount, wantCount, theshold, compareRule, firstStageCount, firstCompare,secondStageCount,secondCompare])
                                    writer.writerow(output)
                                    print(f"{id}-{name}:{finalCount}/{wantCount}, {theshold},"
                                          f"Rule : {compareRule}"
                                          f" first round:{firstStageCount}, {firstCompare};"
                                          f"sceond round:{secondStageCount}, {secondCompare}")

                                    i = 0
                                else:
                                    i += 1
                            except:
                                exceptCSV.writerow(row)
                                exception = True
                                name = row[2]


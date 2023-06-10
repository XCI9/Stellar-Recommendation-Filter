import psycopg2

def getRank(standard, score):
    if score >= standard[0]: return 5
    if score >= standard[1]: return 4
    if score >= standard[2]: return 3
    if score >= standard[3]: return 2
    if score >= standard[4]: return 1
    return 0

def convert2keyword(data):
    output = []
    for str in data:
        outString = '%'
        for char in str:
            outString += char + '%'
        output.append(outString)
    return output

def theshold2Str(theshold):
    if theshold == 0: return 'x '
    if theshold == 1: return '底'
    if theshold == 2: return '後'
    if theshold == 3: return '均'
    if theshold == 4: return '前'
    if theshold == 5: return '頂'
    raise Exception("Error!")

def listeningTheshold2Str(theshold):
    if theshold == 0: return 'x '
    if theshold == 1: return 'C'
    if theshold == 2: return 'B'
    if theshold == 3: return 'A'
    raise Exception("Error!")


print("正在連接到資料庫...")
conn = psycopg2.connect(host="db20220410hw1.coqd9yey4uqv.us-east-1.rds.amazonaws.com", dbname = "finalProject",
                        user="chenyutse", password="141zn69tan")
print("連接成功")
cursor = conn.cursor()
conn.autocommit = True

while True:
    chinese = int(input("請輸入國文級分:"))
    english = int(input("請輸入英文級分:"))
    math    = int(input("請輸入數學級分:"))
    society = int(input("請輸入社會級分:"))
    science = int(input("請輸入自然級分:"))
    listening = input("請輸入英聽等第(A/B/C/F):")
    scoreInSchool = int(input("請輸入校排%:"))

    if   listening == 'A': listeningRank = 3
    elif listening == 'B': listeningRank = 2
    elif listening == 'C': listeningRank = 1
    elif listening == 'F': listeningRank = 0


    showAddition = input("是否顯示外加名額(Y/N)?")

    schoolRestrict = input("請輸入學校關鍵字(多所學校以','分隔):")
    schoolRestrict = convert2keyword(schoolRestrict.split(','))

    departmentRestrict = input("請輸入科系關鍵字(多個科系以','分隔):")
    departmentRestrict = convert2keyword(departmentRestrict.split(','))
    stage = int(input("請選擇一輪或二輪(1/2):"))

    print("請稍後...")
    total = chinese + english + math + society + science

    #是否顯示外加名額
    if showAddition == '':
        additionConstraint = ''
    elif showAddition == 'Y':
        additionConstraint = 'and isaddition = true'
    elif showAddition == 'N':
        additionConstraint = 'and isaddition = false'
    
    #學校關鍵字
    schoolConstraint = ''
    if len(schoolRestrict) > 0:
        schoolConstraint = 'where '
        for restrict in schoolRestrict:
            schoolConstraint += f"school.name like '{restrict}' or "
        schoolConstraint = schoolConstraint[:-4]
    
    #科系關鍵字
    departmentConstraint = ''
    if len(departmentRestrict) > 0:
        departmentConstraint = ' and ('
        for restrict in departmentRestrict:
            departmentConstraint += f"name like '{restrict}' or "
        departmentConstraint = departmentConstraint[:-4] + ')'
    
    #1/2輪
    if stage == 2:
        stageRow = 'secondStageCount, secondStageRule1, secondStageRule2, secondStageRule3, secondStageRule4, secondStageRule5, secondStageRule6, secondStageRule7'
    else:
        stageRow = 'firstStageCount, firstStageRule1, firstStageRule2, firstStageRule3, firstStageRule4, firstStageRule5, firstStageRule6, firstStageRule7'

    cursor.execute("select distinct year from standard order by year desc")
    results = []
    for year in cursor.fetchall():
        year = year[0]
        cursor.execute(f"select * from standard where year = {year} and subject = '國文'")
        chineseStd = cursor.fetchall()[0][2:]
        chineseRank = getRank(chineseStd, chinese)

        cursor.execute(f"select * from standard where year = {year} and subject = '英文'")
        englishStd = cursor.fetchall()[0][2:]
        englishRank = getRank(englishStd, english)

        cursor.execute(f"select * from standard where year = {year} and subject = '數學'")
        mathStd = cursor.fetchall()[0][2:]
        mathRank = getRank(mathStd, math)

        cursor.execute(f"select * from standard where year = {year} and subject = '社會'")
        societyStd = cursor.fetchall()[0][2:]
        societyRank = getRank(societyStd, society)

        cursor.execute(f"select * from standard where year = {year} and subject = '自然'")
        scienceStd = cursor.fetchall()[0][2:]
        scienceRank = getRank(scienceStd, science)

        if year < 108:
            cursor.execute(f"select * from standard where year = {year} and subject = '總級分'")
            totalStd = cursor.fetchall()[0][2:]
            totalRank = getRank(totalStd, total)
        else:
            totalRank = 0

        query = ('select '
        'year, school.name, main.name, isaddition, wantcount, finalcount,'
        'chineseTheshold, englishTheshold, mathTheshold, scienceTheshold, societyTheshold, totalTheshold, listeningTheshold,'
        'CompareRule1, CompareRule2, CompareRule3, CompareRule4, CompareRule5, CompareRule6, CompareRule7,'
        + stageRow +\
        ' from('
        '  select year, schoolId, name, isaddition, wantcount, finalcount,'
        '  chineseTheshold, englishTheshold, mathTheshold, scienceTheshold, societyTheshold, totalTheshold, listeningTheshold,'
        '  CompareRule1, CompareRule2, CompareRule3, CompareRule4, CompareRule5, CompareRule6, CompareRule7,'
        + stageRow +\
        '  from main '
        '  join'
        '  (select * from department) as department '
        '  on main.departmentId = department.id '
        f'  where chineseTheshold <= {chineseRank} and englishTheshold <= {englishRank} '
        f'  and mathTheshold <= {mathRank} and scienceTheshold <= {scienceRank} and societyTheshold <= {scienceRank} and totalTheshold <= {totalRank} '
        f' and year = {year} '
        + additionConstraint + departmentConstraint + ') as main '
        'join'
        '(select * from school) as school '
        'on school.id = main.schoolId ' 
        + schoolConstraint +\
        ' order by school.name')

        cursor.execute(query)

        results += cursor.fetchall()

    if len(results) == 0:
        print("無符合的搜尋結果，請確認輸入無誤或放寬篩選條件")

    for year, school, department, isAddition, finalCount, wantCount,\
        chineseTheshold, englishTheshold, mathTheshold, societyTheshold, scienceTheshold,\
        totalTheshold, listeningTheshold, \
        compareRule1, compareRule2, compareRule3, compareRule4, compareRule5, compareRule6, compareRule7,\
        stageCount, stageRule1, stageRule2, stageRule3, stageRule4, stageRule5, stageRule6, stageRule7 \
         in results:
        compareRule = [compareRule1, compareRule2, compareRule3, compareRule4, compareRule5, compareRule6, compareRule7]
        stageRule = [stageRule1, stageRule2, stageRule3, stageRule4, stageRule5, stageRule6, stageRule7]

        while len(compareRule) > 0 and compareRule[-1] is None:
            compareRule.pop()
            stageRule.pop()

        while len(stageRule) > 0 and stageRule[-1] is None:
            compareRule.pop()
            stageRule.pop()

        valid = True
        for i in range(len(compareRule)):
            if '學測' in compareRule[i]:
                total = 0
                if '國' in compareRule[i]:
                    total += chinese
                if '英' in compareRule[i]:
                    total += english
                if '數' in compareRule[i]:
                    total += math
                if '社' in compareRule[i]:
                    total += society
                if '自' in compareRule[i]:
                    total += science

                if total < int(stageRule[i].split('*')[0]) and stage == 2:
                    valid = False
                    break
                elif total < int(stageRule[i].split('*')[0]) and stage == 1 and wantCount > stageCount:
                    valid = False
                    break
            if compareRule[i] == '在校學業':
                if scoreInSchool > int(stageRule[i].split('%')[0].split('*')[0]):
                    valid = False
                    break
        if not valid:
            continue
        else:
            outputMsg = f"({year}){school}-{department}"

            if isAddition:
                outputMsg += "(外加)"

            tab = int((36 - len(outputMsg))/2)
            if isAddition:
                tab -= 2
            for i in range(tab,0,-2):
                outputMsg += '\t'

            outputMsg += f" {finalCount:2}/{wantCount:2}"
            outputMsg += (f" {theshold2Str(chineseTheshold)} {theshold2Str(englishTheshold)}"
            f" {theshold2Str(mathTheshold)} {theshold2Str(societyTheshold)}"
            f" {theshold2Str(scienceTheshold)} {theshold2Str(totalTheshold)}"
            f" {listeningTheshold2Str(listeningTheshold)} ")

            for i in range(len(compareRule)):
                outputMsg += f"{compareRule[i]}({stageRule[i]})"

            print(outputMsg)
    print()











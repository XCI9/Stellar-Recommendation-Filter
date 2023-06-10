with open('standard.csv','w',encoding='utf8') as output:
    for year in range(104,111):
        with open(f'standard/{year}_standard.csv',encoding='utf8') as input:
            output.write(input.read())

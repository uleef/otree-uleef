import os
import pandas as pd
import xlrd
import csv

## use this code to gerate integer lists


# INTS1book = xlrd.open_workbook('INTS1.xls')
# INTS1 = INTS1book.sheet_by_index(0)
# INTS2book = xlrd.open_workbook('INTS2.xls')
# INTS2 = INTS2book.sheet_by_index(0)
# integer1Array = []
# integer2Array = []
#
# for i in range (INTS1.nrows):
#     integer1Array.append([INTS1.cell_value(i,0),INTS1.cell_value(i,1)])
#
# print(integer1Array)
# print()
# print()
#
#
# for i in range (INTS2.nrows):
#     integer2Array.append([INTS2.cell_value(i,0),INTS2.cell_value(i,1)])
#
# print(integer2Array)


df = pd.read_excel('nametags.xlsx', 'A Names')

print(df.head())

total_payoffs = {3: [0.75, 0.75, 0.0, 0.0, 0.0, 0.0, 0.0], 6: [0.0, 0.75, 0.0, 0.0, 0.0, 0.0, 0.0], 9: [0.75, 0.75, 0.0, 0.0, 0.0, 0.0, 0.0], 12: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}


df.to_csv('Results/TestCSV.csv')

if os.path.isfile('Results/TestCSV.csv'):
    with open('Results/TestCSV.csv', 'a') as testCSV:
        test_writer = csv.writer(testCSV, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        test_writer.writerow([])
        test_writer.writerow(['hello, world','this is it on two lines','heres another on a sperate line'])
        test_writer.writerow(['dictionary'])
        test_writer.writerow([str(total_payoffs)])
        test_writer.writerow(['dictionary iterated over'])
        scoreArray = []
        for key in total_payoffs:
            scoreArray.append(key)
            for value in total_payoffs[key]:
                scoreArray.append(value)
            scoreArray.append('\n')
        test_writer.writerow(scoreArray)


for key in total_payoffs:
    print(key)
    for value in total_payoffs[key]:
        print(value)
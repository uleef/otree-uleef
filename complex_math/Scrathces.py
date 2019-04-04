import os
import pandas as pd
import xlrd

## use this code to gerate integer lists


INTS1book = xlrd.open_workbook('INTS1.xls')
INTS1 = INTS1book.sheet_by_index(0)
INTS2book = xlrd.open_workbook('INTS2.xls')
INTS2 = INTS2book.sheet_by_index(0)
integer1Array = []
integer2Array = []

for i in range (INTS1.nrows):
    integer1Array.append([INTS1.cell_value(i,0),INTS1.cell_value(i,1)])

print(integer1Array)
print()
print()


for i in range (INTS2.nrows):
    integer2Array.append([INTS2.cell_value(i,0),INTS2.cell_value(i,1)])

print(integer2Array)
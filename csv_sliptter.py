import csv
import glob, os
import pandas as pd
from typing import List
from time import sleep

# save_path = '/home/guest/Desktop/Application/runtime/hai-22.04/' + filename + ".csv"
# file1 = open(save_path, "w")


file = open('test_data_file.csv', 'r')
header = file.readline()
csvfile = file.readlines()
filename = 1
batch_size = 10000
for i in range(len(csvfile)):
    if i % batch_size == 0:
        open(str(filename) + '.csv', 'w+').writelines(header)
        open(str(filename) + '.csv', 'a+').writelines(csvfile[i:i + batch_size])
        filename += 1
    #print(filename)







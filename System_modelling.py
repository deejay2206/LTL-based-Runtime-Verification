import csv
import glob, os
import pandas as pd
from typing import List
from time import sleep


#file = open('output23_file.csv', 'r')
#header = file.readline()
#csvfile = file.readlines()
#filename = 1
#batch_size = 20
#for i in range(len(csvfile)):
#        if i % batch_size == 0:
#                open(str(filename) + '.csv', 'w+').writelines(header)
#                open(str(filename) + '.csv', 'a+').writelines(csvfile[i:i+batch_size])
#                filename += 1
#        #print(filename)

with open("4.csv", "r") as f:
    os.system("python3 runtime-monitor.py -i 7")
    data = csv.reader(f)
    #print(data)
    row: list[int]
    str1 = ""
    next(data, None)  # skip the headers
    # headers = next(data, None) #returns the headers or 'None' if the input is empty (write header to the output file unprocessed)
    # if headers:
    # write.writerow(headers)

    for row in data:
        print(row)
        ints = [round(float(s)) for s in row]
        # print(ints)
        # print(len(ints))
        # print(type(ints))

        os.system(
            "python3 runtime-monitor.py -a {} {} {} {} {} {} {} ".format(ints[0], ints[1], ints[2],ints[3], ints[4], ints[5], ints[6]))
        ## Waiting time to process (1sec)
        # sleep(1)

f.close()

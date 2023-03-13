import csv
import glob, os
import pandas as pd
from typing import List
from time import sleep

# save_path = '/home/guest/Desktop/Application/runtime/hai-22.04/' + filename + ".csv"
# file1 = open(save_path, "w")


with open("1.csv", "r") as df:
df = pd.read_csv('1.csv', index_col=0)
#print(df)

os.system("python3 runtime-monitor.py -i 45")
data = csv.reader(df)
row: list[int]
str1 = ""
next(data, None)  # skip the headers
# headers = next(data, None) #returns the headers or 'None' if the input is empty (write header to the output file unprocessed)
# if headers:
# write.writerow(headers)

for row in data:
    ints = [round(float(s)) for s in row]
    # print(ints)
    # print(len(ints))
    # print(type(ints))

    os.system(
        "python3 runtime-monitor.py -a {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} ".format(
            ints[0], ints[1], ints[2], ints[3], ints[4], ints[5], ints[6], ints[7], ints[8], ints[9], ints[10],
            ints[11], ints[12], ints[14], ints[15], ints[16], ints[17], ints[18], ints[19], ints[20], ints[21],
            ints[22], ints[23], ints[24], ints[25], ints[26], ints[27], ints[28], ints[29], ints[30], ints[31],
            ints[32], ints[33], ints[34], ints[35], ints[36], ints[37], ints[38], ints[39], ints[40], ints[41],
            ints[42], ints[43], ints[44], ints[45]))
    ## Waiting time to process (1sec)
    # sleep(1)

    df.close()





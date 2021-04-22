import os
import pandas as pd
from RNA import Rna


# Loads all the sequences into the dataset from a folder with .seq and .ct files.
def load_sequences(folder):
    sequence_list = []
    pos = 0
    for filename in sorted(os.listdir(folder), reverse=True):
        #print(filename)
        if filename.endswith(".seq"):
            file = open(folder + "/" + filename)
            lines = file.readlines()
            seqname = lines[1].split()[0]
            seq = lines[2][:-2]
            sequence_list.append(Rna(seqname, seq, 0))
            pos = pos + 1

        if filename.endswith(".ct"):
            file = folder + "/" + filename
            dataframe = pd.read_table(file, sep="\t", header = None, index_col=0, skiprows=1)
            dataframe.rename(columns={1: "base", 4: "base_pair"}, inplace = True)
            dataframe.drop([2,3,5], axis = 1, inplace = True)

            sequence_list[pos-1].update_structure(dataframe)

    return list(sequence_list)








""" print("Begining load_dataset test.")
path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "/Databases/archiveII"
#print(path)
testList = load_sequences(path)
print("RNA samples number: ", len(testList))

print(" ")
print("Samples: ")
print("RNA Sample: ", testList[1].name)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(testList[1].structure.head())

print(" ")
print("RNA Sample: ", testList[5].name)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(testList[5].structure.head())

print(" ")
print("RNA Sample: ", testList[10].name)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(testList[10].structure.head()) """





             


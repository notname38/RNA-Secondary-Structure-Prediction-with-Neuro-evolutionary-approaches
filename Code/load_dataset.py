import os
import pandas as pd
from RNA import Rna

def load_dataframe(file):
    dataframe = pd.read_table(file, sep="\t", header = None, index_col=0, skiprows=1)
    dataframe.rename(columns={1: "base", 4: "base_pair"}, inplace = True)
    dataframe.drop([2,3,5], axis = 1, inplace = True)
    dataframe = dataframe.iloc[0:]
    return dataframe



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
            #if seqname == "lcaligenes-sp--1":
            #    print(filename)
            seq = lines[2][:-2]
            sequence_list.append(Rna(seqname, seq, 0))
            pos = pos + 1

        if filename.endswith(".ct"):
            file = folder + "/" + filename
            dataframe = load_dataframe(file)
            sequence_list[pos-1].update_structure(dataframe)

    return list(sequence_list)


# Usefull for models that save results as CT tables.
# Creates predicted RNA objects
def load_ct_only(folder):
    aux_list = []
    for filename in sorted(os.listdir(folder), reverse=True):
        file = folder + "/" + filename
        dataframe = load_dataframe(file)
        element = Rna(filename[:-3], "prediction", 0)
        element.update_structure(dataframe)
        aux_list.append(element)

    return list(aux_list)










# print("Begining load_dataset test.")
# path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "/Databases/archiveII"
# #print(path)
# testList = load_sequences(path)
# print("RNA samples number: ", len(testList))

# test_set = [ 
#     "A_Anab-vari-_CP000117_1-390",
#     "Rhod-rubr-_CP000230",
#     "lcaligenes-sp--1",
#     "rtemia-sp--1"
# ]

# test_set = ["Rhod-rubr-_CP000230"]

# print(" ")
# print("Samples: ")
# print(" ")
# for elem in testList:
#     if elem.name in test_set:
#         testelem = elem
#         print("RNA Sample: ", testelem.name)
#         #with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#         #    print(testelem.structure.head())
#         print(*testelem.structure["base_pair"].tolist())
#         print(" ")
#         print(len(testelem.structure["base_pair"].tolist()))
#         print(" ")






             


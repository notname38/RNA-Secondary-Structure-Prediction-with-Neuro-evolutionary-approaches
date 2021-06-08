import os
import pandas as pd
from pandas.errors import ParserError

def load_dataframe(file):
    dataframe = pd.read_csv(file,header = None, index_col=0, sep='\s+')
    dataframe.rename(columns={1: "base", 4: "base_pair"}, inplace = True)
    dataframe.drop([2,3,5], axis = 1, inplace = True)
    dataframe = dataframe.iloc[0:]
    return dataframe

def write_on_file(dataframe, name):
    ind = 1
    namefile = "bpseq_database/" + name + ".bpseq"
    f = open(namefile, "w")
    for index, row in dataframe.iterrows():
        line = str(ind) + " " + str(row["base"]) + " " + str(row["base_pair"])
        f.write(line)
        f.write("\n")
        ind = ind + 1
    f.close()

path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
folder = path + "/Code/fixed_files"
aux_cont = 0
for filename in sorted(os.listdir(folder), reverse=True):
    if filename.endswith(".csv"):
        name = filename[:-4]
        file = folder + "/" + filename
        aux_cont += 1
        print(aux_cont ,", Converting ", name, " to .bpseq.")
        try:
            dataframe = load_dataframe(file)
            write_on_file(dataframe, name)
        except Exception:
            print("SKIPPED!!!")
            aux_cont -=1
        
    if aux_cont == 8000:
        break



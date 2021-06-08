import load_dataset as ld
from algorithms import RNAFold
#import pretrained_E2E as e2e 
import os
import csv

path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
database = ld.load_sequences(path + "/Databases/archiveII")
rnaFold = RNAFold("RNAFOLD")

list_bin_acc = ["Bin Accuracy"]
list_bin_recall = ["Bin Recall"]
list_bin_f = ["Bin F1"]
list_bin_prec = ["Bin Precision"]
list_ex_acc = ["Elem Accuracy"]
list_ex_recall = ["Elem Accuracy"]
list_ex_f = ["Elem Accuracy"]
list_ex_prec = ["Elem Accuracy"]
list_ex_amm = ["Exact match rate"]

test_set = [ 
    "A_Anab-vari-_CP000117_1-390",
    "lcaligenes-sp--1",
    "rtemia-sp--1"
]

#test_set = ["ytilus-galloprovincialis-3"]

test_list = []
for elem in database:
    if elem.name in test_set:
        test_list.append(elem)

test_list = database

aux_cont = 0

for elem in test_list:
    aux_cont = aux_cont + 1
    print("(",aux_cont,"/",len(test_list),") RNAFOLD Evaluations. Sequence: ", elem.name)
    if("N" not in elem.sequence):
        # print("Len predicted: ", len(prediction.structure["base_pair"].tolist()), ", should be: ", len(elem.structure["base_pair"].tolist()))
        # check = check and (len(prediction.structure["base_pair"].tolist()) == len(elem.structure["base_pair"].tolist()))
        predicted = rnaFold.calculate_structure(elem.sequence)
        bin_acc, bin_recall, bin_f, bin_prec, ex_acc, ex_recall, ex_f, ex_prec, ex_amm = elem.comp_evaluate(predicted)
        #elem.evaluate(prediction.structure["base_pair"].tolist())
        list_bin_acc.append(bin_acc)
        list_bin_recall.append(bin_recall)
        list_bin_f.append(bin_f)
        list_bin_prec.append(bin_prec)
        list_ex_acc.append(ex_acc)
        list_ex_recall.append(ex_recall)
        list_ex_f.append(ex_f)
        list_ex_prec.append(ex_prec)
        list_ex_amm.append(ex_amm)
        if (aux_cont == 150):
            break

with open('saved_stats/RNAFOLD_result_stats.csv', mode='w') as results_file:
    writer = csv.writer(results_file, delimiter='\t')
    writer.writerow(["Metric"] + list(range(len(list_bin_acc))))
    writer.writerow(list_bin_acc)
    writer.writerow(list_bin_recall)
    writer.writerow(list_bin_f)
    writer.writerow(list_bin_prec)
    writer.writerow(list_ex_acc)
    writer.writerow(list_ex_recall)
    writer.writerow(list_ex_f)
    writer.writerow(list_ex_prec)
    writer.writerow(list_ex_amm)

results_file.close()
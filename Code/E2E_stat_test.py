import load_dataset as ld
#from algorithms import RNAFold
import pretrained_E2E as e2e 
import os
import csv

path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
database = ld.load_sequences(path + "/Databases/archiveII")

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

#test_list = database

e2e.pretrainE2E(path+"/Code", path+"/Code/saved_results", test_list)
#results = ld.load_ct_only(path+"/Code/saved_results")

# check = True
# for prediction in results:
#     print(prediction.name)
#     for elem in test_list:
#         if prediction.name == elem.name:
#             if("N" not in elem.sequence):
#                 print("Len predicted: ", len(prediction.structure["base_pair"].tolist()), ", should be: ", len(elem.structure["base_pair"].tolist()))
#                 check = check and (len(prediction.structure["base_pair"].tolist()) == len(elem.structure["base_pair"].tolist()))
#                 # bin_acc, bin_recall, bin_f, bin_prec, ex_acc, ex_recall, ex_f, ex_prec, ex_amm = elem.comp_evaluate(prediction.structure["base_pair"].tolist())
#                 # #elem.evaluate(prediction.structure["base_pair"].tolist())
#                 # list_bin_acc.append(bin_acc)
#                 # list_bin_recall.append(bin_recall)
#                 # list_bin_f.append(bin_f)
#                 # list_bin_prec.append(bin_prec)
#                 # list_ex_acc.append(ex_acc)
#                 # list_ex_recall.append(ex_recall)
#                 # list_ex_f.append(ex_f)
#                 # list_ex_prec.append(ex_prec)
#                 # list_ex_amm.append(ex_amm)
#             break

# print("End check: ", check)


# with open('saved_stats/e2e_result_stats_under600.csv', mode='w') as results_file:
#     writer = csv.writer(results_file, delimiter='\t')
#     writer.writerow(["Metric"] + list(range(len(list_bin_acc))))
#     writer.writerow(list_bin_acc)
#     writer.writerow(list_bin_recall)
#     writer.writerow(list_bin_f)
#     writer.writerow(list_bin_prec)
#     writer.writerow(list_ex_acc)
#     writer.writerow(list_ex_recall)
#     writer.writerow(list_ex_f)
#     writer.writerow(list_ex_prec)
#     writer.writerow(list_ex_amm)

# results_file.close()

####################### TO TEST RNAFOLD ##########################
#rnaFold = RNAFold("RNAFOLD")

#test_set = [ 
#    "A_Anab-vari-_CP000117_1-390",
#    "Rhod-rubr-_CP000230",
#    "lcaligenes-sp--1",
#    "rtemia-sp--1"
#]

#for elem in database:
#    if elem.name in test_set:
#        testelem = elem
#        pseq = testelem.sequence
#        predicted = rnaFold.calculate_structure(pseq)
#        testelem.evaluate(predicted)













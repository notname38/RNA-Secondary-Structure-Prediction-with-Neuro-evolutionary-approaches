import load_dataset as ld
#from algorithms import RNAFold
import pretrained_E2E as e2e 
import os


print("Begining database load.")

path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
database = ld.load_sequences(path + "/Databases/archiveII")
print("RNA samples number: ", len(database))


print(" ")
########################### TO TEST DNN: E2E_fold #########################
print("Start main test.")
print(" ")

# This is a simple script to test the e2e fold model
# but for any other premade model should be interchangeable

test_set = [ 
    "A_Anab-vari-_CP000117_1-390",
    "Rhod-rubr-_CP000230",
    "lcaligenes-sp--1",
    "rtemia-sp--1"
]


test_list = []
for elem in database:
    if elem.name in test_set:
        test_list.append(elem)

e2e.pretrainE2E(path+"/Code", path+"/Code/saved_results", test_list)
results = ld.load_ct_only(path+"/Code/saved_results")

print("Evaluating results...")




for prediction in results:
    print(prediction.name)
    for elem in test_list:
        if prediction.name == elem.name:
            elem.evaluate(prediction.structure["base_pair"].tolist())























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













import load_dataset as ld
from algorithms import RNAFold
import os

print("Start main test.")
print("This test calculates the average MCC of applying RNAFOLD to the archive II database")
print(" ")
print("Begining database load.")

path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "/Databases/archiveII"
database = ld.load_sequences(path)
print("RNA samples number: ", len(database))

print(" ")
print("Applying RNAFOLD to the first 3 sequences and getting MCC...")
print(" ")
rnaFold = RNAFold("RNAFOLD")
#mcc_list = []
#cont = 0
#for elem in database:
#    if cont == 3 :
#        break
testName = "Rhod-rubr-_CP000230"
testelem = 0

for elem in database:
    if elem.name == testName:
        testelem = elem
        break

# TODO
# OUTDATED,

if testelem != 0:
    pseq = testelem.sequence
    print("Analizing:", testelem.name)
    print("Sequence: ", testelem.sequence)
    print("Structure: ")
    print(testelem.structure)
    print(" ")
    predicted = rnaFold.calculate_structure(pseq)
    print("Predicted structure: ")
    cont = 1
    for i in predicted:
        print(i[0],"   ",i[1])
    MCC, precision, recall, f1_score = testelem.evaluate(predicted)
    print("Mcc: ", MCC, ". Precision: ", precision, ". Recall: ", recall, ". F1_Score: ", f1_score)
    print(" ")
#    cont = cont + 1
#print(" ")



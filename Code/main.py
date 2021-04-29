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

rnaFold = RNAFold("RNAFOLD")

test_set = [ 
    "A_Anab-vari-_CP000117_1-390",
    "Rhod-rubr-_CP000230",
    "lcaligenes-sp--1",
    "rtemia-sp--1"
]

for elem in database:
    if elem.name in test_set:
        testelem = elem
        pseq = testelem.sequence
        predicted = rnaFold.calculate_structure(pseq)
        testelem.evaluate(predicted)













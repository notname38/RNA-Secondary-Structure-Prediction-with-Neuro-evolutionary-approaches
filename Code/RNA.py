import operations as op
import numpy as np

class Rna:

    def __init__(self, pName, pSequence, pStructure):
        self.name = pName
        self.sequence = pSequence
        self.structure = pStructure
    
    # Update methods
    def update_structure(self, pStructure):
        self.structure = pStructure
    
    def update_name(self, pName):
        self.name = pName
    
    def update_sequence(self, pSequence):
        self.sequence = pSequence

    def evaluate(self, pStructure, format = "list"):
        # Measures the Matthews correlation coefficient, precision, recall, f1 between the
        # ground truth and the given structure.
        # The ground truth is assumed to be the one stored in the object.

        # Important: we dont care with wich nucleotide one is paired.
        # We only care if they are paired or not
        # True: X has a pair. False: X doesnt have a pair.
        # True positive: X is paired in both predicted sequence and ground truth...

        # For now we work with a dataframe and a list of pairs. 
        # This whole code is a prototype.
        # Things might change in the future.
        truth = op.get_connected(self.structure, mode = "dataframe")
        predicted = op.get_connected(pStructure, mode = format)
        print(" ")
        print("Connections, Truth:")
        print(truth)
        print(sum(truth))
        print(" ")
        print("Connections, Predicted:")
        print(predicted)
        print(sum(predicted))
        print(" ")
        TP, TN, FP, FN = op.get_TP_TN_FP_FN(predicted, truth)
        print("TP: ", TP, ", FP: ", FP, ", TN: ", TN, ", FN: ", FN)

        MCC = ((TP*TN)-(FP*FN))/(np.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)))
        precision = TP / (TP+FP)
        recall = TP / (TP + FN)
        f1_score = 2 * ((precision * recall)/(precision + recall))
        return MCC , precision, recall, f1_score
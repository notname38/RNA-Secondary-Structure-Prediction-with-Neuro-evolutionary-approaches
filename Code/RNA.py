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

    # Soft evaluation methods:
        # Soft evaluation methods calculate the metrics 
        # where we dont care with wich nucleotide one is paired.
        # We only care if they are paired or not
        # True: X has a pair. False: X doesnt have a pair.
        # True positive: X is paired in both predicted sequence and ground truth...
    
    def soft_f1_score(self, pStructure):
        # Calculates the soft F1 score 
        TP, TN, FP, FN = op.get_TP_TN_FP_FN(pStructure, self.structure) 
        f1_score = 2 * (((TP / (TP+FP)) * (TP / (TP + FN)))/((TP / (TP+FP)) + (TP / (TP + FN))))
        return f1_score
    
    def soft_precision(self, pStructure):
        # Calculates the soft Precision score 
        TP, TN, FP, FN = op.get_TP_TN_FP_FN(pStructure, self.structure) 
        precision = TP / (TP+FP)
        return precision
    
    def soft_recall(self, pStructure):
        # Calculates the soft recall score
        TP, TN, FP, FN = op.get_TP_TN_FP_FN(pStructure, self.structure) 
        recall = TP / (TP + FN)
        return recall

    def soft_MCC(self, pStructure):
        # Measures the soft Matthews correlation coefficient.
        TP, TN, FP, FN = op.get_TP_TN_FP_FN(pStructure, self.structure) 
        MCC = ((TP*TN)-(FP*FN))/(np.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)))
        return MCC 
    
    # Normal or "hard" evaluation methods:
        # Normal evaluation methods calculate the metrics 
        # where we do care with wich nucleotide one is paired.

    def f1_score(self, pStructure):
        # Calculates the F1 score 
        TP, TN, FP, FN = op.get_TP_TN_FP_FN(pStructure, self.structure) 
        f1_score = 2 * (((TP / (TP+FP)) * (TP / (TP + FN)))/((TP / (TP+FP)) + (TP / (TP + FN))))
        return f1_score
    
    def precision(self, pStructure):
        # Calculates the Precision score 
        TP, TN, FP, FN = op.get_TP_TN_FP_FN(pStructure, self.structure) 
        precision = TP / (TP+FP)
        return precision
    
    def recall(self, pStructure):
        # Calculates the recall score
        TP, TN, FP, FN = op.get_TP_TN_FP_FN(pStructure, self.structure) 
        recall = TP / (TP + FN)
        return recall

    def MCC(self, pStructure):
        # Measures the Matthews correlation coefficient.
        TP, TN, FP, FN = op.get_TP_TN_FP_FN(pStructure, self.structure) 
        MCC = ((TP*TN)-(FP*FN))/(np.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)))
        return MCC 
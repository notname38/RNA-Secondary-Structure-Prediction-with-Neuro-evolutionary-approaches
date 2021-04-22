import numpy as np

def format_result(pair_list, nElements):
    # TODO:
    # take a good look at this method. Might find a better way.
    result_list = np.zeros((nElements,2), dtype=np.int32)
    for n in range(nElements):
        result_list[n][0] = n
    for pair in pair_list:
        result_list[pair[0]] = [pair[0], pair[1]] 
        result_list[pair[1]] = [pair[1], pair[0]]
    return list(result_list) 

def get_connected(structure, mode = "list"):
    # Returns a list where 1 is the element is connected, 0 if it isnt
    # Two modes: for a pandas dataset and a normal pair list
    sol_list = []
    if mode == "list":
        for pair in structure:
            if pair[1] == 0:
                sol_list.append(0)
            else:
                sol_list.append(1)

    if mode == "dataframe":
        pairs = structure["base_pair"].tolist()
        for pair in pairs:
            if pair == 0:
                sol_list.append(0)
            else:
                sol_list.append(1)
    
    return list(sol_list)


def get_TP_TN_FP_FN(prediction, ground_truth, mode = "soft"):
    # Returns the number of for both types "soft" and normal
    #   true positives
    TP = 0
    #   true negatives
    TN = 0
    #   false positives
    FP = 0
    #   false negatives
    FN = 0
    
    if (mode == "soft"):
        # Soft Evaluation method.
        truth = get_connected(ground_truth, mode = "dataframe")
        predicted = get_connected(prediction)
    else:
        # TODO
            # Normal evaluation method.

    nElements = len(truth)
    for n in range(nElements):
        if predicted[n] == 1 and truth[n] == 1:
            TP = TP + 1
        if predicted[n] == 1 and truth[n] == 0:
            FP = FP + 1
        if predicted[n] == 0 and truth[n] == 1:
            FN = TN + 1
        if predicted[n] == 0 and truth[n] == 0:
            TN = TN + 1
    return TP, TN, FP, FN


import math

def h(x, N):
    return math.log(x/N)*x/N

def gmd(R, S, fm, fs):
    """
    Args:
        R (list of list): the partition, output of the entity resolution that we want to evaluate 
        S (list of list): the gold standard
        fm(x,y) -> int (function): cost of merging a group of size x with another group of size y
        fs(x,y) -> int (function): cost of splitting a group into 2 groups of respective sizes x and y  
    Returns:
        double : the generalized merge distance between R and S       
    """
    # build a map M from record to cluster number
    # store sizes of each cluster in Rsizes
    Rsizes = {}
    M = {}
    for i, group in enumerate(R):
        for r, rec in enumerate(group):
            M[rec] = i
        Rsizes[i] = len(group)
    split_cost = 0
    merge_cost = 0
    for i, group in enumerate(S):
        # determine which clusters in R contain the records in group i
        pMap = {}
        for r, rec in enumerate(group):
            # if we haven't seen the R cluster corresponding to this element we add it to the map
            try:
                M[rec]
            except KeyError as err:
                raise KeyError(
                    'The element of R : {} isn\'t present in S. Check that you did reconcile R and S'.format(err))
            if M[rec] not in pMap:
                pMap[M[rec]] = 0
            # increment the count for this partition
            pMap[M[rec]] += 1

        # compute cost to generate group i of S
        totalRecs = 0
        s_cost = 0
        m_cost = 0
        for i, count in pMap.items():
            if Rsizes[i] > count:
                # add the cost to split R[i]
                s_cost += fs(count, Rsizes[i] - count)
            Rsizes[i] -= count
            if totalRecs != 0:
                # cost to merge into S[i]
                m_cost += fm(count, totalRecs)
            totalRecs += count
        split_cost += s_cost
        merge_cost += m_cost
    return split_cost + merge_cost


def check_r_s_same_size(R, S):
    """
    Raises an exception if R and S have different number of distinct elements

    Args:
        R (list of list): the gold standard
        S (list of list): the partition, output of the entity resolution that we want to evaluate
    """
    R_set = set()
    S_set = set()
    for i, val in enumerate(R):
        for j, rec in enumerate(val):
            R_set.add(rec)
    for i, val in enumerate(S):
        for j, rec in enumerate(val):
            S_set.add(rec)
    if len(R_set) != len(S_set):
        raise ValueError("R and S have different numbers of distincts records : R has", len(
            R_set), "distinct records while S has", len(S_set), "distinct records")


def to_set(list_of_list):
    """
     Transforms a list of list into a set
     [[0,1],[2]] -> {0,1,2}
    """
    _set = set()
    for list_ in list_of_list:
        for element in list_:
            _set.add(element)
    return _set


def splitted(_set):
    """ Transforms a set {0,1,2} into a list of singletons [[0],[1],[2]]"""
    splitted = []
    for el in _set:
        splitted.append([el])
    return splitted


def evaluate(R, S, metric):
    """
    Evaluate R against S on metric 
    Args:
        R (list of list): the entity resolution we want to evaluate
        S (list of list): the gold standard
        metric (str) : the metric we want to use to evaluate : bmd, precision, recall, variation_of_information, f1
    Returns:
        double : the value of the metric
    """
    check_r_s_same_size(R,S)
    S_set = to_set(S)
    N = len(S_set)

    metrics_cost = {
        'bmd': {
            'merge_cost': lambda x, y: 1,
            'split_cost': lambda x, y: 1},

        'precision': {
            'merge_cost': lambda x, y: 0,
            'split_cost': lambda x, y: x*y},

        'recall': {
            'merge_cost': lambda x, y: x*y,
            'split_cost': lambda x, y: 0},

        'variation_of_information': {
            'merge_cost': lambda x, y: h(x+y, N) - h(x, N) - h(y, N),
            'split_cost': lambda x, y: h(x+y, N) - h(x, N) - h(y, N)},
        'f1':{}
    }
    if metric not in metrics_cost:
        raise ValueError('{} is not part of the possible metrics : {}'.format(
            metric, metrics_cost.keys()))

    direct_metrics = {'bmd', 'variation_of_information'}

    if metric in direct_metrics:
        return gmd(R, S, metrics_cost[metric]['merge_cost'], metrics_cost[metric]['split_cost'])

    if metric in ('precision','f1'):
        S_splitted = splitted(S_set)
        distance_to_splitted = gmd(
            R, S_splitted, metrics_cost['precision']['merge_cost'], metrics_cost['precision']['split_cost'])
        if distance_to_splitted == 0:
            return 0
        precision = 1 - gmd(R, S, metrics_cost['precision']['merge_cost'], metrics_cost['precision']['split_cost']) / distance_to_splitted
        value = precision        

    if metric in ('recall','f1'):
        S_splitted = splitted(S_set)
        distance_from_splitted = gmd(
            S_splitted, S, metrics_cost['recall']['merge_cost'], metrics_cost['recall']['split_cost'])
        if distance_from_splitted == 0:
            return 0
        recall =  1 - gmd(R, S, metrics_cost['recall']['merge_cost'], metrics_cost['recall']['split_cost']) / distance_from_splitted
        value = recall        

    if metric == 'f1':
        return 2 * precision * recall / (precision + recall)
    else:
        return value


def worst_entities(R,S,kind):
    """
    Args:
        R (list of list): the entity resolution we want to evaluate
        S (list of list): the gold standard
        kind (str) : the metric we want to use to evaluate : bmd, precision, recall, variation_of_information, f1
    Returns:
        list : list of entities with the linked entities
    """
    dic_s = {}

    for i,entity in enumerate(S):
        for r, rec in enumerate(entity):
            dic_s[rec] = i


    if kind == "glued":
        dic_r_s = {}
        for i,entity in enumerate(R):
            _set = set()
            for r,rec in enumerate(entity):
                _set.add(dic_s[r])
            dic_r_s[i] = _set
        
        dic_r_s_count = {key:len(_set) for key,_set in dic_r_s.items()}
        sorted_list = sorted(dic_r_s_count,key = dic_r_s_count.get, reverse = True)
        
        return sorted_list[:100], dic_r_s
            





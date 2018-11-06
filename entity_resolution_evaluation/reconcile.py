from entity_resolution_evaluation.evaluation import to_set


def reconcile(R,S,method):
    """
    If R_set, the set of elements of R and S_set are disjoints, we can't evaluate R with S.
    First we need to reconcile R and S so that R_set and S_set are equal
    Args:
        R (list of list): the partition, output of the entity resolution that we want to evaluate
        S (list of list): the gold standard
        method (str): the reconciliation method among 'R0S' and 'R1S1'
    Returns:
        (list of list): R after reconciliation
        (list of list): S after reconciliation
    """
    S_set = to_set(S)

    if method == "R0S":
        # delete all elements of R not in S
        R0 = []
        for i, entity in enumerate(R):
            R0_entity = []
            for r, rec in enumerate(entity):
                if rec in S_set:
                    R0_entity.append(rec)
            R0.append(R0_entity)
        return R0,S

    if method == "R1S1":
        # first let's build R1
        R1 = []
        for i, entity in enumerate(R):
            entity_partially_in_S = 0
            for r,rec in enumerate(entity):
                if rec in S_set:
                    entity_partially_in_S = 1
                    break
            # we only add to R1, entities that have at least 1 element in S
            if entity_partially_in_S == 1:
                R1.append(entity)
        # now S1
        S1 = S[:]
        for i, entity in enumerate(R1):
            new_entity = []
            for r, rec in enumerate(entity):
                if rec not in S_set:
                    new_entity.append(rec)
            S1.append(new_entity)

        return R1,S1








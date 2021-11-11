from itertools import combinations

def power_set(S):
    output_power_set = set()
    for ii in range(len(S)+1):
        for subset in combinations(S, ii):
            print(frozenset(subset))
            output_power_set.add(frozenset(subset))
    return frozenset(output_power_set)




    
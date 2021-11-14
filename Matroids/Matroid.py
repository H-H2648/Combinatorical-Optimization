from helper import power_set
from itertools import combinations

class Matroid:
    #Matroids are defined by the ground set and the independent set
    #only the ground_set is required but one of circuits, bases, independent_set is required to run greedy algorithm
    #ground_set, independent_set, circuits, bases are assumed to be sets of sets
    #all sets are assumed to be frozen
    def __init__(self, ground_set = None, independent_set = None, circuits = None, bases = None):
        self.ground_set = ground_set
        self.independent_set = independent_set
        self.circuits = circuits
        self.bases = bases
        self.power_ground_set = None

    def generate_power_ground_set(self):
        self.power_ground_set = power_set(self.ground_set)

    #NOTE: IF YOU SET THE INDEPENDENT SET, CIRCUITS, BASES TO BE INCONSISTENT BETWEEN EACH OTHER, THE PROGRAM WILL FAIL TO OUTPUT THE CORRECT ANSWER

    def set_independent_set(self, independent_set):
        self.independent_set = independent_set

    #usually this function will be defined manually
    def is_independent(self, some_set):
        return (some_set in self.independent_set)

    def form_independent_set(self):
        if self.power_ground_set is None:
            self.generate_power_ground_set()
        self.independent_set = set()
        for element in self.power_ground_set:
            if self.is_independent(element):
                self.independent_set.add(element)
        self.independent_set = frozenset(self.independent_set)


    def compute_rank(self, some_set):
        max_size = -1
        for subset in power_set(some_set):
            if self.is_independent(subset):
                size = len(subset)
                if size > max_size:
                    max_size = size
        return max_size

    ### determines if B is a basis with respect to the superset, A
    ### assumes B is a subset of As
    def is_basis(self, B, A):
        if not(self.is_independent(B)):
            return False
        for elem in A:
            if not(elem in B):
                ###look at set(B) temporarily so that B is mutable
                temp_B = set(B)
                temp_B.add(elem)
                if self.is_independent(temp_B):
                    return False
        return True

    ### computes rho: the minimum size of a basis in a set
    def compute_rho(self, some_set):
        rho = len(some_set)
        for subset in power_set(some_set):
            if self.is_basis(subset, some_set):
                print(subset)
                size = len(subset)
                if size < rho:
                    rho = size
        return rho

    def check_independent_sets(self):
        #M1
        if not(frozenset(set()) in self.independent_set):
            return False
        #M2
        for ind in self.independent_set:
            for ind_subset in power_set(ind):
                if not(ind_subset in self.independent_set):
                    return False
        #M3'
        for X, Y in combinations(self.independent_set, 2):
            if len(X) != len(Y):
                if len(Y) > len(X):
                    X, Y = Y, X
                bad_pair = True
                for new_elem in X.difference(Y):
                    if self.is_independent(Y.union(frozenset({new_elem}))):
                        bad_pair = False
                        break
                if bad_pair:
                    print(f"M3 FAILED! {X}, {Y}")
                    return False
        return True



    def set_circuits(self, circuits):
        self.circuits = circuits

    def form_independent_set_from_circuits(self):
        if self.circuits is None:
            print("ERROR must have circuits")
        if self.power_ground_set is None:
            self.generate_power_ground_set()
        self.independent_set = set()
        for element in self.power_ground_set:
            independence=True
            for circuit in self.circuits:
                if circuit.issubset(element):
                    independence=False
                    break
            if independence:
                self.independent_set.add(element)
        self.independent_set = frozenset(self.independent_set)


    def check_circuits(self):
        #C1
        if (frozenset(set()) in self.circuits):
            return False
        #C2
        for C1, C2 in combinations(self.circuits, 2):
            if C1.issubset(C2) or C2.issubset(C1):
                #since we have combination, if they are already distinct
                return False
        #C3
        for C1, C2 in combinations(self.circuits, 2):
            for element in C1.intersection(C2):
                test_set = (C1.union(C2)).difference(frozenset({element}))
                bad_pair = True
                for circuit in self.circuits:
                    if circuit.issubset(test_set):
                        bad_pair = False
                        break
                if bad_pair:
                    return False
        return True

    def set_bases(self, bases):
        self.bases = bases
    
    
    def form_independent_set_from_bases(self):
        if self.bases is None:
            print("ERROR must have bases")
        if self.power_ground_set is None:
            self.generate_power_ground_set()
        self.independent_set = set()
        for element in self.power_ground_set:
            for basis in self.bases:
                if element.issubset(basis):
                    self.independent_set.add(element)
                    break
        self.independent_set = frozenset(self.independent_set)


    def check_bases(self):
        def check_bases_helper(B1, B2, x, bases):
            for y in B2.difference(B1):
                if (B1.difference(frozenset({x})).union(frozenset({y})) in bases):
                    return True
            return False
        if self.bases == frozenset(set()):
            return False
        for B1, B2 in combinations(self.bases, 2):
            for x in B1.difference(B2):
                if check_bases_helper(B1, B2, x, self.bases):
                    continue
                return False
        return True



    def set_costs(self, costs_dict):
        costs = []
        for key in costs_dict:
            costs.append((key, costs_dict[key]))
        costs = sorted(costs, key = lambda x: x[1], reverse=True)
        return costs

    def max_cost_greedy(self, costs_dict):
        costs = self.set_costs(costs_dict)
        object_so_far = set()
        for elem, cost in costs:
            if cost <= 0:
                break
            else:
                object_so_far.add(elem)
                if not(self.is_independent(object_so_far)):
                    object_so_far.remove(elem)
        return object_so_far

    def min_cost_greedy(self, costs_dict):
        for elem in costs_dict:
            costs_dict[elem] = -costs_dict[elem]
        return self.max_cost_greedy(costs_dict)
            

                    

                
        
         

    

            
                        

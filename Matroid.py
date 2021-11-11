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

    def set_circuits(self, circuits):
        self.circuits = circuits

    def set_bases(self, bases):
        self.bases = bases

    def form_independent_set_from_circuits(self):
        if self.circuits is None:
            print("ERROR must have circuits")
        if self.power_ground_set is None:
            self.generate_power_ground_set()
        else:
            self.independent_set = set()
            for element in self.power_ground_set:
                for circuit in circuits:
                    if circuit.issubset(element):
                        break
                self.independent_set.add(element)
            self.independent_set = frozenset(self.independent_set)

    def form_independent_set_from_bases(self):
        if self.bases is None:
            print("ERROR must have bases")
        if self.power_ground_set is None:
            self.generate_power_ground_set()
        else:
            self.independent_set = set()
            for element in self.power_ground_set:
                for basis in self.bases:
                    if element.issubset(basis):
                        self.independent_set.add(element)
                        break
            self.independent_set = frozenset(self.independent_set)

    def check_independent_set(self):
        #M1
        if not(frozenset(set()) in self.independent_set):
            return False
        #M2
        for ind in self.independent_set:
            for ind_subset in power_set(ind):
                if not(ind_subset in self.independent_set):
                    return False
        #M3'
        for X, Y in combination(self.independent_set, 2):
            if len(X) != len(Y):
                if len(Y) > len(X):
                    X, Y = Y, X
                for new_elem in X.difference(Y):
                    if Y.union(frozenset({new_elem})) in self.independent_set:
                        continue
                return False
        return True

    def check_circuits(self):
        #C1
        if (frozenset(set()) in self.circuits):
            return False
        #C2
        for C1, C2 in combination(self.circuits, 2):
            if C1.issubset(C2) or C2.issubset(C1):
                #since we have combination, if they are already distinct
                return False
        #C3
        for C1, C2 in combination(self.circuits, 2):
            for element in C1.union(C2):
                test_set = (C1.union(C2)).difference(frozenset({element}))
                for circuit in self.circuits:
                    if circuit.issubset(test_set):
                        continue
            return False
        return True

    

    def check_bases(self):
        def check_bases_helper(B1, B2, x, bases):
            for y in B2.difference(B1):
                if (B1.difference(frozenset({x})).union(frozenset({y})) in bases):
                    return True
            return False
        if self.bases == frozenset(set()):
            return False
        for B1, B2 in combination(self.bases, 2):
            for x in B1.difference(B2):
                if check_bases_helper(B1, B2, x, self.bases):
                    continue
                return False
        return True

    def is_independent(self, some_set):
        return (some_set in self.independent_set)

                    

                
        
         

    

            
                        

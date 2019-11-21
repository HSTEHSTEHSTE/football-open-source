import numpy as np
import random

position_list = ['GK', 'SW', 'DL', 'DR', 'DC', 'DML', 'DMR', 'DMC', 'ML', 'MR', 'MC', 'AML', 'AMR', 'AMC', 'FL', 'FR', 'FC']
number_of_positions = len(position_list)
first_names = ['Jack', 'John', 'Henry']
last_names = ['Doe', 'Gee', 'Ba']

class Player: 
    def __init__(self, position_familiarity = ([0] * number_of_positions), overall_score = 0, first_name = None, last_name = None): 
        self.generate_name(first_name, last_name)
        self.position_familiarity = position_familiarity
        self.overall_score = overall_score
        
    def set_position(self, position, strength):
        if isinstance(position, int): 
            self.position_familiarity[position] = strength
        else: 
            self.position_familiarity[position_list.index(position)] = strength
    
    def set_overall_score(self, score):
        self.overall_score = score
        
    def get_overall_score(self):
        return self.overall_score
        
    def get_position_familiarity(self, position):
        if isinstance(position, int):
            return self.position_familiarity[position]
        else:
            return self.position_familiarity[position_list.index(position)]
            
    def get_name(self):
        return self.first_name + ' ' + self.last_name
        
    def generate_name(self, first_name = None, last_name = None):
        if first_name is None:
            self.first_name = random.choice(first_names)
        else: 
            self.first_name = first_name
        if last_name is None:
            self.last_name = random.choice(last_names)
        else:
            self.last_name = last_name
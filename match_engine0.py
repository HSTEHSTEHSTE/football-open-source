import numpy as np
import player
import match_data
import pandas
import random
import math

formation_442 = ['GK', 'DL', 'DC', 'DC', 'DR', 'ML', 'MC', 'MC', 'MR', 'FC', 'FC']
areas = ['shot_def', 'def', 'mid', 'atk', 'shot_atk']
position_weight = pandas.read_excel('metadata/match_engine.xlsx', 'me0_posweight', index_col = 0)
class Match_Engine():
    def __init__(self, squad_size): 
        self.ready = False
        if squad_size >= 11: 
            self.squad_size = squad_size
        else: 
            self.squad_size = 17
        self.def_multiplier = 3
        self.shot_def_multiplier = 7
    
    def init_lineup(self, home_player_list, away_player_list, home_formation = formation_442, away_formation = formation_442): #numbers
        self.home_player_list = home_player_list
        self.away_player_list = away_player_list
        self.home_formation = home_formation
        self.away_formation = away_formation
        self.ready = self.validate_lineup(home_formation) & self.validate_lineup(away_formation)
        if self.ready: 
            self.calculate_strengths()
        
    def validate_lineup(self, formation): 
        gk_count = formation.count('GK')
        gk_count += formation.count(0)
        if gk_count == 1:
            return True
        else: 
            return False
            
    def play_match(self, extra_time = False):
        if not self.ready:
            return False
        self.time = 0
        self.added_time = 0
        current_match_data = match_data.Match_data()
        current_match_data.start()
        message = ''
        self.in_added_time = False
        while not current_match_data.get_finished():
            if not self.in_added_time:
                self.time += 1
                message = str(self.time) + ' minute' + '\n'  
                if self.time == 45 or self.time == 90:
                    added_time = self.calculate_added_time()
                    self.in_added_time = True
            else:
                self.added_time += 1
                message = str(self.time) + ' minute ' + str(self.added_time) + ' minute in added time\n' 
                if self.added_time >= added_time:
                    self.in_added_time = False
                    self.added_time = 0
                    if not extra_time and self.time == 45:
                        current_match_data.update_second_half()
                    if not extra_time and self.time == 90:
                        current_match_data.finish()
            possession = self.calculate_possession()
            atk = 0
            dfs = 0
            possession_team_name = ''              
            if possession == 0:
                current_match_data.add_home_possession()
                atk = self.home_strength_list[3]
                dfs = self.away_strength_list[1]
                shot_atk = self.home_strength_list[4]
                shot_def = self.away_strength_list[0]
                message += 'Home team has possession.' + '\n'
                possession_team_name = 'Home team'
            if possession == 1:
                current_match_data.add_away_possession()
                atk = self.away_strength_list[3]
                dfs = self.home_strength_list[1]
                shot_atk = self.home_strength_list[0]
                shot_def = self.away_strength_list[4]
                message += 'Away team has possession.' + '\n'
                possession_team_name = 'Away team'
            attack = self.calculate_attack(atk, dfs)
            if attack == 0:
                message += 'The attack was broken down.'
            if attack == 1:
                current_match_data.add_shot(possession)
                message += possession_team_name + ' has a crack!' + '\n'
                goal = self.calculate_shot(shot_atk, shot_def)   
                if goal == 0:
                    message += possession_team_name + ' missed it!'
                if goal == 1:
                    message += possession_team_name + ' scored!' + '\n'
                    current_match_data = self.add_goal(possession, current_match_data)
                    home_score, away_score = current_match_data.get_score()
                    message += 'Home team ' + str(home_score) + ':' + str(away_score) + ' Away team'
            print(message)
        self.print_match_stats(current_match_data)
        return current_match_data            
    
    def calculate_strengths(self):
        self.home_strength_list = []
        self.away_strength_list = []
        for area in areas:
            area_weight = position_weight[area]
            area_strengh = 0
            for player in self.home_player_list[:11]: 
                position = self.home_formation[self.home_player_list.index(player)]
                player_position_familiarity = player.get_position_familiarity(position)
                area_strengh += player.get_overall_score() * player_position_familiarity * area_weight.loc[position]
            self.home_strength_list.append(area_strengh)
            area_strengh = 0
            for player in self.away_player_list[:11]: 
                position = self.away_formation[self.away_player_list.index(player)]
                player_position_familiarity = player.get_position_familiarity(position)
                area_strengh += player.get_overall_score() * player_position_familiarity * area_weight.loc[position]
            self.away_strength_list.append(area_strengh)
    
    def calculate_possession(self):
        home_mid = self.home_strength_list[2]
        away_mid = self.away_strength_list[2]
        random_mid = random.random() * (home_mid + away_mid)
        if random_mid <= home_mid:
            return 0
        else:
            return 1
            
    def calculate_attack(self, atk, dfs):
        random_atk = random.random() * (atk + dfs * self.def_multiplier)
        if random_atk <= atk: 
            return 1
        else: 
            return 0
            
    def calculate_shot(self, shot_atk, shot_def):
        random_shot = random.random() * (shot_atk + shot_def * self.shot_def_multiplier)
        if random_shot <= shot_atk:
            return 1
        else:
            return 0
            
    def add_goal(self, possession_team, match_data):
        if possession_team == 0:
            match_data.add_home_goal()
        if possession_team == 1:
            match_data.add_away_goal()
        return match_data
        
    def calculate_added_time(self):
        added_time = random.randint(1, 5)
        return added_time
        
    def print_match_stats(self, match_data):
        message = 'Match end' + '\n'
        home_score, away_score = match_data.get_score()
        message += 'Final score: ' + str(home_score) + ':' + str(away_score) +'\n'
        home_shots, away_shots = match_data.get_shots()
        message += 'Shots: ' + str(home_shots) + ':' + str(away_shots) + '\n'
        home_possession, away_possession = match_data.get_possession()
        message += 'Possession: ' + str(round(home_possession, 1)) + ':' + str(round(away_possession,1))
        print(message)

test = Match_Engine(0)
test_home_player_list = []
test_away_player_list = []
for i in range(17):
    test_player = player.Player(overall_score = 10, position_familiarity = [1] * 17)
    print(test_player.get_name())
    test_home_player_list.append(test_player)
    test_away_player_list.append(test_player)
test.init_lineup(test_home_player_list, test_away_player_list)
test.play_match()

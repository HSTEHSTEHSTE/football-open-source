import player

class Team():
    def __init__(self, name, player_list = []):
        self.name = name
        self.player_list = player_list
    
    def update_players(self, player_list = []):
        self.player_list = player_list
        
    def add_player(self, player):
        self.player_list.append(player)
    
    def pick_team(self, )
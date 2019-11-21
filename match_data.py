import player

class Match_data():
    def __init__(self, time = 0, score_home = 0, score_away = 0, started = False, finished = False, half = 0, shots_home = 0, shots_away = 0, possession_home = 0, possession_away = 0):
        self.time = time
        self.score_home = score_home
        self.score_away = score_away
        self.started = started
        self.finished = finished
        self.half = 0
        self.shots_home = shots_home
        self.shots_away = shots_away
        self.possession_home = possession_home
        self.possession_away = possession_away
    
    def get_time(self):
        return self.time
    
    def update_time(self, new_time):
        self.time = new_time
    
    def add_time(self, added_time):
        self.time += added_time
        
    def get_started(self):
        return self.started
        
    def start(self):
        self.start = True
        
    def get_finished(self):
        return self.finished
        
    def finish(self):
        self.finished = True
        
    def get_score(self):
        return self.score_home, self.score_away
        
    def update_score(self, home_score = None, away_score = None):
        if home_score is not None: 
            self.score_home = home_score
        if away_score is not None:
            self.score_away = away_score
        
    def add_home_goal(self):
        self.score_home += 1
        
    def add_away_goal(self):
        self.score_away += 1
        
    def update_shots(self, home_shots = None, away_shots = None):
        if home_shots is not None:
            self.shots_home = home_shots
        if away_shots is not None:
            self.shots_away = away_shots
        
    def add_home_shot(self):
        self.shots_home += 1
        
    def add_away_shot(self):
        self.shots_away += 1
        
    def get_shots(self):
        return self.shots_home, self.shots_away
        
    def add_shot(self, team):
        if team == 0:
            self.shots_home += 1
        if team == 1:
            self.shots_away += 1
        
    def update_possession(self, home_possession = None, away_possession = None):
        if home_possession is not None:
            self.possession_home = home_possession
        if away_possession is not None:
            self.possession_away = away_possession
    
    def add_home_possession(self, added_home_possession = 1):
        self.possession_home += added_home_possession
        
    def add_away_possession(self, added_away_possession = 1):
        self.possession_away += added_away_possession
        
    def get_possession(self):
        if self.possession_home == 0 and self.possession_away == 0:
            return 50.0, 50.0
        if self.possession_home == 0:
            return 0.0, 100.0
        if self.possession_away == 0:
            return 100.0, 0.0
        possession_total = self.possession_home + self.possession_away
        possession_home = self.possession_home/possession_total * 100
        possession_away = self.possession_away/possession_total * 100
        return possession_home, possession_away
        
    def get_half(self):
        return self.half;
    
    def update_second_half(self):
        self.half = 1
    
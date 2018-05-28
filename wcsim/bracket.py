from match import play_match
from collections import defaultdict
import itertools

class Bracket:
    def __init__(self, teams):
        self.root = None
        self.teams = teams
        

class Team:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating
        self.points = 0
        
    def add_win_points(self):
        self.points += 3
        
    def add_draw_points(self):
        self.points += 1
        

class Group:
    def __init__(self, name, teams):
        self.name = name
        self.teams = teams
        self.results = defaultdict(dict)
        
    def _add_result(self, winner, loser, is_draw=False):
        if is_draw:
            self.results[winner.name][loser.name] = 'D'
            self.results[loser.name][winner.name] = 'D'
            winner.add_draw_points()
            loser.add_draw_points()
        else:
            self.results[winner.name][loser.name] = 'W'
            self.results[loser.name][winner.name] = 'L'
            winner.add_win_points()
        
    def play_fixtures(self):
        for a, b in itertools.combinations(self.teams, 2):
            outcome = play_match(a, b, draw_possible=True)
            if outcome == 'Draw':
                self._add_result(a, b, is_draw=True)
            else:
                self._add_result(outcome[0], outcome[1])
                
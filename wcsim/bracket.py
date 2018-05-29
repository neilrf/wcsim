from match import play_match
from collections import defaultdict
import itertools


class KnockOut:
    def __init__(self, first_stage):
        self.champion = None
        self.rounds = [first_stage]
        
    def _play_knockout(self, stage):
        next_stage = []
        for (a, b) in stage:
            winner, loser = play_match(a, b, draw_possible=False)
            team_through = winner
            next_stage.append(team_through)
        if len(next_stage) > 1:
            self.rounds.append(zip(next_stage, next_stage[1:][::2]))
            self._play_knockout(self.rounds[-1])
        else:
            self.champion = next_stage[0]
    
    def play_knockout(self):
        self._play_knockout(self.rounds[-1])

        
class Node:
    def __init__(self, team, lchild=None, rchild=None):
        self.team = team
        self.parent = None
        self.lchild = lchild
        self.rchild = rchild


class Team:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating
        self.points = 0
        
    def add_win_points(self):
        self.points += 3
        
    def add_draw_points(self):
        self.points += 1
        
    def reset_points(self):
        self.points = 0

        
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
                
        self.teams = sorted(self.teams, key=lambda x: x.points, reverse=True)
        
    def print_table(self):
        print '==============='
        print 'Group {}'.format(self.name)
        print '==============='
        for team in self.teams:
            print '{:<12}  {}'.format(team.name, team.points)
        print '==============='


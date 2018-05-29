from match import play_match
from collections import defaultdict
import itertools


class KnockOut:
    def __init__(self, teams):
        self.champion = None
        self.root = None
        self.teams = teams
        self.tree = [[Node(team) for team in self.teams]]
        
    def _play_knockout(self, nodes):
        if len(nodes) == 1:
            self.champion = nodes[0].team
            self.root = nodes[0]
        else:
            next_round = []
            for a, b in zip(nodes, nodes[1:])[::2]:
                winner, loser = play_match(a.team, b.team, draw_possible=False)
                team_through = Node(winner, a, b)
                a.parent = team_through
                b.parent = team_through
                next_round.append(team_through)
            self.rounds.append(next_round)
            self._play_knockout(self.tree[-1])
    
    def play_knockout(self):
        self._play_knockout(self.tree[-1])

        
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

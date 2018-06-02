from match import play_match
from collections import defaultdict
from random import shuffle
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
            winner.add_win()
            next_stage.append(team_through)
        if len(next_stage) > 1:
            self.rounds.append(zip(next_stage, next_stage[1:])[::2])
            self._play_knockout(self.rounds[-1])
        else:
            self.champion = next_stage[0]
    
    def play_knockout(self):
        self._play_knockout(self.rounds[-1])
    
    @staticmethod
    def _determine_round(stage):
        num_matches = len(stage)
        if num_matches == 1:
            return 'Final'
        elif num_matches == 2:
            return 'Semi-finals'
        elif num_matches == 4:
            return 'Quarter-finals'
        else:
            return 'Round of {}'.format(2*num_matches)
    
    def _print_stage(self, stage):
        stage_name = self._determine_round(stage)
        print stage_name
        print '==========================='
        for match in stage:
            print '{:<12} v {:>12}'.format(match[0].name, match[1].name)
        print '==========================='
            
    def print_rounds(self):
        for stage in self.rounds:
            self._print_stage(stage)
        print "Winner: {}".format(self.champion.name)
        print '==========================='
    
    @staticmethod
    def _get_teams_in_round(stage):
        return [team.name for match in stage for team in match]
        
    def teams_per_round(self):
        round_teams = {}
        for stage in self.rounds:
            stage_name = self._determine_round(stage)
            round_teams[stage_name] = self._get_teams_in_round(stage)
        round_teams['Winner'] = [self.champion.name]
        return round_teams
            

class Team:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating
        self.points = 0
        self.wins = 0
        
    def add_win_points(self):
        self.points += 3
        
    def add_draw_points(self):
        self.points += 1
        
    def reset_points(self):
        self.points = 0
        
    def add_win(self):
        self.wins += 1

        
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
            winner.add_win()
        
    def play_fixtures(self):
        for a, b in itertools.combinations(self.teams, 2):
            outcome = play_match(a, b, draw_possible=True)
            if outcome == 'Draw':
                self._add_result(a, b, is_draw=True)
            else:
                self._add_result(outcome[0], outcome[1])
        
        shuffle(self.teams)
        self.teams = sorted(self.teams, key=lambda x: x.points, reverse=True)
        
    def print_table(self):
        print '==============='
        print 'Group {}'.format(self.name)
        print '==============='
        for team in self.teams:
            print '{:<12}  {}'.format(team.name, team.points)
        print '==============='


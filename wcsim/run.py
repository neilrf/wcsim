from bracket import Team, KnockOut, Group
import config
import collections
import pandas as pd

def run_tournament(config, print_results=True):
    """
    Run entire tournament (based on config for now)
    """
    GROUPS_CONFIG = config.GROUPS
    RATINGS = config.RATINGS
    KNOCKOUT_CONFIG = config.RO16
    
    groups = sorted([
        Group(name,
              [Team(country, RATINGS[country]) for country in teams])
        for name, teams in GROUPS_CONFIG.iteritems()
    ], key=lambda x: x.name)
    
    for g in groups:
        g.play_fixtures()
        if print_results:
            g.print_table()
            
    qualifiers = {}
    for g in groups:
        qualifiers['{}1'.format(g.name)] = g.teams[0]
        qualifiers['{}2'.format(g.name)] = g.teams[1]
    
    first_round = [(qualifiers[x], qualifiers[y]) for x,y in KNOCKOUT_CONFIG]
    knockout = KnockOut(first_round)
    knockout.play_knockout()
    return knockout
    

def mc_wc(config, num_runs=10):
    teams = [team for group in config.GROUPS.values() for team in group]
    
    def empty_counter(items_list):
        return collections.Counter({
            item: 0 for item in items_list
        })
        
    results = {
        'Round of 16': empty_counter(teams),
        'Quarter-finals': empty_counter(teams),
        'Semi-finals': empty_counter(teams),
        'Final': empty_counter(teams),
        'Winner': empty_counter(teams)
    }
    
    for i in range(num_runs):
        knockout = run_tournament(config,False)
        round_teams = knockout.teams_per_round()
    
        for round, nations in round_teams.iteritems():
            results[round].update(nations)
            
    results_df = pd.DataFrame(results)
    results_df = 100*results_df/num_runs
    columns = ['Round of 16',
               'Quarter-finals',
               'Semi-finals',
               'Final',
               'Winner']
    results_df = results_df[columns]
            
    return results_df.sort_values('Winner', ascending=False)
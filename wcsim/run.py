from bracket import Team, Node, KnockOut, Group
import config

def run_tournament(config, print_results=True):
    """
    Run entire tournament (based on config for now)
    """
    GROUPS_CONFIG = config.GROUPS
    RATINGS = config.RATINGS
    KNOCKOUT_CONFIG = config.RO16
    
    groups = [
        Group(name,
              [Team(country, RATINGS[country]) for country in teams])
        for name, teams in GROUPS_CONFIG.iteritems()
    ]
    
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
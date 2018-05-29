from __future__ import division
import numpy as np
from scipy.stats import norm
import math


def play_match(a, b, draw_possible=True):
    """
    Generate result of match between team a and b.
    """
    draw_prob = 0
    rating_diff = b.rating - a.rating
    a_winprob = 1 / (1 + 10**(rating_diff / 400))
    b_winprob = 1 - a_winprob
    if draw_possible:
        draw_prob = norm.pdf(rating_diff/200, 0, math.e)
        b_winprob = b_winprob - 0.5 * draw_prob
        a_winprob = a_winprob - 0.5 * draw_prob
        
    result = np.random.choice(['1','2','X'], p=[a_winprob,
                                                b_winprob,
                                                draw_prob])
    if result == 'X':
        return 'Draw'
    elif result == '1':
        winner = a
        loser = b
    elif result == '2':
        winner = b
        loser = a
        
    return winner, loser

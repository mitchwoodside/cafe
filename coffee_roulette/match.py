import math
import random

def split_list(a):
    half = len(a)//2
    return a[:half], a[half:]

def match_players(names, banned_matches):
    while True:
        random.shuffle(names)
        a,b = split_list(names)
        matches = {frozenset(i) for i in zip(a, b)}
        if not matches & banned_matches:
            break

    return matches

def remove_exhausted_players(names, banned_matches):
    matches_exhausted = []
    for name in names:
        names_banned_matches = [i for i in banned_matches if name in i]
        banned_match_count = len(names_banned_matches)
        if banned_match_count >= len(names) - 1:
            matches_exhausted.append(name)

    for name in matches_exhausted:
        names.remove(name)

    return matches_exhausted

def all_matches_banned(names, banned_matches):
    return len(banned_matches) >= math.comb(len(names),2)

def ban_self_matches(names, banned_matches):
    for name in names:
        banned_matches.add(frozenset((name,name)))


def get_matches(names, banned_matches):
    if not len(names) == len(set(names)):
        raise Exception("not all players are unique")

    exhausted_players = remove_exhausted_players(names, banned_matches)
    ban_self_matches(names, banned_matches)

    if all_matches_banned(names, banned_matches):
        raise Exception("All matches are banned")

    if not len(names) == 2 * (len(names)//2):
        unmatched_player = random.choice(names)
        names.remove(unmatched_player)

    matches = match_players(names, banned_matches)

    return matches, unmatched_player, exhausted_players

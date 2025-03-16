import random
from itertools import combinations

import click


def is_odd(n):
    return n % 2


def remove_exhausted_players(players, available_matches):
    exhausted_players = []

    for name in players:
        if not any(name in s for s in available_matches):
            exhausted_players.append(name)
            players.remove(name)

    return exhausted_players


def match_players(names_orig, available_matches_orig):
    def reshuffle():
        random.shuffle(names_orig)
        random.shuffle(list(available_matches_orig))
        return list(names_orig), list(available_matches_orig), []

    def valid_match(potential_match, potential_name):
        other = next(n for n in potential_match if not n == potential_name)
        return name in potential_match and other in names

    names, available_matches, matches = reshuffle()
    attempts = 0

    while names:
        name = names.pop()
        try:
            match = next(m for m in available_matches if valid_match(m, name))
            matches.append(match)

            for player in (p for p in match if not p == name):
                names.remove(player)

        except StopIteration:
            attempts += 1
            click.echo('-----+++++##### RESHUFFLING #####+++++-----')
            if attempts > 100:
                raise Exception("Cannot match all players")
            names, available_matches, matches = reshuffle()

    return matches


def get_matches(names, banned_matches):
    unmatched_player = None
    exhausted_players = []

    if not len(names) == len(set(names)):
        raise Exception("not all players are unique")

    available_matches = {frozenset(a) for a in combinations(names, 2)} - banned_matches

    for name in names:
        if not any(name in s for s in available_matches):
            exhausted_players.append(name)
            names.remove(name)

    if not available_matches:
        raise Exception("All matches are banned")

    if is_odd(len(names)):
        unmatched_player = random.choice(names)
        available_matches -= {m for m in available_matches if unmatched_player in m}
        names.remove(unmatched_player)

    matches = match_players(names, available_matches)

    return matches, unmatched_player, exhausted_players

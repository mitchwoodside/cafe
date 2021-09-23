import random
import csv
import math

import click

def split_list(a):
    half = len(a)//2
    return a[:half], a[half:]

@click.group()
def cli():
    pass

@cli.command()
@click.option("-l", "--list", "options_file", default="list.csv")
@click.option("-b", "--banned", "banned_matches_file", default="banned.csv")
@click.option("-u", "--update", "update", is_flag=True)
def spin(options_file, banned_matches_file, update):
    names = []
    banned_matches = set()
    matches = []
    matches_exhausted = []
    unmatched = []

    with open(options_file, newline="") as options_csv:
        reader = csv.reader(options_csv)
        for row in reader:
            names.append(row[0])

    with open(banned_matches_file, newline="") as banned_csv:
        reader = csv.reader(banned_csv)
        for row in reader:
            banned_matches.add(frozenset(row))

    names = list(set(names))

    for name in names:
        names_banned_matches = [i for i in banned_matches if name in i]
        banned_match_count = len(names_banned_matches)
        if banned_match_count >= len(names) - 1:
            matches_exhausted.append(name)

        banned_matches.add(frozenset((name,name)))

    for name in matches_exhausted:
        names.pop(names.index(name))

    if len(names) != 2 * (len(names)//2):
        names.append("")

    if len(banned_matches) >= math.comb(len(names),2):
        click.echo("all matches are banned")
        return

    names_list = names.copy()

    while True:
        random.shuffle(names_list)
        a,b = split_list(names_list)
        matches = {frozenset(i) for i in zip(a, b)}
        if not matches & banned_matches:
            break

    for name in matches_exhausted:
        click.echo("no matches available for {}".format(name))

    for match in matches:
        match = tuple(match)
        if "" in match:
            unmatched.append(match[0] if match[0] else match[1])
        else:
            click.echo("{}\t<-->\t{}".format(match[0],match[1]))

    if unmatched:
        for name in unmatched:
            click.echo("{} went unmatched".format(name))

    if update:
        with open(banned_matches_file, "a", newline="") as banned_csv:
            writer = csv.writer(banned_csv)
            writer.writerows(matches)

if __name__ == "__main__":
    cli()

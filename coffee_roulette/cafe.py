import random
import csv
import math

import click

from coffee_roulette.match import get_matches

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

    with open(options_file, newline="") as options_csv:
        reader = csv.reader(options_csv)
        for row in reader:
            names.append(row[0].strip())

    with open(banned_matches_file, mode="r+", newline="") as banned_csv:
        reader = csv.reader(banned_csv)
        for row in reader:
            banned_matches.add(frozenset(map(lambda x: x.strip(), row)))
        banned_csv.seek(0)
        if not banned_csv.read()[-1] == "\n":
            banned_csv.write("\n")

    matches, unmatched_player, exhausted_players = get_matches(names, banned_matches)

    for name in exhausted_players:
        click.echo("no matches available for {}".format(name))

    for match in matches:
        match = tuple(match)
        click.echo("{}\t<-->\t{}".format(match[0],match[1]))

    if unmatched_player:
        click.echo("{} went unmatched".format(unmatched_player))

    if update:
        with open(banned_matches_file, "a", newline="") as banned_csv:
            writer = csv.writer(banned_csv)
            writer.writerows(matches)

if __name__ == "__main__":
    cli()

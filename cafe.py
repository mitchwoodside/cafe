import random
import csv

import click

@click.group()
def cli():
    pass

@cli.command()
@click.option("-l", "--list", "options_file", default="list.csv")
@click.option("-b", "--banned", "banned_matches_file", default="banned.csv")
def spin(options_file, banned_file):
    names = []
    banned_matches = []
    matches = []

    with open(options_file, newline="") as options_csv:
        reader = csv.reader(options_csv)
        for row in reader:
            names.append(row[0])

    with open(banned_file, newline="") as banned_csv:
        reader = csv.reader(banned_csv)
        for row in reader:
            banned_matches.append(row)

    names_list = names.copy()

    for name in names:
        if name in names_list:
            names_list.pop(names_list.index(name))
            potential_matches = names_list.copy()

            relevant_banned_matches = [i for i in banned_matches if name in i]
            banned_names = []
            for match in relevant_banned_matches:
                for banned_name in match:
                    if name != banned_name:
                        banned_names.append(banned_name)


            for banned_name in banned_names:
                if banned_name in potential_matches:
                    potential_matches.pop(potential_matches.index(banned_name))

            try:
                new_match = random.choice(potential_matches)
            except:
                click.echo("no possible matches for {}".format(name))
                continue

            names_list.pop(names_list.index(new_match))

            matches.append((name, new_match))
            click.echo("{} - {}".format(name, new_match))
        else:
            continue

if __name__ == "__main__":
    cli()

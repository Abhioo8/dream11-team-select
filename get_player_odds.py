import argparse
import operator
import pandas as pd
from tabulate import tabulate
from collections import OrderedDict


def main(file_name="players.txt", sortby=1, use_df=False):
    player_dict = dict()
    with open(file_name) as f:
        players = f.readlines()
    for i,j in zip(range(0,len(players),2), range(1,len(players),2)):
        player_dict[players[i].strip('\n').strip()] = float(players[j].strip('\n').strip())
    if sortby == 1:
        sorted_players = sorted(player_dict.items(), key=operator.itemgetter(sortby), reverse=True)
    else:
        sorted_players = sorted(player_dict.items(), key=operator.itemgetter(sortby))
    ordered_players = OrderedDict(sorted_players)
    if use_df:
        df = pd.DataFrame(sorted_players)
        tabular_df = tabulate(df, headers='keys', tablefmt='psql')
        print(tabular_df)
    return ordered_players


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="An utility that reads\
                                    the given file having two team players\
                                    separated by commas and generate required\
                                    number of pairs of cap and vice-cap")
    arg_group = parser.add_argument_group("Required Arguments")
    arg_group.add_argument("-f", "--filename", required=True, help="A File name\
                            which consists of captains and vice-captains\
                            from two team players respectively")
    arg_group.add_argument("-s", "--sortby", required=True, help="An argument\
                            which tells to sort by player name or odds?")
    arg_group.add_argument("-d", "--usedf", required=False, help="This tells \
                           whether to use DataFrames or not")
    args = parser.parse_args()
    file_name = args.filename
    sortby = args.sortby
    use_df = 0
    if args.usedf:
        use_df = args.usedf
        try:
            use_df = int(use_df)
        except ValueError:
            raise ValueError("-d argument should be an integer")
    try:
        sortby = int(sortby)
    except ValueError:
        raise ValueError("-s argument should be an integer")
    main(file_name, sortby, use_df)

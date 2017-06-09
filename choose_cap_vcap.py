import argparse
from random import sample


def main():
    parser = argparse.ArgumentParser(description="An utility that reads\
                                    the given file having two team players\
                                    separated by commas and generate required\
                                    number of pairs of cap and vice-cap")
    arg_group = parser.add_argument_group("Required Arguments")
    arg_group.add_argument("-f", "--filename", required=False, help="A File name\
                            which consists of captains and vice-captains\
                            from two team players respectively")
    arg_group.add_argument("-n", "--number", required=True, help="Total number\
                            of cap and vice-cap pairs")
    args = parser.parse_args()
    file_name = args.filename if args.filename else 'choose_cap_vcap.txt'
    try:
        pairs = int(args.number)
    except ValueError:
        print("-n should be an integer")
        return
    with open(file_name, 'r') as f:
        total_players = f.readlines()
    if(len(total_players) > 2):
        print("Only two lines are needed")
        return
    cap = [x.strip(",").strip("\n").strip() for x in total_players[0].split(",")]
    vcap = [x.strip(",").strip("\n").strip() for x in total_players[1].split(",")]
    if pairs > (len(cap) or len(vcap)):
        print("cap or vcap list should be less than number of pairs required")
        return
    # all_possible_combinations = [(each_cap, each_vcap) for each_cap in cap for each_vcap in vcap]
    # res = []
    # for each_num in range(pairs):
        # x = sample(all_possible_combinations, 1).pop()
        # temp = set()
        # for each_x in x:
            # for each_combination in all_possible_combinations:
              #  if each_x in each_combination:
               #     temp.add(each_combination)
        #all_possible_combinations = list(set(all_possible_combinations) - temp)
        #res.append(x)
    # res = sample(list(zip(cap, vcap)), pairs)
    res = sample(zip(cap, vcap), pairs)
    print("******** possible cap and vice-cap ********\n")
    print("cap\tvice-cap")
    for each_res in res:
        for z in each_res:
            print(z+"\t"),
        print


if __name__ == '__main__':
    main()

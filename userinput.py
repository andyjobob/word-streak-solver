import sys
import re

def proces_inputs(args):
    """ Takes input file and breaks data into two list of lists
    1. Word Grid
    2. Bonus Grid

    :param args: Input from sys.argv
    :return: grid, bonus
    """

    # Check for correct number of inputs
    if len(args) != 2:
        print("    Usage: python wordstreak.py <INPUT_FILE>")
        sys.exit()

    # Try opening input file, else exit
    try:
        infh = open(args[1], "r")
    except:
        print("    Error: unable to open input file {0}".format(args[1]))
        sys.exit()

    grid = []
    bonus = []
    linecnt = 0
    for line in infh:
        linecnt += 1
        line = line.rstrip()

        # First four lines should be the word grid
        if linecnt <= 4:
            grid.append(list(line))
            #grid.append(re.split(r".", line))

        # Second four lines should the bonus grid
        elif 4 < linecnt <= 8:
            bonus.append(line.split(","))

        # All other lines are ignored
        else:
            print("    Extra line ({0}) in input file".format(linecnt))

    return grid, bonus

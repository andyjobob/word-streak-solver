import sys
import os
import pickle


def process_inputs(args):
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


def load_dictionary():
    """ Loads words from dictionary file into a list

    :return: returns list of words
    """
    file_path = "enable1_qu_mod.txt"
    pkl_file = "enable1_qu_mod.pkl"
    pkl_exists = False

    # Check if file exists and get file info
    if os.path.isfile(file_path):
        file_name = os.path.basename(file_path)
        file_info = os.stat(file_path)
        file_size = file_info.st_size
        file_mtime = file_info.st_mtime
    else:
        sys.exit("Dictionary file ({0}) does not exist!!!".format(file_path))

    # Check if pickled version of dictionary data already exists and is valid
    if os.path.isfile(pkl_file):
        pkl_exists = True
        print("    Reading in pickled data ...")
        with open(pkl_file, 'rb') as file_handle:
            word_dictionary = pickle.load(file_handle)

        if "FileName" in word_dictionary.keys():
            if not word_dictionary["FileName"] == file_name:
                pkl_exists = False
                print("    Pickled data does not match on file name {0} != {1}".format(
                    file_name, word_dictionary["FileName"]))
        else:
            pkl_exists = False
            print("    Pickled data does not contain file name")

        if "FileSize" in word_dictionary.keys():
            if not word_dictionary["FileSize"] == file_size:
                pkl_exists = False
                print("    Pickled data does not match on file size {0} != {1}".format(
                    file_name, word_dictionary["FileSize"]))
        else:
            pkl_exists = False
            print("    Pickled data does not contain file size")

        if "FileMTime" in word_dictionary.keys():
            if not word_dictionary["FileMTime"] == file_mtime:
                pkl_exists = False
                print("    Pickled data does not match on file mod time {0} != {1}".format(
                    file_mtime, word_dictionary["FileMTime"]))
        else:
            pkl_exists = False
            print("    Pickled data does not contain file mod time")

    else:
        pkl_exists = False

    # If the pickled data does not exist or is not valid, re-read the words from file and re-pickle
    if not pkl_exists:
        word_dictionary = dict()
        word_dictionary["FileName"] = file_name
        word_dictionary["FileSize"] = file_size
        word_dictionary["FileMTime"] = file_mtime

        # Load dictionary word list
        print("    Reading in word list ...")
        words = []
        with open(file_path, "r") as file_handle:
            for line in file_handle:
                words.append(line.strip())
        word_dictionary["Words"] = words
        print("    Done, read {0} words".format(len(words)))

        # Pickle data to file
        print("    Writing data for future use: {} ".format(pkl_file))
        with open(pkl_file, "wb") as file_handle:
            pickle.dump(word_dictionary, file_handle, pickle.HIGHEST_PROTOCOL)
        print("    Done!")

    return word_dictionary["Words"]

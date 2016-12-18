# TODO: Currently the word search algo stops when the first occurence of a word is found.
#       This would exclude possible other occurrences of the same word that may have higher point values.

print("Reading in word list ...")
fh = open("enable1.txt", "r")

words = []
word_count = 0
for line in fh:
    words.append(line.strip())
    word_count += 1

#words = ["flied", "filed", "fled", "oldest", "soled", "help", "stole", "pa", "hoe", "shed", "magnet", "doer", "forget"]
print("Done, read {0} words".format(word_count))

grid = [["j", "n", "a", "s"],
        ["i", "l", "o", "r"],
        ["n", "u", "e", "d"],
        ["g", "s", "t", "z"]]

bonus = [["", "", "", ""],
         ["", "3l", "", ""],
         ["3l", "3l", "3w", ""],
         ["", "", "", ""]]

letter_values = {"a": 1, "b":  4, "c": 4, "d":  2, "e": 1, "f": 4,
                 "g": 3, "h":  3, "i": 1, "j": 10, "k": 5, "l": 2,
                 "m": 4, "n":  2, "o": 1, "p":  4, "?": 0, "r": 1,
                 "s": 1, "t":  1, "u": 2, "v":  5, "w": 4, "x": 8,
                 "y": 3, "z": 10}

# Word length bonus {word_length: bonus}
length_bonus = {1: 0, 2: 0, 3: 0, 4: 0, 5: 3, 6: 6, 7: 10, 8: 15, 9: 15, 10: 15, 11: 15, 12: 15}


def func(prevcoor_array, working_answer):
    """

    :param prevcoor_array:
    :param working_answer:
    :return:
    """
    temp_char = word[len(working_answer)]
    array = build_array(prevcoor_array, temp_char)

    # If the next character is found in at leas one valid position (array exists), then keep looking
    if array:
        for thing in array:

            if working_answer + temp_char == word:
                temp_list = prevcoor_array[:]
                temp_list.append(thing)
                return temp_list
            else:
                temp_list = prevcoor_array[:]
                temp_list.append(thing)
                result = func(temp_list, working_answer + temp_char)
                if result is not None:
                    return result

        # If after all things in array the word is not found, then return none
        return None

    # If the next character was not found in any valid position (array is empty), then return none
    else:
        return None


def build_array(prevcoor_array, char):
    """

    :param prevcoor_array:
    :param char:
    :return:
    """
    array = []

    # If first time to build array look over whole grid for matching character
    if len(prevcoor_array) == 0:
        for row in range(4):
            for col in range(4):
                if grid[row][col] == char:
                    array.append((row, col))

    # All other times, look around character found last
    else:
        last_coor = prevcoor_array[-1]
        for row in range(last_coor[0] - 1, last_coor[0] + 2):
            if (row < 0) or (row > 3):
                continue

            for col in range(last_coor[1] - 1, last_coor[1] + 2):
                if (col < 0) or (col > 3):
                    continue

                if (row, col) in prevcoor_array:
                    continue

                if grid[row][col] == char:
                    array.append((row, col))

    return array


def get_score(word, word_array):
    """ Formula = sum(letter_value * letter_bonus) * word_bonus) + length_bonus)

    :param word_array:
    :return:
    """

    total_points = 0
    sum_letter_points = 0
    word_bonus = 1  # Default multiplier
    for coor in word_array:
        letter_bonus = 1  # Default multiplier

        # Get and decode bonus chars for each letter
        bonus_chars = bonus[coor[0]][coor[1]]
        if len(bonus_chars) == 2:
            if bonus_chars[1] == "l":
                letter_bonus = int(bonus_chars[0])
            elif bonus_chars[1] == "w":
                word_bonus *= int(bonus_chars[0])

        # Add letter points the the running sum of letter points
        sum_letter_points += letter_values[grid[coor[0]][coor[1]]] * letter_bonus

    # Calculate total points
    total_points = (sum_letter_points * word_bonus) + length_bonus[len(word)]

    return total_points

#####################################################################
### MAIN
#####################################################################
print("Looking for words in grid ...")
answer_dict = {}
word_count = 0
for word in words:

    word_array = func([], "")

    if word_array:
        word_count += 1
        word_score = get_score(word, word_array)
        answer_dict[word] = (word_score, word_array)

print("Done, found {0} words".format(word_count))

# Sort answers based on score
for word in sorted(answer_dict, key=lambda x: answer_dict[x][0]):
    print("Found word: {0:20} Score: {1:3}  Points: {2}".format(word, answer_dict[word][0], answer_dict[word][1]))


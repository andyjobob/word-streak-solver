from userinput import *


def find_word(word, prev_coor_array, working_answer):
    """ Recursively searches for given word in letter grid, letter by letter
    Example returned data (two solutions for the same word):
    [[(1, 0), (0, 1), (1, 1), (2, 2), (3, 2)],
     [(1, 0), (2, 0), (1, 1), (2, 2), (3, 2)]]

    :param word:
    :param prevcoor_array:
    :param working_answer:
    :return: A list of lists of tuple coordinates
    """
    result = None

    # Get the next character to look for, based off of how many characters already found
    temp_char = word[len(working_answer)]

    # Look for character and return array of coordinates, (row, column) tuples, corresponding to valid matches
    coor_array = find_next_char(prev_coor_array, temp_char)

    # If the next character is found in at least one valid position (array exists), then keep looking
    if coor_array:
        # For each coordinate found
        for coordinate in coor_array:
            # Check to see if word has been completely found
            if working_answer + temp_char == word:
                temp_coor_array = prev_coor_array[:]  # Make a copy
                temp_coor_array.append(coordinate)    # Append final coordinate
                if result is None:
                    result = []
                result.append(temp_coor_array)
            else:
                temp_coor_array = prev_coor_array[:]  # Make a copy
                temp_coor_array.append(coordinate)
                temp_result = find_word(word, temp_coor_array, working_answer + temp_char)
                if temp_result:
                    if result is None:
                        result = []
                    result.extend(temp_result)

        # Return the result after going through all coordinates in coor_array
        return result

    # If the next character was not found in any valid position (array is empty), then return none
    else:
        return None


def find_next_char(prev_coor_array, char):
    """ Finds all the coordinate pairs for the next character in the word, if any.
    Coordinates must be adjacent to the last coordinate found in the word and must not include any coordinates
    that are already part of the word.

    :param prev_coor_array: Coordinates that are already part of the word
    :param char: The next character we are looking for
    :return: Array of coordinates, (row, col) tuples, representing valid character matches
    """
    ret_array = []

    # If first time to build array look over whole grid for matching characters
    if len(prev_coor_array) == 0:
        for row in range(4):
            for col in range(4):
                if grid[row][col] == char:
                    ret_array.append((row, col))

    # All other times, look around character found last
    else:
        last_coor = prev_coor_array[-1]

        # Loop over rows starting from one less, to one more than last coordinate row
        for row in range(last_coor[0] - 1, last_coor[0] + 2):
            # If row is off grid, continue to next coordinate
            if (row < 0) or (row > 3):
                continue

            # Loop over columns starting from one less, to one more than last coordinate column
            for col in range(last_coor[1] - 1, last_coor[1] + 2):
                # If column is off grid, continue to next coordinate
                if (col < 0) or (col > 3):
                    continue

                # If coordinate already part of word move to next coordinate
                if (row, col) in prev_coor_array:
                    continue

                # If character at given coordinate matches the character we are looking for, append to retrun array
                if grid[row][col] == char:
                    ret_array.append((row, col))

    return ret_array


def get_score(word, word_array):
    """ Calculate the score of a found word
    Formula = sum(letter_value * letter_bonus) * word_bonus) + length_bonus)

    :param word:
    :param word_array:
    :return: Integer that is total point value of word
    """

    total_letter_points = 0
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
        total_letter_points += letter_values[grid[coor[0]][coor[1]]] * letter_bonus

    # Calculate total points
    total_points = (total_letter_points * word_bonus) + length_bonus[len(word)]

    return total_points

#####################################################################
### MAIN
#####################################################################
print("Loading inputs ...")

#  Load dictionary data
words = load_dictionary()

# Process input file to populate the word grid and bonus grid, each is a list of lists
grid, bonus = process_inputs(sys.argv)

# Letter values dictionary, used to calculate word score
letter_values = {"a": 1, "b":  4, "c": 4, "d":  2, "e":  1, "f": 4,
                 "g": 3, "h":  3, "i": 1, "j": 10, "k":  5, "l": 2,
                 "m": 4, "n":  2, "o": 1, "p":  4, "?": 10, "r": 1,
                 "s": 1, "t":  1, "u": 2, "v":  5, "w":  4, "x": 8,
                 "y": 3, "z": 10}

# Word length bonus {word_length: bonus}
length_bonus = {1: 0, 2: 0, 3: 0, 4: 0, 5: 3, 6: 6, 7: 10, 8: 15, 9: 15, 10: 15, 11: 15, 12: 15}

print("Looking for words in grid ...")
answer_dict = {}
word_count = 0

# For each word in list of dictionary words
for word in words:

    # Recursively search for word in letter grid, find all possible solutions, returns a list of lists of tuple coordinates
    word_array = find_word(word, [], "")

    if word_array:
        word_count += 1
        for letter_array in word_array:
            word_score = get_score(word, letter_array)
            if word in answer_dict.keys():
                print("    Already found word {0}, this one worth {1}".format(word, word_score))
                if word_score > answer_dict[word][0]:
                    answer_dict[word] = (word_score, letter_array)
            else:
                answer_dict[word] = (word_score, letter_array)

print("Done, found {0} unique words".format(word_count))

# Sort answers based on score
#for word in sorted(answer_dict, key=lambda x: answer_dict[x][0]):
#    print("Found word: {0:20} Score: {1:3}  Points: {2}".format(word, answer_dict[word][0], answer_dict[word][1]))

# Sort answers alphabetically
#for word in sorted(answer_dict.keys()):
#    print("Found word: {0:20} Score: {1:3}  Points: {2}".format(word, answer_dict[word][0], answer_dict[word][1]))

# Sort answers based on letter coordinates
last_coor = None
word_group = []
word_group_score = 0
word_group_list = []
for word in sorted(answer_dict, key=lambda x: answer_dict[x][1]):
    curr_coor = answer_dict[word][1][:2]  # Store first two coordinates of word

    # If last coordinates match the current coordinates, add word to group
    if last_coor == curr_coor:
        word_group.append(word)
        word_group_score += answer_dict[word][0]

    # If not, then append group to group list and start new group
    else:
        word_group_list.append([word_group_score, word_group])
        word_group = [word]
        word_group_score = answer_dict[word][0]

    # Update last coordinates
    last_coor = curr_coor

# Print out words in groups sorted by total group score
for group in sorted(word_group_list, key=lambda x: x[0]):
    for word in group[1]:
        print("    Found word: {0:20} Score: {1:3}  Points: {2}".format(word, answer_dict[word][0], answer_dict[word][1]))

    print("Total Group Score: {0}".format(group[0]))

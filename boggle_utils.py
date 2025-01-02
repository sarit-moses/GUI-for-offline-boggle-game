##############################################################################
#                                   Imports                                  #
##############################################################################
from typing import List, Tuple, Iterable, Optional

##############################################################################

##############################################################################
#                                   TYPING                                   #
##############################################################################
Board = List[List[str]]
Path = List[Tuple[int, int]]

##############################################################################

##############################################################################
#                                   FUNCTIONS                                #
##############################################################################

##############################################################################


def __find_in_database(words: List[str], word: str,
                       length: Optional[int] = None):
    '''
    Description: This function get an iterable object, and find in the object
    some substring with binary search.
    '''

    low: int = 0
    high: int = len(words) - 1
    
    # checking if substring in the database with binary search
    # (if length is None check if full word in the database).
    while low <= high:
        mid = (high + low) // 2
        
        if words[mid][:length] == word:  # the substring in the database
            return True

        elif words[mid][:length] < word:
            low = mid + 1  # take the right side of the database
 
        elif words[mid][:length] > word:
            high = mid - 1  # take the left side of the database

    return False  # the substring not found in the database


def is_valid_path(board: Board, path: Path,
                  words: Iterable[str]) -> Optional[str]:
    '''
    Description: This function get a path in the boggle game and
                 return the word if its valid, None else.  
    '''
    new_word: str = ''
    previous_moves: Path = []
    
    # transform the database of words to sorted
    word_list: List[str] = list(words)
    word_list = sorted(word_list)
    
    # check if all moves in the path is legal.
    for move in range(len(path)):

        # check if the move is not the first move -
        # check if its legal move from the previous move
        if move != 0:
            if abs(path[move][0] - path[move - 1][0]) > 1:
                return None
            if abs(path[move][1] - path[move - 1][1]) > 1:
                return None

        # check if this cube is already taken or out of board.
        if not __correct_move(board, path[move][0], path[move][1],
                              previous_moves):
            return None
        
        # add the letter from the current cube to the new word.
        row_index: int = path[move][0]
        column_index: int = path[move][1]
        new_letter: str = board[row_index][column_index]
        new_word += new_letter
        previous_moves.append(path[move])
    
    # check if the word getting from the path is in database.
    if __find_in_database(word_list, new_word):
        return new_word
    else:
        return None


def __correct_move(board: Board, row: int, col: int, previous_moves: Path):
    '''
    Description: This function check if the move in the path is legal
                 - not taken already or out of board.
    '''
    if row >= 0 and row < len(board) and col >= 0 and col < len(board[0]) \
            and (row, col) not in previous_moves:
        return True
    else:
        return False


def _find_length_n_helper(n: int, length: int, current_row: int,
                          current_col: int, board: Board, words: List[str],
                          current_word: str, current_path: Path,
                          found_n_paths: List[Path],
                          found_n_words_paths: List[str],
                          n_words_checking: bool) -> None:
    '''
    Description: This function search all paths with n length that make legal
                 word by backtracking.
                 If the function find a correct path - 
                 its save the word and the path in lists getting as parameters.
    '''
    # if the path length is n:
    # add the path to the lists of n_paths and n_words_paths
    if length >= n:
        if __find_in_database(words, current_word):
            found_n_paths.append(current_path[:])
            found_n_words_paths.append(current_path[:])
        return  # stopping the backtracking
    
    # if the length of the getting word from the path is n -
    # add the path to the list of n_words_paths.
    if len(current_word) == n:
        if __find_in_database(words, current_word):
            found_n_words_paths.append(current_path[:])
        if n_words_checking:
            return  # stopping the backtracking
    
    # recursive calling the function with next move to all sides of the cube,
    # if this cube was not taken until now.
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (not (i == 0 and j == 0)
                and __correct_move(board, current_row + i, current_col + j,
                                   current_path) and
                    __find_in_database(words, current_word,
                                       len(current_word))):
                current_word += board[current_row + i][current_col + j]
                current_path += [(current_row + i, current_col + j)]
                length += 1

                _find_length_n_helper(n, length, current_row + i,
                                      current_col + j, board, words,
                                      current_word, current_path,
                                      found_n_paths, found_n_words_paths,
                                      n_words_checking)
                
                length -= 1
                current_word = current_word[:-(len(board[current_row + i]
                                                   [current_col + j]))]
                del current_path[-1]
                
            
def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> \
        List[Path]:
    '''
    Description: This function search all paths with n length that make legal
                 word by backtracking.
                 The function return a sorted list of all correct paths.
    '''
    if n <= 0:
        return []
    
    length_n_paths: list = []

    # transform the database of words to sorted
    word_list = list(words)
    word_list = sorted(word_list)

    # get all n length paths from every cube in the board with recursion.
    for start_row in range(len(board)):
        for start_col in range(len(board[0])):
            current_word = board[start_row][start_col]
            current_path = [(start_row, start_col)]
            _find_length_n_helper(n, 1, start_row, start_col, board, word_list,
                                  current_word, current_path, length_n_paths,
                                  [], False)
    
    return length_n_paths


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> \
        List[Path]:
    '''
    Description: This function search all paths with n length that make legal
                 word by backtracking.
                 The function return a list of all correct words.
    '''
    if n <= 0:
        return []
    
    length_n_words_paths: list = []

    # transform the database of words to sorted
    word_list = list(words)
    word_list = sorted(word_list)

    # get all n length words paths from every cube in the board with recursion.
    for start_row in range(len(board)):
        for start_col in range(len(board[0])):
            current_word = board[start_row][start_col]
            current_path = [(start_row, start_col)]
            _find_length_n_helper(n, 1, start_row, start_col, board, word_list,
                                  current_word, current_path, [],
                                  length_n_words_paths, True)
    
    return length_n_words_paths


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    '''
    Description: This function return a list of paths that give the max score
    in the game.
    '''
    # transform the database of words to sorted
    word_list = list(words)
    word_list = sorted(word_list)

    max_words: list = []
    max_paths: list = []

    # check all length from the max board size to 1,
    # and save all new words getting from the board
    for length in range((len(board) * len(board[0])), 0, -1):
        for path in find_length_n_paths(length, board, word_list):
            new_word = is_valid_path(board, path, word_list)
            
            # check if is legal word and the word not taken already.
            if new_word is not None and (new_word not in max_words):
                max_paths.append(path)
                max_words.append(new_word)
    
    return max_paths

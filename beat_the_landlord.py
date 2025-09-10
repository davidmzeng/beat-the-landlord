"""
In working on this project, I remembered Michael Smyers again and 
wondered what he would have thought of this. Rest in peace, Michael;
"don't let perfect be the enemy of good" and "problem exists between chair and keyboard"
seemed relevant to my experience coding this.
"""


import random # for shuffling collections
from itertools import combinations # for enumerating combinations
import time # for slowing down printed outputs

# establishes relative ordering of values
RANK_ORDER = ("3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A", "2", "B", "R")

# establishes defined combos 
DEFINED_COMBOS = ("single", 
                  "sequence of singles", 
                  "pair", 
                  "sequence of pairs", 
                  "triplet", 
                  "triplet with single", 
                  "triplet with pair", 
                  "sequence of triplets", 
                  "sequence of triplets with singles", 
                  "sequence of triplets with pairs",
                  "quad with two singles",
                  "quad with two pairs",
                  "bomb", 
                  "rocket")

def generate_shuffled_deck(): 
    """
    Constructs and returns a shuffled standard deck without suits
    """
    deck = []
    for rank in RANK_ORDER: # add all the cards to the deck
        if rank != "B" and rank != "R": # add four of each card except Jokers
            for i in range(4):
                deck.append(rank)
        else: 
            deck.append(rank)
    random.shuffle(deck) # shuffle deck
    return deck

def deal_hands_with_leftovers(deck):
    """
    Takes a deck as an argument and "deals it," returning three hands
    and a leftover pile of cards for bidding.
    It mirrors "real-life" dealing by dealing from top of deck and 
    leaving an empty deck after dealing,
    """
    if len(deck) != 54:
        raise ValueError("deal_hands_with_leftovers expects a 54-card deck")
    hand_1 = []
    hand_2 = []
    hand_3 = []
    leftovers = []
    for i in range(17): # deal cards to each person in order
        hand_1.append(deck.pop(0))
        hand_2.append(deck.pop(0))
        hand_3.append(deck.pop(0))
    for j in range(3):
        leftovers.append(deck.pop(0)) # the remaining "deck" is the leftovers pile
    return hand_1, hand_2, hand_3, leftovers 

def sorted_cards(cards): 
    """ 
    Takes cards as an argument and returns a new group of sorted cards
    """
    for card in cards: # check for invalid cards
        if card not in RANK_ORDER: 
            raise ValueError("invalid card found")
    sorted_result = []
    for rank in RANK_ORDER: # iterate in sorted order
        for card in cards:
            if card == rank:
                sorted_result.append(card)
    return sorted_result

def get_rank(card):
    """ 
    Takes a card as an argument and returns a value representing its relative
    rank compared with other cards 
    """
    if card not in RANK_ORDER: # check that card isn't invalid
        raise ValueError("invalid card")
    return RANK_ORDER.index(card)

def get_combo_type(combo): 
    """ 
    Takes a combo (a group of cards) as an argument and returns what kind
    of combo it is, returns "invalid combo" if not a valid combo
    """
    # given cases are mutually exclusive 
    if is_single(combo):
        return "single"
    elif is_sequence_of_singles(combo):
        return "sequence of singles"
    elif is_pair(combo):
        return "pair"
    elif is_sequence_of_pairs(combo):
        return "sequence of pairs"
    elif is_triplet(combo):
        return "triplet"
    elif is_triplet_with_single(combo):
        return "triplet with single"
    elif is_triplet_with_pair(combo):
        return "triplet with pair"
    elif is_sequence_of_triplets(combo):
        return "sequence of triplets"
    elif is_sequence_of_triplets_with_singles(combo):
        return "sequence of triplets with singles"
    elif is_sequence_of_triplets_with_pairs(combo):
        return "sequence of triplets with pairs"
    elif is_quad_with_two_singles(combo):
        return "quad with two singles"
    elif is_quad_with_two_pairs(combo):
        return "quad with two pairs"
    elif is_bomb(combo):
        return "bomb"
    elif is_rocket(combo):
        return "rocket"
    else:
        return "invalid combo"
    
def is_single(combo):
    """ 
    Takes a combo as an argument and returns True if it is a "single" combo type, returns False otherwise
    """
    return (len(combo) == 1 and combo[0] in RANK_ORDER) # any one defined card rank counts as a single

def is_sequence_of_singles(combo):
    """ 
    Takes a combo as an argument and returns True if it is a "sequence of singles" combo type, 
    returns False otherwise
    """
    for card in combo: # check for invalid cards
        if card not in RANK_ORDER:
            return False
    if len(combo) < 5 or "2" in combo or "B" in combo or "R" in combo: # invalid combos 
        return False
    sorted_combo = sorted_cards(combo)
    for i in range(len(sorted_combo) - 1): # check if cards are consecutive
        if get_rank(sorted_combo[i]) != get_rank(sorted_combo[i + 1]) - 1: 
            return False 
    return True

def is_pair(combo):
    """ 
    Takes a combo as an argument and returns True if it is a "pair" combo type, returns False otherwise
    """
    if len(combo) != 2: # check for invalid number of cards
        return False
    for card in combo: # check for invalid cards
        if card not in RANK_ORDER:
            return False
    return (combo[0] == combo[1])

def is_sequence_of_pairs(combo):
    """ 
    Takes a combo as an argument and returns True if it is a "sequence of pairs" combo type, 
    returns False otherwise
    """
    for card in combo: # check for invalid cards
        if card not in RANK_ORDER:
            return False
    if "2" in combo or "B" in combo or "R" in combo: # check for invalid cards used in combo
        return False
    rank_counts = {} 
    for card in combo: # put combo into a dictionary representing frequency of each card 
        if card not in rank_counts:
            rank_counts[card] = 1
        else:
            rank_counts[card] += 1
    for rank in rank_counts: # check all cards used are pairs
        if rank_counts[rank] != 2:
            return False
    if len(rank_counts) < 3: # check for at least 3 pairs
        return False
    ranks_list = list(rank_counts.keys()) 
    sorted_ranks_list = sorted_cards(ranks_list) # get a sorted list of the ranks in combo
    for i in range(len(sorted_ranks_list) - 1): # check ranks are consecutive
        if get_rank(sorted_ranks_list[i]) != get_rank(sorted_ranks_list[i + 1]) - 1:
            return False
    return True

def is_triplet(combo):
    """ 
    Takes a combo as an argument and returns True if it is a "triplet" combo type, returns False otherwise
    """
    if len(combo) != 3: # check for invalid number of cards
        return False
    for card in combo: # check for invalid cards
        if card not in RANK_ORDER:
            return False
    return (combo[0] == combo[1] and combo[1] == combo[2])

def is_triplet_with_single(combo):
    """ 
    Takes a combo as an argument and returns True if it is a "triplet with single" combo type, returns False otherwise
    """
    if len(combo) != 4: # check for invalid number of cards
        return False
    for card in combo: # check for invalid cards
        if card not in RANK_ORDER: 
            return False
    rank_counts = {}
    for card in combo: # put combo into a dictionary representing frequency of each card
        if card not in rank_counts: 
            rank_counts[card] = 1
        else:
            rank_counts[card] += 1
    for card in combo: 
        if rank_counts[card] != 3 and rank_counts[card] != 1: # check that we have only triplets and singles 
            return False
    counts_list = list(rank_counts.values()) # get all the counts of each rank
    count_triplets = counts_list.count(3) # counts how many triplets exist
    count_singles = counts_list.count(1) # counts how many singles exist
    return (count_triplets == 1 and count_singles == 1)

def is_triplet_with_pair(combo):
    """ 
    Takes a combo as an argument and returns True if it is a "triplet with pair" combo type, returns False otherwise
    """
    if len(combo) != 5: # check for invalid number of cards
        return False
    for card in combo: # check for invalid cards
        if card not in RANK_ORDER: 
            return False
    rank_counts = {}
    for card in combo: # put combo into a dictionary representing frequency of each card
        if card not in rank_counts: 
            rank_counts[card] = 1
        else:
            rank_counts[card] += 1
    for card in combo: 
        if rank_counts[card] != 3 and rank_counts[card] != 2: # check that we have only triplets and pairs 
            return False
    counts_list = list(rank_counts.values()) # get all the counts of each rank
    count_triplets = counts_list.count(3) # counts how many triplets exist
    count_pairs = counts_list.count(2) # counts how many pairs exist
    return (count_triplets == 1 and count_pairs == 1)

def is_sequence_of_triplets(combo):
    """ 
    Takes a combo as an argument and returns True if it is a "sequence of triplets" combo type, 
    returns False otherwise
    """
    for card in combo: # check for invalid cards
        if card not in RANK_ORDER:
            return False
    if "2" in combo or "B" in combo or "R" in combo: # check for invalid cards used in combo
        return False
    rank_counts = {} 
    for card in combo: # put combo into a dictionary representing frequency of each card 
        if card not in rank_counts:
            rank_counts[card] = 1
        else:
            rank_counts[card] += 1
    for rank in rank_counts: # check all cards used are triplets
        if rank_counts[rank] != 3:
            return False
    if len(rank_counts) < 2: # check for at least 2 triplets
        return False
    ranks_list = list(rank_counts.keys()) 
    sorted_ranks_list = sorted_cards(ranks_list) # get a sorted list of the ranks in combo
    for i in range(len(sorted_ranks_list) - 1): # check ranks are consecutive
        if get_rank(sorted_ranks_list[i]) != get_rank(sorted_ranks_list[i + 1]) - 1:
            return False
    return True

def is_sequence_of_triplets_with_singles(combo):
    """ 
    Takes a combo as an argument and returns True if it is a "sequence of triplets with singles" combo type,
    returns False otherwise
    """
    for card in combo: # check for invalid cards
        if card not in RANK_ORDER: 
            return False
    rank_counts = {}
    for card in combo: # put combo into a dictionary representing frequency of each card 
        if card not in rank_counts:
            rank_counts[card] = 1
        else:
            rank_counts[card] += 1
    for card in combo: 
        if rank_counts[card] != 3 and rank_counts[card] != 1: # check that we have only triplets and singles 
            return False
    triplets_ranks = []
    singles_ranks = []
    for rank in rank_counts: # get ranks of triplets and ranks of singles
        if rank_counts[rank] == 3:
            triplets_ranks.append(rank)
        elif rank_counts[rank] == 1:
            singles_ranks.append(rank)
    if len(triplets_ranks) != len(singles_ranks): # number of triplets must match number of singles
        return False
    if "2" in triplets_ranks: # check for invalid cards in triplets
        return False
    if "B" in singles_ranks and "R" in singles_ranks: # check for invalid singles - both Jokers cannot be used in combo
        return False 
    if len(triplets_ranks) < 2: # check for at least 2 triplets
        return False
    sorted_triplets_ranks = sorted_cards(triplets_ranks) 
    for i in range(len(sorted_triplets_ranks) - 1): # check triplets are consecutive
        if get_rank(sorted_triplets_ranks[i]) != get_rank(sorted_triplets_ranks[i + 1]) - 1:
            return False
    return True

def is_sequence_of_triplets_with_pairs(combo):
    """ 
    Takes a combo as an argument and returns True if it is a "sequence of triplets with pairs" combo type,
    returns False otherwise
    """
    for card in combo: # check for invalid cards
        if card not in RANK_ORDER: 
            return False
    rank_counts = {}
    for card in combo: # put combo into a dictionary representing frequency of each card 
        if card not in rank_counts:
            rank_counts[card] = 1
        else:
            rank_counts[card] += 1
    for card in combo: 
        if rank_counts[card] != 3 and rank_counts[card] != 2: # check that we have only triplets and pairs 
            return False
    triplets_ranks = []
    pairs_ranks = []
    for rank in rank_counts: # get ranks of triplets and ranks of pairs
        if rank_counts[rank] == 3:
            triplets_ranks.append(rank)
        elif rank_counts[rank] == 2:
            pairs_ranks.append(rank)
    if len(triplets_ranks) != len(pairs_ranks): # number of triplets must match number of pairs
        return False
    if "2" in triplets_ranks: # check for invalid cards in triplets
        return False
    if len(triplets_ranks) < 2: # check for at least 2 triplets
        return False
    sorted_triplets_ranks = sorted_cards(triplets_ranks) 
    for i in range(len(sorted_triplets_ranks) - 1): # check triplets are consecutive
        if get_rank(sorted_triplets_ranks[i]) != get_rank(sorted_triplets_ranks[i + 1]) - 1:
            return False
    return True

def is_quad_with_two_singles(combo):
    """ 
    Takes a combo as an argument and returns True if it is a "quad with two singles" combo type,
    returns False otherwise
    """
    if len(combo) != 6: # check for invalid number of cards
        return False
    for card in combo: # check for invalid cards
        if card not in RANK_ORDER: 
            return False
    if "B" in combo and "R" in combo: # check for invalid combo - both Jokers cannot be used in combo
        return False
    rank_counts = {}
    for card in combo: # put combo into a dictionary representing frequency of each card
        if card not in rank_counts: 
            rank_counts[card] = 1
        else:
            rank_counts[card] += 1
    for card in combo: 
        if rank_counts[card] != 4 and rank_counts[card] != 1: # check that we have only quads and singles 
            return False
    counts_list = list(rank_counts.values()) # get all the counts of each rank
    count_quads = counts_list.count(4) # counts how many quads exist
    count_singles = counts_list.count(1) # counts how many singles exist
    return (count_quads == 1 and count_singles == 2)

def is_quad_with_two_pairs(combo):
    """ 
    Takes a combo as an argument and returns True if it is a "quad with two pairs" combo type,
    returns False otherwise
    """
    if len(combo) != 8: # check for invalid number of cards
        return False
    for card in combo: # check for invalid cards
        if card not in RANK_ORDER: 
            return False
    rank_counts = {}
    for card in combo: # put combo into a dictionary representing frequency of each card
        if card not in rank_counts: 
            rank_counts[card] = 1
        else:
            rank_counts[card] += 1
    for card in combo: 
        if rank_counts[card] != 4 and rank_counts[card] != 2: # check that we have only quads and pairs 
            return False
    counts_list = list(rank_counts.values()) # get all the counts of each rank
    count_quads = counts_list.count(4) # counts how many quads exist
    count_pairs = counts_list.count(2) # counts how many pairs exist
    return (count_quads == 1 and count_pairs == 2)

def is_bomb(combo):
    """ 
    Takes a combo as an argument and returns True if it is a "bomb" combo type, returns False otherwise
    """
    if len(combo) != 4: # check for invalid number of cards
        return False
    for card in combo: # check for invalid cards
        if card not in RANK_ORDER:
            return False
    return (combo[0] == combo[1] and combo[1] == combo[2] and combo[2] == combo[3])


def is_rocket(combo):
    """ 
    Takes a combo as an argument and returns True if it is a "rocket" combo type, returns False otherwise
    """
    if len(combo) != 2: # check for invalid number of cards
        return False
    for card in combo:  # check for invalid cards
        if card not in RANK_ORDER:
            return False
    return ("B" in combo and "R" in combo)


def get_combo_rank(combo):
    """ 
    Takes a combo as an argument and returns a value representing its relative
    rank compared with other combos of that same combo type
    """
    if is_single(combo):
        return get_rank(combo[0]) # assumes list of one value
    elif is_sequence_of_singles(combo):
        sorted_combo = sorted_cards(combo)
        return get_rank(sorted_combo[0]) # examines first element in sorted list
    elif is_pair(combo):
        return get_rank(combo[0]) # assumes list of two identical values
    elif is_sequence_of_pairs(combo):
        sorted_combo = sorted_cards(combo)
        return get_rank(sorted_combo[0]) # examines first element in sorted list
    elif is_triplet(combo):
        return get_rank(combo[0]) # assumes list of three identical values
    elif is_triplet_with_single(combo):
        rank_counts = {}
        for card in combo: # put combo into a dictionary representing frequency of each card 
            if card not in rank_counts:
                rank_counts[card] = 1
            else:
                rank_counts[card] += 1
        triplet_rank = None
        for rank in rank_counts: # find the rank of the triplet, which is guaranteed 
            if rank_counts[rank] == 3: 
                triplet_rank = rank
        return get_rank(triplet_rank)
    elif is_triplet_with_pair(combo):
        rank_counts = {}
        for card in combo: # put combo into a dictionary representing frequency of each card 
            if card not in rank_counts:
                rank_counts[card] = 1
            else:
                rank_counts[card] += 1
        triplet_rank = None
        for rank in rank_counts: # find the rank of the triplet, which is guaranteed 
            if rank_counts[rank] == 3: 
                triplet_rank = rank
        return get_rank(triplet_rank)
    elif is_sequence_of_triplets(combo):
        sorted_combo = sorted_cards(combo)
        return get_rank(sorted_combo[0]) # examines first element in sorted list
    elif is_sequence_of_triplets_with_singles(combo):
        rank_counts = {}
        for card in combo: # put combo into a dictionary representing frequency of each card 
            if card not in rank_counts:
                rank_counts[card] = 1
            else:
                rank_counts[card] += 1
        triplet_ranks = []
        for rank in rank_counts: # find the ranks of the triplets, which is guaranteed
            if rank_counts[rank] == 3:
                triplet_ranks.append(rank)
        sorted_triplet_ranks = sorted_cards(triplet_ranks)
        return get_rank(sorted_triplet_ranks[0]) # examines first element in sorted list
    elif is_sequence_of_triplets_with_pairs(combo):
        rank_counts = {}
        for card in combo: # put combo into a dictionary representing frequency of each card 
            if card not in rank_counts:
                rank_counts[card] = 1
            else:
                rank_counts[card] += 1
        triplet_ranks = []
        for rank in rank_counts: # find the ranks of the triplets, which is guaranteed
            if rank_counts[rank] == 3:
                triplet_ranks.append(rank)
        sorted_triplet_ranks = sorted_cards(triplet_ranks)
        return get_rank(sorted_triplet_ranks[0]) # examines first element in sorted list
    elif is_quad_with_two_singles(combo):
        rank_counts = {}
        for card in combo: # put combo into a dictionary representing frequency of each card 
            if card not in rank_counts:
                rank_counts[card] = 1
            else:
                rank_counts[card] += 1
        quad_rank = None
        for rank in rank_counts: # find the rank of the quad, which is guaranteed 
            if rank_counts[rank] == 4: 
                quad_rank = rank
        return get_rank(quad_rank)    
    elif is_quad_with_two_pairs(combo):
        rank_counts = {}
        for card in combo: # put combo into a dictionary representing frequency of each card 
            if card not in rank_counts:
                rank_counts[card] = 1
            else:
                rank_counts[card] += 1
        quad_rank = None
        for rank in rank_counts: # find the rank of the quad, which is guaranteed 
            if rank_counts[rank] == 4: 
                quad_rank = rank
        return get_rank(quad_rank) 
    elif is_bomb(combo):
        return get_rank(combo[0]) # assumes list of four identical values
    elif is_rocket(combo):
        return len(RANK_ORDER) # assign arbitrary "high value", but only one instance of this combo exists anyway
    else:
        return None # invalid combo
    
def is_playable(played_combo, playing_combo):
    """ 
    Takes a played combo and a playing combo as arguments and returns True if the playing combo
    beats the played combo (and is therefore playable), False otherwise
    """
    if get_combo_type(playing_combo) == "invalid combo": # check that playing combo is valid
        return False
    if played_combo is None: # special case where we start with no combo played yet (a "new round")
        return True
    if is_rocket(played_combo): # special case: if rocket was played, nothing beats it
        return False
    if is_rocket(playing_combo): # special case: rocket beats everything
        return True
    if is_bomb(playing_combo): # special case: if playing_combo is a bomb
        if not is_bomb(played_combo): # if played_combo is not a bomb
            return True
        else: # played_combo is also a bomb
            return (get_combo_rank(playing_combo) > get_combo_rank(played_combo))
    # at this point, neither combo is a rocket nor bomb (both combos are "regular" types) 
    # check that the played combo is the same type and same amount of cards as the played combo
    if (get_combo_type(played_combo) == get_combo_type(playing_combo)) and (len(played_combo) == len(playing_combo)): 
        return (get_combo_rank(playing_combo) > get_combo_rank(played_combo))
    else: # the combo to be played is not in the same category as the played combo or not the same amount of cards, so cannot play 
        return False
    
def get_combos(hand, combo_type): 
    """ 
    Takes a player's hand and a specified combo type as arguments and returns all the possible
    combos of the specified combo type from the hand in sorted order 
    """
    for card in hand: # check for invalid cards
        if card not in RANK_ORDER: 
            raise ValueError("invalid card in hand")
    combos = [] # initialize all possible combos of indicated combo type
    hand_dict = {}
    for card in hand: # put hand into a dictionary representing frequency of each card
        if card not in hand_dict:
            hand_dict[card] = 1
        else:
            hand_dict[card] += 1
    if combo_type == "single":
        for rank in sorted_cards(list(hand_dict.keys())): # iterate in sorted order
            found_combo = [rank]
            combos.append(found_combo)
        return combos
    elif combo_type == "sequence of singles":
        ranks_set = set(hand_dict.keys()) # get ranks of hand as as set
        possible_lengths = (5, 6, 7, 8, 9, 10, 11, 12) # check all possible lengths of a sequence of singles
        for length in possible_lengths: # check all possible lengths in order of smallest length to largest length
            for i in range((len(RANK_ORDER) - 3) - length + 1): # check all possible sequences given a length, 2's and Jokers not allowed, off-by-one for range() function
                sequence_window = RANK_ORDER[i : (i + length)] # get needed ranks for the candidate sequence
                sequence_window_set = set(sequence_window)
                if sequence_window_set.issubset(ranks_set): # check if hand contains candidate sequence ranks
                    found_combo = list(sequence_window) # should be in sorted order already
                    combos.append(found_combo)
        return combos
    elif combo_type == "pair": 
        for rank in sorted_cards(list(hand_dict.keys())): # iterate in sorted order
            if hand_dict[rank] >= 2 : # if there are at least two of the value
                found_combo = [rank, rank]
                combos.append(found_combo)
        return combos
    elif combo_type == "sequence of pairs": 
        pairs_ranks_set = set()
        for rank in hand_dict: # get all ranks that would constitute a pair
            if hand_dict[rank] >= 2:
                pairs_ranks_set.add(rank)
        possible_lengths = (3, 4, 5, 6, 7, 8, 9, 10, 11, 12) # check all possible lengths of a sequence of pairs
        for length in possible_lengths: # check all possible lengths in order of smallest length to largest length
            for i in range((len(RANK_ORDER) - 3) - length + 1): # check all possible sequences given a length, 2's and Jokers not allowed, off-by-one for range() function
                sequence_window = RANK_ORDER[i : (i + length)] # get needed ranks for the candidate sequence
                sequence_window_set = set(sequence_window)
                if sequence_window_set.issubset(pairs_ranks_set): # check if hand contains candidate sequence ranks
                    found_combo = []
                    for rank in sequence_window: # get valid combo values, should be in sorted order already
                        for j in range(2):
                            found_combo.append(rank) # re-create the valid combo with all the individual cards
                    combos.append(found_combo)
        return combos
    elif combo_type == "triplet": # need to check if contains at least three of a value
        for rank in sorted_cards(list(hand_dict.keys())): # iterate in sorted order
            if hand_dict[rank] >= 3:
                found_combo = [rank, rank, rank]
                combos.append(found_combo)
        return combos
    elif combo_type == "triplet with single": 
        triplet_ranks = []
        single_ranks = []
        for rank in sorted_cards(list(hand_dict.keys())): # iterate in sorted order
            if hand_dict[rank] >= 3:
                triplet_ranks.append(rank)
            if hand_dict[rank] >= 1: # note that triplet_ranks and single_ranks can have elements in common here
                single_ranks.append(rank) 
        for triplet_rank in triplet_ranks: # create all combinations of triplets with singles (already in sorted order)
            for single_rank in single_ranks:
                if triplet_rank != single_rank:
                    found_combo = [triplet_rank, triplet_rank, triplet_rank, single_rank]
                    combos.append(found_combo)
        return combos
    elif combo_type == "triplet with pair": 
        triplet_ranks = []
        pair_ranks = []
        for rank in sorted_cards(list(hand_dict.keys())): # iterate in sorted order
            if hand_dict[rank] >= 3:
                triplet_ranks.append(rank)
            if hand_dict[rank] >= 2: # note that triplet_ranks and pair_ranks can have elements in common here
                pair_ranks.append(rank) 
        for triplet_rank in triplet_ranks: # create all combinations of triplets with pairs (already in sorted order)
            for pair_rank in pair_ranks:
                if triplet_rank != pair_rank:
                    found_combo = [triplet_rank, triplet_rank, triplet_rank, pair_rank, pair_rank]
                    combos.append(found_combo)
        return combos
    elif combo_type == "sequence of triplets":
        triplets_ranks_set = set()
        for rank in hand_dict: # get all ranks that would constitute a triplet
            if hand_dict[rank] >= 3:
                triplets_ranks_set.add(rank)
        possible_lengths = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12) # check all possible lengths of a sequence of triplets
        for length in possible_lengths: # check all possible lengths in order of smallest length to largest length
            for i in range((len(RANK_ORDER) - 3) - length + 1): # check all possible sequences given a length, 2's and Jokers not allowed, off-by-one for range() function
                sequence_window = RANK_ORDER[i : (i + length)] # get needed ranks for the candidate sequence
                sequence_window_set = set(sequence_window)
                if sequence_window_set.issubset(triplets_ranks_set): # check if hand contains candidate sequence ranks
                    found_combo = []
                    for rank in sequence_window: # get valid combo values, should be in sorted order already
                        for j in range(3):
                            found_combo.append(rank) # re-create the valid combo with all the individual cards
                    combos.append(found_combo)
        return combos
    elif combo_type == "sequence of triplets with singles":
        triplet_ranks_set = set()
        for rank in hand_dict: # get all ranks that would constitute a triplet
            if hand_dict[rank] >= 3:
                triplet_ranks_set.add(rank)
        sequence_of_triplets_list = [] # get a list of lists representing all valid sequences of triplets in "ranks form", expected be in sorted order when added to later on
        possible_lengths = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12) # check all possible lengths of a sequence of triplets
        for length in possible_lengths: # check all possible lengths in order of smallest length to largest length
            for i in range((len(RANK_ORDER) - 3) - length + 1): # check all possible sequences given a length, 2's and Jokers not allowed, off-by-one for range() function
                sequence_window = RANK_ORDER[i : (i + length)] # get needed ranks for the candidate sequence
                sequence_window_set = set(sequence_window)
                if sequence_window_set.issubset(triplet_ranks_set): # if valid sequence of triplets found
                    sequence_of_triplets_list.append(sequence_window) # append to our list of lists, should be in sorted order

        singles_ranks_list = [] #  get a list of all valid singles in "ranks form", expected be in sorted order when added to later on
        for rank in sorted_cards(list(hand_dict.keys())): # iterate in sorted order
            if hand_dict[rank] >= 1: 
                singles_ranks_list.append(rank)

        # now that we have a list of all sequences of triplets and a list of all singles ranks, create valid combinations
        for sequence in sequence_of_triplets_list: # iterate over every possible sequence of triplets
            valid_singles_ranks = []
            for rank in singles_ranks_list: # get list of valid singles we can attach to each triplet being considered
                if rank not in sequence: # rank of attached singles card must not be same as any triplet rank being considered
                    valid_singles_ranks.append(rank)
            if len(valid_singles_ranks) >= len(sequence): # only construct combinations where have enough singles to attach to each triplet being considered
                possible_attachments = combinations(valid_singles_ranks, len(sequence)) # get all "n choose k combinations" where each represents a possible group of "attachments"
                for attachment in possible_attachments: # now construct our combinations of the sequence of triplets being considered and all possible "attachments"
                    found_combo = []
                    for rank in sequence: # construct the sequence of triplets first
                        for j in range(3): # "i" was previously used, so we use "j" since using "i" would exist in same scope as previous "i" (scoping unit in Python is a function)
                            found_combo.append(rank)
                    for rank in attachment: # then attach the ranks of the possible attachment being considered
                        found_combo.append(rank)
                    if not ("B" in found_combo and "R" in found_combo): # exception: combos can't contain both Jokers as attachments
                        combos.append(found_combo)
        return combos
    elif combo_type == "sequence of triplets with pairs": 
        triplet_ranks_set = set()
        for rank in hand_dict: # get all ranks that would constitute a triplet
            if hand_dict[rank] >= 3:
                triplet_ranks_set.add(rank)
        sequence_of_triplets_list = [] # get a list of lists representing all valid sequences of triplets in "ranks form", expected be in sorted order when added to later on
        possible_lengths = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12) # check all possible lengths of a sequence of triplets
        for length in possible_lengths: # check all possible lengths in order of smallest length to largest length
            for i in range((len(RANK_ORDER) - 3) - length + 1): # check all possible sequences given a length, 2's and Jokers not allowed, off-by-one for range() function
                sequence_window = RANK_ORDER[i : (i + length)] # get needed ranks for the candidate sequence
                sequence_window_set = set(sequence_window)
                if sequence_window_set.issubset(triplet_ranks_set): # if valid sequence of triplets found
                    sequence_of_triplets_list.append(sequence_window) # append to our list of lists, should be in sorted order

        pairs_ranks_list = [] #  get a list of all valid pairs in "ranks form", expected be in sorted order when added to later on 
        for rank in sorted_cards(list(hand_dict.keys())): # iterate in sorted order
            if hand_dict[rank] >= 2: 
                pairs_ranks_list.append(rank)

        # now that we have a list of all sequences of triplets and a list of all pairs ranks, create valid combinations
        for sequence in sequence_of_triplets_list: # iterate over every possible sequence of triplets
            valid_pairs_ranks = []
            for rank in pairs_ranks_list: # get list of valid pairs we can attach to each triplet being considered
                if rank not in sequence: # rank of attached pairs cards must not be same as any triplet rank being considered
                    valid_pairs_ranks.append(rank)
            if len(valid_pairs_ranks) >= len(sequence): # only construct combinations where have enough pairs to attach to each triplet being considered
                possible_attachments = combinations(valid_pairs_ranks, len(sequence)) # get all "n choose k combinations" where each represents a possible group of "attachments"
                for attachment in possible_attachments: # now construct our combinations of the sequence of triplets being considered and all possible "attachments"
                    found_combo = []
                    for rank in sequence: # construct the sequence of triplets first
                        for j in range(3): # "i" was previously used, so we use "j" since using "i" would exist in same scope as previous "i" (scoping unit in Python is a function)
                            found_combo.append(rank)
                    for rank in attachment: # then attach the ranks of the possible attachment being considered
                        for k in range(2): # "j" was previously used, so we use "k" since using "j" would exist in same scope as previous "j" (scoping unit in Python is a function)
                            found_combo.append(rank)
                    combos.append(found_combo)
        return combos   
    elif combo_type == "quad with two singles":
        quad_ranks = []
        singles_ranks = []
        for rank in sorted_cards(list(hand_dict.keys())): # iterate in sorted order
            if hand_dict[rank] >= 4: # shouldn't have more than 4 of a card, but we use >= in case of future changes to game
                quad_ranks.append(rank)
            if hand_dict[rank] >= 1: # note that quad_ranks and singles_ranks can have elements in common here
                singles_ranks.append(rank) 
        for quad_rank in quad_ranks: # create all combinations of quads with singles (already in sorted order)
            valid_singles_ranks = []
            for rank in singles_ranks:
                if rank != quad_rank:
                    valid_singles_ranks.append(rank)
            if len(valid_singles_ranks) >= 2: # only construct combinations where we have enough singles to attach to the quad being considered
                possible_attachments = combinations(valid_singles_ranks, 2) # get all "n choose 2 combinations" where each represents a possible group of "attachments"
                for attachment in possible_attachments: # now construct our combinations of the quad being considered with all possible "attachments" 
                    found_combo = []
                    for i in range(4):
                        found_combo.append(quad_rank)
                    for rank in attachment: # then attach the ranks of the possible attachment being considered
                        found_combo.append(rank)
                    if not ("B" in found_combo and "R" in found_combo): # exception: combos can't contain both Jokers as attachments
                        combos.append(found_combo)
        return combos
    elif combo_type == "quad with two pairs":
        quad_ranks = []
        pairs_ranks = []
        for rank in sorted_cards(list(hand_dict.keys())): # iterate in sorted order
            if hand_dict[rank] >= 4: # shouldn't have more than 4 of a card, but we use >= in case of future changes to game
                quad_ranks.append(rank)
            if hand_dict[rank] >= 2: # note that quad_ranks and pairs_ranks can have elements in common here
                pairs_ranks.append(rank) 
        for quad_rank in quad_ranks: # create all combinations of quads with pairs (already in sorted order)
            valid_pairs_ranks = []
            for rank in pairs_ranks:
                if rank != quad_rank:
                    valid_pairs_ranks.append(rank)
            if len(valid_pairs_ranks) >= 2: # only construct combinations where we have enough pairs to attach to the quad being considered
                possible_attachments = combinations(valid_pairs_ranks, 2) # get all "n choose 2 combinations" where each represents a possible group of "attachments"
                for attachment in possible_attachments: # now construct our combinations of the quad being considered with all possible "attachments" 
                    found_combo = []
                    for i in range(4):
                        found_combo.append(quad_rank)
                    for rank in attachment: # then attach the ranks of the possible attachment being considered
                        for j in range(2): # "i" was previously used, so we use "j" since using "i" would exist in same scope as previous "i" (scoping unit in Python is a function)
                            found_combo.append(rank)
                    combos.append(found_combo)
        return combos    
    elif combo_type == "bomb": 
        for rank in sorted_cards(list(hand_dict.keys())): # iterate in sorted order
            if hand_dict[rank] >= 4: # shouldn't have more than 4 of a card, but we use >= in case of future changes to game
                found_combo = [rank, rank, rank, rank]
                combos.append(found_combo)
        return combos    
    elif combo_type == "rocket":
        if "B" in hand_dict and "R" in hand_dict:
            found_combo = ["B", "R"]
            combos.append(found_combo)
        return combos
    else: # in this case, combos is an empty list
        return combos 

def get_computer_move(played_combo, hand):
    """
    Takes a played combo and a hand as arguments and returns a choice for the computer. 
    It does not modify hand argument if a choice to play a combo is made. 
    Will either return a combo to be played or "pass" 
    """
    if len(hand) == 0: # check that hand is empty (game should be over if it reaches this)
        raise AssertionError("Hand is empty and should indicate end of game")
    if played_combo is None: # case where playing on a new round, note that it plays a combo if possible rather than choosing to "pass"
        for combo_type in DEFINED_COMBOS: # iterate through defined combos
            candidate_combos = get_combos(hand, combo_type) # look for combos of the combo type being considered 
            if len(candidate_combos) != 0: # found candidate combos
                playing_combo = candidate_combos[0] # pick the first candidate combo as the combo to be played
                return playing_combo
    else: # case where we are playing on a player's combo that has been played last turn 
        combo_type = get_combo_type(played_combo) # get the type of combo that was played
        candidate_combos = get_combos(hand, combo_type) # get all the possible combos of the specified combo type from the hand
        if combo_type != "bomb": # in the case where the played combo is not a bomb
            for combo in get_combos(hand, "bomb"): # if hand contains bombs, append it to candidate_combos
                candidate_combos.append(combo)
        if combo_type != "rocket": # in the case where the played combo is not a rocket
            for combo in get_combos(hand, "rocket"): # if hand contains a rocket, append it to candidate_combos
                candidate_combos.append(combo)
        if len(candidate_combos) != 0: # if there are any candidate combos that can be played, including bombs or rocket (if any)
            for candidate_combo in candidate_combos: # iterate over the list of candidate combos 
                if is_playable(played_combo, candidate_combo): # check if the given candidate combo can be played
                    playing_combo = candidate_combo # found playable combo, pick it to be played
                    return playing_combo
            return "pass" # found candidate combos, but they were not playable, so computer must choose to "pass"
        else: # no candidate combos of the specified combo type were found, so computer must choose to "pass"
            return "pass"                   

def get_player_move(played_combo, hand):
    """
    Takes a played combo and a hand as arguments and returns a choice for the user based on user input. 
    It does not modify hand argument if a choice to play a combo is made. 
    Will either return a combo to be played or "pass" based on user input. 
    """
    if len(hand) == 0: # check that hand is empty (game should be over if it reaches this)
        raise AssertionError("Hand is empty and should indicate end of game")
    if played_combo is None: # indicates start of new round
        print(f"It is now your turn. You are starting the new round; you may play any combo.")
    else: # playing on an already played combo
        print(f"\tIt is now your turn. The last played combo is: {played_combo} ({get_combo_type(played_combo)})")
    print(f"\tYour hand: {hand}")
    user_move = None
    while user_move is None: # input-validation loop
        user_input = input("\tPlease input your cards separated by spaces or pass (e.g., \"3 3\", \"10 J Q K A\", \"B R\", \"pass\"): ")
        user_choice = user_input.strip()

        if (user_choice.lower() == "pass"): # user chooses to pass
            if (played_combo is None): # user cannot pass on a start of a new round
                print("\tCannot pass on a new round. Must play a combo.")
            else: # not a new round, valid to choose "pass"
                user_move = "pass"
        else: # user inputs cards
            user_combo = user_choice.upper().split()

            # check that any cards were entered
            is_nonempty = True
            if len(user_combo) == 0:
                is_nonempty = False

            # check that the inputted cards are all valid
            all_valid_cards_in_combo = True
            invalid_cards = []
            for card in user_combo:
                if card not in RANK_ORDER:
                    all_valid_cards_in_combo = False
                    invalid_cards.append(card)

            # check that the inputted cards are actually all contained in the hand
            hand_contains_all_cards = True
            uncontained_cards = []
            if all_valid_cards_in_combo: # we use this if statement because this block raises ValueError if an invalid card is found
                user_combo_dict = {}
                for card in user_combo: # put user combo into a dictionary representing frequency of each card
                    if card not in user_combo_dict:
                        user_combo_dict[card] = 1
                    else:
                        user_combo_dict[card] += 1
                hand_dict = {}
                for card in hand: # put hand into a dictionary representing frequency of each card
                    if card not in hand_dict:
                        hand_dict[card] = 1
                    else:
                        hand_dict[card] += 1
                for card in sorted_cards(list(user_combo_dict.keys())): # iterate in sorted order
                    if card not in hand_dict: # hand doesn't contain the card
                        for i in range(user_combo_dict[card]): # update uncontained cards
                            uncontained_cards.append(card) 
                    else: # hand contains the card
                        if hand_dict[card] < user_combo_dict[card]: # hand doesn't contain enough specified cards
                            for i in range(user_combo_dict[card] - hand_dict[card]):
                                uncontained_cards.append(card)
                if len(uncontained_cards) != 0:
                    hand_contains_all_cards = False

            # check that the inputted cards don't form an invalid combo
            valid_combo = True
            if get_combo_type(user_combo) == "invalid combo":
                valid_combo = False
            
            # check that the inputted cards are actually playable (beat the played combo)
            playable_combo = True
            if not is_playable(played_combo, user_combo):
                playable_combo = False

            if not is_nonempty:
                print("\t\tNo cards entered.")
            elif not all_valid_cards_in_combo: 
                print(f"\t\tInvalid cards found: {invalid_cards}")
            elif not hand_contains_all_cards:
                print(f"\t\tHand doesn't contain enough of following cards: {uncontained_cards}")
            elif not valid_combo:
                print("\t\tGiven cards do not form a valid combo.")
            elif not playable_combo:
                print(f"\t\tYour combo does not beat the last played combo. Must match shape/length (unless bomb/rocket) and be higher ranked.")  
            else: 
                user_move = user_combo
    return user_move

def remove_combo_from_hand(combo, hand):
    """
    Takes a combo and a hand as arguments and modifies hand in place by removing combo from it.
    """
    for card in combo: # check for invalid cards in combo
        if card not in RANK_ORDER: 
            raise ValueError("invalid card found")
    for card in hand: # check for invalid cards in hand
        if card not in RANK_ORDER: 
            raise ValueError("invalid card found")
    uncontained_cards = []
    combo_dict = {}
    for card in combo: # put combo into a dictionary representing frequency of each card
        if card not in combo_dict:
            combo_dict[card] = 1
        else: 
            combo_dict[card] += 1
    hand_dict = {}
    for card in hand: # put hand into a dictionary representing frequency of each card
        if card not in hand_dict:
            hand_dict[card] = 1
        else: 
            hand_dict[card] += 1
    for card in sorted_cards(list(combo_dict.keys())): # iterate in sorted order
        if card not in hand_dict: # hand doesn't contain the card
            for i in range(combo_dict[card]): # update uncontained cards
                uncontained_cards.append(card)
        else: # hand contains the card
            if hand_dict[card] < combo_dict[card]: # hand doesn't contain enough specified cards
                for i in range(combo_dict[card] - hand_dict[card]):
                    uncontained_cards.append(card)
    if len(uncontained_cards) != 0: 
        raise ValueError(f"Hand does not contain all cards in combo; missing: {uncontained_cards}")
    for card in combo:
        hand.remove(card)


if __name__ == "__main__":
    """ 
    Plays a game of Beat the Landlord. We skip the bidding phase and assign the user as one of the peasants.
    The turn order is: landlord, user, other peasant. 
    """
    deck = generate_shuffled_deck() # generate shuffled deck
    hand_1, hand_2, hand_3, leftovers = deal_hands_with_leftovers(deck) # deal cards
    for card in leftovers: # automatically give leftovers pile to landlord (hand_3) - skipping bidding phase 
        hand_3.append(card)
    hand_1 = sorted_cards(hand_1) # sorts user's hand for easier viewing

    turn_order = ("landlord", "user", "peasant")
    current_player = "landlord" 
    last_played_combo = None
    passes_in_a_row = 0
    winner = None

    print("Game start. Landlord starts game.")
    print()
    while winner is None:

        # get current player's move 
        if current_player == "user":
            time.sleep(1)
            move = get_player_move(last_played_combo, hand_1)
        elif current_player == "landlord":
            move = get_computer_move(last_played_combo, hand_3)
        else: # current_player == peasant
            move = get_computer_move(last_played_combo, hand_2)

        if move == "pass": # player chose to pass
            passes_in_a_row += 1
            time.sleep(1)
            print(f"{current_player.title()} passes")
        
            if passes_in_a_row == 2: # check the case where we end the round and start a new round
                current_player_index = turn_order.index(current_player) 
                updated_current_player_index = (current_player_index + 1) % len(turn_order)
                current_player = turn_order[updated_current_player_index] # update current player to person who won the round (next player)
                last_played_combo = None 
                passes_in_a_row = 0
                time.sleep(1)
                print("End of round. Starting new round.")
                print()
            else: # only one pass so far, move to next person
                current_player_index = turn_order.index(current_player) 
                updated_current_player_index = (current_player_index + 1) % len(turn_order)
                current_player = turn_order[updated_current_player_index] # update current player to next player

        else: # player chose to play a combo
            if current_player == "user":
                remove_combo_from_hand(move, hand_1)
            elif current_player == "landlord":
                remove_combo_from_hand(move, hand_3)
            else: # current_player = peasant
                remove_combo_from_hand(move, hand_2)
            
            last_played_combo = move # update the last played combo
            passes_in_a_row = 0 # reset number of passes in a row

            if current_player == "user":
                print(f"{current_player.title()} plays: {last_played_combo} ({get_combo_type(last_played_combo)}) [cards left: {len(hand_1)}]")
            elif current_player == "landlord":
                time.sleep(1)
                print(f"{current_player.title()} plays: {last_played_combo} ({get_combo_type(last_played_combo)}) [cards left: {len(hand_3)}]")
            else: # current_player == "peasant":
                time.sleep(1)
                print(f"{current_player.title()} plays: {last_played_combo} ({get_combo_type(last_played_combo)}) [cards left: {len(hand_2)}]")

            # check win condition
            if current_player == "user":
                if len(hand_1) == 0:
                    winner = current_player
            elif current_player == "landlord":
                if len(hand_3) == 0:
                    winner = current_player            
            else: # current_player = peasant
                if len(hand_2) == 0:
                    winner = current_player    
            
            if winner is None: # nobody has won yet, so move to next player
                current_player_index = turn_order.index(current_player) 
                updated_current_player_index = (current_player_index + 1) % len(turn_order)
                current_player = turn_order[updated_current_player_index] # update current player to next player

    time.sleep(1)
    print()
    print("Game is over")
    print(f"Winner: {winner.title()}")
    if winner == "landlord":
        print("Landlord wins")
    else: # winner == "user" or winner == "peasant"
        print("Peasants win")
# Range container support input in GTO+ text combos format.

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

deck2 = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
deck = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

# init cover /may change to static variable later
cover_list_temp = []
for i in range(len(deck2) - 1, -1, -1):
    cover_row_temp = []
    for j in range(len(deck2) - 1, -1, -1):
        if i == j:  # pocket
            cover_row_temp.append(deck2[i] + deck2[j])
        elif j < i:  # suit
            cover_row_temp.append(deck2[max(i, j)] + deck2[min(i, j)] + "s")  # max, min use for order card
        else:
            cover_row_temp.append(deck2[max(i, j)] + deck2[min(i, j)] + "o")
    cover_list_temp.append(cover_row_temp)

cover = np.array(cover_list_temp)


# return position of combo in 13x13 table as i,j
def get_combo_position(combo):
    n = len(combo)
    first_card = combo[0]
    second_card = combo[1]
    index_first_card = deck.index(first_card)
    index_second_card = deck.index(second_card)

    if n == 2:  # it's pocket
        return index_first_card, index_second_card
    elif n == 3:
        if combo[2] == 's':  # it's suit
            return index_first_card, index_second_card
        else:  # if not suit then it's off suit
            return index_second_card, index_first_card


# return combo of this position i,j
def pos_to_combo(i, j):
    if i == j:  # pocket
        return deck[i] + deck[j]
    elif j > i:  # suit
        return deck[i] + deck[j] + 's'
    else:  # off suit
        return deck[i] + deck[j] + 'o'


# class Range as poker range container
class Range:
    # create len_deck as length of deck
    # create range_c as range combos
    # create range_p as range in percent
    len_deck = len(deck)
    range_c = np.zeros((len_deck, len_deck))
    range_p = np.zeros((len_deck, len_deck))

    # init range
    def __init__(self, text='None'):
        if text == 'None':
            return
        self.set_range(text)

    # set range to input combos in flopzilla/GTO+ format
    def set_range(cls, text):
        text_order = text.split(',')
        # print(text_order)
        weight = 100.0
        for order in text_order:
            # find weight for each order
            if order[0] == '[':
                weight = float(order[1:5])

            # set start index to first combo
            start_index = order.find(']')
            if start_index == -1:
                start_index = 0
            else:
                start_index += 1  # shift 1

            # set stop index to last combo
            stop_index = order.find('[', start_index)
            if stop_index == -1:
                stop_index = len(order)

            # '/' is special case for last combo
            if '/' in order:
                if order[0] != '[':
                    stop_index = order.find('[')
                    start_index = 0

            # start filling range (case 1 is multi combos/case 2 is single combo)
            if '-' in order:  # case 1
                start_combo, stop_combo = order[start_index:stop_index].split('-')
                i, j = get_combo_position(start_combo)
                ie, je = get_combo_position(stop_combo)
                while i != ie or j != je:
                    cls.add_combo(i, j, weight)
                    if i == j:  # pocket
                        i += 1
                        j += 1
                    elif j < i:  # suit
                        i += 1
                    else:  # off suit
                        j += 1
                cls.add_combo(ie, je, weight)
            else:  # case 2
                i, j = get_combo_position(order[start_index:stop_index])
                cls.add_combo(i, j, weight)

            # check is last combo of this weight
            if order[len(order) - 1] == ']':
                weight = 100.0

        # create range in percent
        cls.set_percent_range()

    # store combos as percent to range_p
    def set_percent_range(cls):
        for i in range(cls.len_deck):
            for j in range(cls.len_deck):
                if i == j:  # pocket
                    cls.range_p[i, j] = (cls.range_c[i, j] / 6) * 100
                elif j > i:  # suit
                    cls.range_p[i, j] = (cls.range_c[i, j] / 4) * 100
                else:  # off suit
                    cls.range_p[i, j] = (cls.range_c[i, j] / 12) * 100

    # add combo to range
    def add_combo(cls, i, j, weight=100):
        if i == j:  # pocket
            w = (weight / 100) * 6
            cls.range_c[i, j] = w
        elif j > i:  # suit
            w = (weight / 100) * 4
            cls.range_c[i, j] = w
        else:  # off suit
            w = (weight / 100) * 12
            cls.range_c[i, j] = w

    # fill range to 100%
    def fill_100_range(cls):
        for i in range(cls.len_deck):
            for j in range(cls.len_deck):
                if i == j: # pocket
                    cls.range_c[i, j] = 6
                elif j > i: # suit
                    cls.range_c[i, j] = 4
                else: # off suit
                    cls.range_c[i, j] = 12

    # get percent of available combos in range
    def get_percent_of_range(cls):
        total_combos = np.sum(cls.range_c)
        return (total_combos / 1326) * 100

    # get number of input combo
    def get_combo(cls, combo):
        i, j = get_combo_position(combo)
        return cls.range_c[i, j]

    # set number of input combo
    def set_combo(cls, number, combo):
        i, j = get_combo_position(combo)
        cls.range_c[i, j] = number

    # get number of input combo by position
    def get_combo_by_pos(cls, i, j):
        return cls.range_c[i, j]

    # set number of input combo by position
    def set_combo_by_pos(cls, number, i, j):
        cls.range_c[i, j] = number

    # display number of combos in range
    def show_combos(cls):
        fig, ax = plt.subplots()
        ax = sns.heatmap(cls.range_c, annot=cls.range_c, square=True, color='white')
        total_combos = np.sum(cls.range_c)
        ax.set_title('Total combos : '+str(total_combos))
        ax.xaxis.tick_top()
        ax.set_xticklabels(deck)
        ax.set_yticklabels(deck, rotation=0)
        plt.tight_layout()
        plt.show()

    # display percent of combos in range
    def show_range(cls):
        fig, ax = plt.subplots()
        ax = sns.heatmap(cls.range_p, annot=cover, fmt='', cmap="YlGnBu", linewidths=.5, linecolor='black',
                         square=True)
        percent_range = cls.get_percent_of_range()
        ax.set_title('Range : '+str(percent_range)+'%')
        ax.xaxis.tick_top()
        ax.set_xticklabels(deck)
        ax.set_yticklabels(deck, rotation=0)
        plt.tight_layout()
        plt.show()

    # display combos and percent of range
    def show(cls):
        pass


if __name__ == '__main__':
    # test
    t = input("Enter range : ").strip()
    A = Range(t)
    # A.fill_100_range()
    # A.show_combos()
    A.show_range()
    A.show_combos()
    # print(get_combo_position('AQs'))
    # B = Range()
    # B.add_combo('AKs',100)
    # B.show_combos()

    # C = Range('AA,[50.0]KK[/50.0]')
    # C.show_combos()

    # D = Range('AKo-AJo')
    # D.show_combos()
